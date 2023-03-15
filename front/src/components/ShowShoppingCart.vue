<template>
  <div>
    <Row>
      <Col span="16" offset="4">
        <Table ref="selection"
               :columns="columns"
               :data="shoppingCart"
               size="small"
               @on-selection-change="select"
               no-data-text="您的购物车没有商品，请先添加商品到购物车再点击购买"></Table>
      </Col>
      <Col span="4"></Col>
    </Row>

    <div class="go-to">
      <Row>
        <Col span="1" offset="4">
            <Button @click="handleSelectAll()" class="cart-bottom" type="text">全选</Button>
        </Col>
        <Col span="2">
          <Button  @click="removeCartItemList()" class="col-4 cart-bottom" type="text">删除选中商品</Button>
        </Col>
        <Col span="1">
          <Button @click="clearCart()" class="col-4 cart-bottom cart-clear" type="text">清理购物车</Button>
        </Col>
        <Col span="2" offset="4">
          <div class="amount-sum cart-bottom">
            已选择<em>{{selectCount}}</em>件商品
          </div>
        </Col>
        <Col span="4">
          <div class="price-sum cart-bottom">
            <div>
              <span class="txt txt-new">总价：</span>
              <span class="price sumPrice">
                <em>¥ {{selectedCartSumPrice.toFixed(2)}}</em>
              </span>
              <b class="ml5 price-tips"></b>
              <div class="price-tipsbox-new" style="left: 55.0375px; display: none;">
                <div class="ui-tips-main">不含运费及送装服务费</div>
                <span class="price-tipsbox-arrow"></span>
              </div>
              <br>
              <div id="price-sum-extra-1" class="price-sum-extra"><span class="">促销：</span><span class="">-¥{{discountAmount.toFixed(2)}}</span></div>
            </div>
          </div>
        </Col>
        <Col span="4">
          <Button @click="goToPay()" type="error" class="ivu-btn-pay">去结算</Button>
        </Col>
      </Row>
    </div>


  </div>
</template>

