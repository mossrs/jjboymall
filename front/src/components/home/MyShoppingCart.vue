<template>
<Layout class="layout">
  <nav-bar title="我的购物车" />
  <div class="page-card">
    <Table class="cart-table" border ref="selection" :columns="columns" :data="shoppingCart" size="large" @on-selection-change="select" no-data-text="您的购物车没有商品，请先添加商品到购物车再点击购买"></Table>
    <div class="go-to">
      <Button @click="handleSelectAll()" class="col-4">全选</Button>
      <Button @click="removeCartItemList()" class="col-4">删除选中商品</Button>
      <Button @click="clearCart()" class="col-4">清空购物车</Button>
      <Button @click="goTo" type="primary">去付款</Button>
    </div>
  </div>
  <Footer class="layout-footer-center">2018 &copy; Gavin</Footer>
</Layout>
</template>

<script>
import store from '@/vuex/store';
import { mapState, mapActions } from 'vuex';
import navBar from '@/components/navBar'
export default {
  name: 'MyShoppingCart',
  data () {
    return {
      status: false,
      columns: [
        {
          type: 'selection',
          width: 50,
          align: 'center',
          className: 'cart-column-selection'
        },
        {
          title: '图片',
          key: 'img',
          width: 100,
          render: (h, params) => {
            return h('div', [
              h('img', {
                attrs: {
                  class: 'cart-column-image',
                  src: params.row.img
                }
              })
            ]);
          },
          align: 'center'
        },
        {
          title: '标题',
          key: 'title',
          className: 'cart-column-absolute cart-column-title',
          align: 'center'
        },
        {
          title: '规格参数',
          width: 198,
          key: 'skuSpec',
          className: 'cart-column-absolute cart-column-sku ellipsis',
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
          className: 'cart-column-absolute cart-column-amount',
          align: 'center'
        },
        {
          title: '价格',
          width: 100,
          key: 'specialPrice',
          className: 'cart-column-absolute cart-column-price',
          align: 'center',
          render: function (h, params) {
            return h('span', this.row.specialPrice.toFixed(2)); // 这里的this.row能够获取当前行的数据
          }
        },
        {
          title: '操作',
          key: 'action',
          width: 150,
          className: 'cart-column-absolute cart-column-action',
          align: 'center',
          render: (h, param) => {
            return h('div', [
              h('Button', {
                props: {
                  type: 'error',
                  size: 'small'
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
    ...mapActions(['loadShoppingCart', 'clearShoppingCart', 'removeCartItems']),
    select (data) {
      console.log('选择购物车.....');
      console.log(data);
    },
    goTo () {
      this.$router.push('/order');
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
        this.$Message.error('没有选中商品');
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
  components: {
    navBar
  },
  store
};
</script>

<style lang="less" scoped>
.layout{
  // padding-top: 44px;
}
.go-to {
  margin: 15px;
  display: flex;
  justify-content: flex-end;
  flex-wrap: wrap;
}
.content {
  // margin: 15px;
  background-color: #fff;
  padding: 15px;
}
.layout-footer-center {
  padding: 0px 15px;
  padding-bottom: 15px;
  text-align: center;
}

/deep/.cart-column-selection .ivu-table-cell{
  text-overflow: initial
}

@media (max-width: 992px) {
  .page-card {
    padding-bottom: 94px;
    padding-left: 0;
    padding-right: 0;
    .cart-table {
      border: none;

      /deep/.ivu-table-border td{
        border: none !important;
      }

      /deep/ .ivu-table-wrapper {
        .ivu-table:before {
          content: none;
        }
      }
      /deep/ .ivu-table-header {
        display: none;
      }
      /deep/ .ivu-table-body {
        overflow: hidden;
      }
      /deep/ .ivu-table-row {
        position: relative;
        > td {
          border-bottom: 0;
          background: #fff;
        }
        .ivu-table-cell {
          padding: 0;
        }
        .cart-column-selection {
          transform: translateY(-15px);
        }
        .cart-column-image {
          width: 100px !important;
          height: 100px !important;
          border-radius: 6px;
          margin-bottom: 30px;
        }
        .cart-column-absolute {
          position: absolute;
        }
        .cart-column-title {
          right: 15px;
          left: 150px;
          max-height: 40px;
          font-size: 12px;
          color: #262626;
          span {
            overflow: hidden;
            text-overflow: ellipsis;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
          }
        }
        .cart-column-sku {
          margin-top: 40px;
          background: #f2f2f2;
          padding: 0 6px;
          height: 16px;
          line-height: 16px;
          font-size: 12px;
          color: #262626;
          border-radius: 8px;
        }
        .cart-column-amount {
          right: 15px;
          margin-top: 60px;
        }
        .cart-column-price {
          padding-left: 6px;
          margin-top: 60px;
        }
        .cart-column-action {
          right: 15px;
          margin-top: 80px;
        }
      }
    }
    .card-total {
      position: fixed;
      left: 0;
      right: 0;
      z-index: 20;
      bottom: 50px;
      padding-left: 6px;
      padding-bottom: 4px;
      border-top: 1px solid #ddd;
      .ivu-btn-pay {
        font-weight: 700;
        margin: 0 12px;
        display: block;
        width: 113px;
        height: 38px;
        text-align: center;
        border-radius: 20px;
        background-color: #f2270c;
        color: #fff;
        font-size: 14px;
        background-image: linear-gradient(
          135deg,
          #f2140c,
          #f2270c 70%,
          #f24d0c
        );
      }
    }
  }
}
</style>