<script>
import store from '@/vuex/store';
import {mapState, mapActions, mapMutations} from 'vuex';
export default {
  name: 'ShowShoppingCart',
  data () {
    return {
      selectedCartSumPrice: 0.00,
      selectCount: 0,
      discountAmount: 0.00,
      status: false,
      columns: [
        {
          type: 'selection',
          width: 58,
          align: 'center'
        },
        {
          title: '图片',
          key: 'image',
          width: 150,
          render: (h, params) => {
            return h('div', [
              h('img', {
                attrs: {
                  src: params.row.image
                },
                style: {
                  width: '80px',
                  height: '80px'
                }
              })
            ]);
          },
          align: 'center'
        },
        {
          title: '标题',
          key: 'title',
          align: 'center'
        },
        {
          title: '规格参数',
          width: 198,
          key: 'skuSpec',
          align: 'center',
          render: function (h, params) {
            var spec = this.row.skuSpec;
            // [{"specType":"主体","list":[{"name":"颜色","value":"粉色"},{"name":"尺寸","value":"6.3"},{"name":"网络","value":"5G"}]}]
            var objs = JSON.parse(spec);
            var description = '';
            for (var obj of objs) {
              var list = obj.list;
              for (var li of list) {
                description += li.name + ':' + li.value + ' ; ';
              }
            }
            return h('span', description);
          }
        },
        {
          title: '数量',
          key: 'amount',
          width: 68,
          align: 'center'
        },
        {
          title: '价格',
          width: 100,
          key: 'specialPrice',
          align: 'center',
          render: function (h, params) {
            return h('span', this.row.specialPrice.toFixed(2)); // 这里的this.row能够获取当前行的数据
          }
        },
        {
          title: '小计',
          width: 100,
          key: 'specialPrice',
          align: 'center',
          render: function (h, params) {
            return h('span', (this.row.specialPrice.toFixed(2) * this.row.amount).toFixed(2)); // 这里的this.row能够获取当前行的数据
          }
        },
        {
          title: '操作',
          key: 'action',
          width: 150,
          align: 'center',
          render: (h, param) => {
            return h('div', [
              h('span', {
                props: {
                  type: 'error',
                  size: 'small'
                },
                style: {
                  cursor: 'pointer'
                },
                on: {
                  click: () => {
                    this.remove(param);
                  }
                }
              }, '删除')
            ]);
          }
        }
      ]
    };
  },
  created () {
    this.loadShoppingCart();
  },
  computed: {
    ...mapState(['shoppingCart'])
  },
  methods: {
    ...mapMutations(['SET_SELECTED_CARTITEMS_INFO', 'SET_SELECTED_CART_INFO']),
    ...mapActions(['loadShoppingCart', 'clearShoppingCart', 'removeCartItems', 'getPreferentialPrice']),
    select (data) {
      const e = this;
      e.selectCount = 0;
      e.selectedCartSumPrice = 0;
      const parmas = [];
      data.forEach(function (val) {
        const param = {};
        param.num = val.amount;
        param.skuId = val.skuId;
        parmas.push(param);
        e.selectCount++;
      });
      e.discountAmount = 0;
      this.getPreferentialPrice(parmas).then(res => {
        res.forEach(function (val) {
          // 选择指定的skuid
          data.forEach(function (val2) {
            if (val2.skuId === val.skuId) {
              e.selectedCartSumPrice += val.discountPrice * val2.amount;
            }
          });
          e.discountAmount += (val.originPrice - val.discountPrice);
        });
      });
    },
    // 跳转确认订单页
    goToPay () {
      // 检查是否选择商品
      const selectionList = this.$refs.selection.getSelection();
      if (selectionList.length === 0) {
        this.$Message.warning('请至少选择一件商品哟~');
        return;
      }
      // 设置被选中的购物车项
      this.SET_SELECTED_CARTITEMS_INFO(selectionList);
      // 附带优惠信息
      const selectedCartInfo = {};
      selectedCartInfo.discountAmount = this.discountAmount;
      selectedCartInfo.selectedCartItems = selectionList;
      this.SET_SELECTED_CART_INFO(selectedCartInfo);
      this.$router.push('/PayOrder');
    },
    remove (param) {
      const data = [];
      const row = param.row;
      const itemData = {
        skuNo: row.skuNo,
        amount: row.amount
      };
      data.push(itemData);
      this.removeCartItems(data).then(data => {
        if (data) {
          this.$Message.success('移除商品成功');
          this.loadShoppingCart();
        } else {
          this.$Message.error('移除购物车商品出错');
        }
      });
    },
    handleSelectAll () {
      this.status = !this.status;
      this.$refs.selection.selectAll(this.status);
    },
    // 移除部分购物车选中的商品
    removeCartItemList () {
      this.status = !this.status;
      const selectionList = this.$refs.selection.getSelection();
      if (selectionList.length === 0) {
        this.$Message.warning('请至少选择一件商品哟~');
        return;
      }
      const data = [];
      for (var item of selectionList) {
        const param = {
          skuNo: item.skuNo,
          amount: item.amount
        };
        data.push(param);
      }
      this.removeCartItems(data).then(data => {
        if (data) {
          this.$Message.success('移除购物车商品成功');
          this.loadShoppingCart();
        } else {
          this.$Message.error('移除购物车商品出错');
        }
      });
    },
    // 清空购物车
    clearCart () {
      this.clearShoppingCart().then(data => {
        if (data) {
          this.$Message.success('清空购物车商品成功');
          this.loadShoppingCart();
        } else {
          this.$Message.error('清空购物车商品出错');
        }
      });
    }
  },
  store
};
</script>

<style scoped>

.go-to {
  margin-bottom: 0px;
  position: fixed;
  bottom: 0px;
  z-index: 999;
  width: 100%;
  background-color: #8b959e29;
}

.ivu-btn-pay {
  border-radius: 0px;
  font-size: 20px;
  height: 57px;
  width: 127px;
}

.cart-bottom {
  margin-top: 15px;
}

.amount-sum {
  color: #999;
  height: 44px;
  line-height: 30px;
  cursor: pointer;
}

.amount-sum em {
  color: #E2231A;
  font-family: verdana;
  font-weight: 700;
  margin: 0 3px;
}

.price-sum {
  float: right;
  height: 43px;
  line-height: 20px;
  margin: 7px 5px 0 10px;
  color: #666;
  width: auto;
  position: relative;
}
.price-sum .txt-new {
  width: 50px;
}

.price-sum .txt {
  float: left;
  width: 50px;
  text-align: right;
  color: #999;
}

.price-sum .price {
  display: inline-block;
  *display: inline;
  *zoom: 1;
  text-align: right;
  font-family: verdana;
}

.price-sum .price em {
  font-size: 16px;
  color: #E2231A;
  font-weight: 700;
}

.price-sum-extra {
  position: absolute;
  right: 0;
  width: auto;
  text-align: right;
  padding-right: 5px;
}

.price-sum-extra span {
  color: #666;
  font-family: verdana,"Microsoft YaHei",SimSun;
}

.cart-clear {
  font-weight: bold;
}

</style>
