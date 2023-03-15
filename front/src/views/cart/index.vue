<template>
  <div class="page-card container page-nav-bar page-footer-bar">
    <nav-bar title="购物车">
      <template #menu>
        <div class="nav-bar-operate">
          <span v-if="!cartOperateState" @click="cartOperateState = true"
            >编辑</span
          >
          <span v-else @click="cartOperateState = false">完成</span>
        </div>
      </template>
    </nav-bar>
    <Table
      ref="selection"
      class="cart-table"
      :columns="columns"
      :data="shoppingCart"
      size="small"
      @on-selection-change="select"
      no-data-text="您的购物车没有商品，请先添加商品到购物车再点击购买"
    ></Table>
    <div class="go-to card-total">
      <div class="card-total-content">
        <Checkbox
          ref="selectCheckbox"
          :checked.sync="isSelectAll"
          @on-change="handleSelectAll"
          >全选</Checkbox
        >
        <template v-if="cartOperateState">
          <div class="card-total-btn-group">
            <Button @click="removeCartItemList()" class="" type="text"
              >删除选中商品</Button
            >
            <Button @click="clearCart()" class="cart-clear " type="text"
              >清理购物车</Button
            >
          </div>
        </template>
      </div>
      <div class="card-pay-content" v-if="!cartOperateState">
        <div class="amount-sum hidden-xs hidden-sm">
          已选择
          <em>{{ selectCount }}</em
          >件商品
        </div>
        <div class="price-sum">
          <div>
            <span class="txt txt-new">总价：</span>
            <span class="price sumPrice">
              <em>¥ {{ selectedCartSumPrice.toFixed(2) }}</em>
            </span>
            <b class="ml5 price-tips"></b>
            <div
              class="price-tipsbox-new"
              style="left: 55.0375px; display: none;"
            >
              <div class="ui-tips-main">不含运费及送装服务费</div>
              <span class="price-tipsbox-arrow"></span>
            </div>
            <br />
            <div id="price-sum-extra-1" class="price-sum-extra">
              <span class>促销：</span>
              <span class>-¥{{ discountAmount.toFixed(2) }}</span>
            </div>
          </div>
        </div>
        <Button @click="goToPay()" type="error" class="ivu-btn-pay"
          >去结算</Button
        >
      </div>
    </div>
    <footer-bar :active-index="2" />
  </div>
</template>

<script>
import store from "@/vuex/store";
import navBar from "@/components/navBar";
import footerBar from "@/components/footerBar";
import { mapState, mapActions, mapMutations } from "vuex";
export default {
  name: "ShowShoppingCart",
  components: {
    navBar,
    footerBar
  },
  data() {
    return {
      selectedCartSumPrice: 0.0,
      selectCount: 0,
      discountAmount: 0.0,
      isSelectAll: false,
      columns: [
        {
          type: "selection",
          width: 30,
          align: "center",
          className: "cart-column-selection"
        },
        {
          title: "图片",
          key: "image",
          width: 100,
          render: (h, params) => {
            return h("div", [
              h("img", {
                attrs: {
                  class: "cart-column-image",
                  src: params.row.image
                },
                style: {
                  display: "block",
                  width: "80px",
                  height: "80px"
                }
              })
            ]);
          },
          align: "center"
        },
        {
          title: "标题",
          key: "title",
          className: "cart-column-absolute cart-column-title",
          align: "center"
        },
        {
          title: "规格参数",
          width: 198,
          key: "skuSpec",
          className: "cart-column-absolute cart-column-sku ellipsis",
          align: "center",
          render: function(h, params) {
            var spec = this.row.spec;
            // [{"specType":"主体","list":[{"name":"颜色","value":"粉色"},{"name":"尺寸","value":"6.3"},{"name":"网络","value":"5G"}]}]
            var objs = JSON.parse(spec);
            var description = "";
            for (var obj of objs) {
              var list = obj.list;
              for (var li of list) {
                description += li.name + ":" + li.value + " ; ";
              }
            }
            return h("span", description);
          }
        },
        {
          title: "数量",
          key: "amount",
          className: "cart-column-absolute cart-column-amount",
          width: 68,
          align: "center"
        },
        {
          title: "价格",
          width: 100,
          key: "specialPrice",
          className: "cart-column-absolute cart-column-price",
          align: "center",
          render: function(h, params) {
            return h("span", this.row.specialPrice.toFixed(2)); // 这里的this.row能够获取当前行的数据
          }
        },
        {
          title: "小计",
          width: 100,
          key: "specialPrice",
          className: "cart-column-absolute hidden-xs hidden-sm",
          align: "center",
          render: function(h, params) {
            return h(
              "span",
              (this.row.specialPrice.toFixed(2) * this.row.amount).toFixed(2)
            ); // 这里的this.row能够获取当前行的数据
          }
        },
        {
          title: "操作",
          key: "action",
          className: "cart-column-absolute cart-column-action",
          width: 150,
          align: "center",
          render: (h, param) => {
            return h("div", [
              h(
                "span",
                {
                  props: {
                    type: "error",
                    size: "small"
                  },
                  style: {
                    cursor: "pointer"
                  },
                  on: {
                    click: () => {
                      this.remove(param);
                    }
                  }
                },
                "删除"
              )
            ]);
          }
        }
      ],
      cartOperateState: false
    };
  },
  created() {
    this.loadShoppingCart();
  },
  computed: {
    ...mapState(["shoppingCart"])
  },
  methods: {
    ...mapMutations(["SET_SELECTED_CARTITEMS_INFO", "SET_SELECTED_CART_INFO"]),
    ...mapActions([
      "loadShoppingCart",
      "clearShoppingCart",
      "removeCartItems",
      "getPreferentialPrice"
    ]),
    select(data) {
      this.isSelectAll = !!(
        data.length && data.length === this.shoppingCart.length
      );
      this.$refs.selectCheckbox.currentValue = this.isSelectAll;
      const e = this;
      e.selectCount = 0;
      e.selectedCartSumPrice = 0;
      const parmas = [];
      data.forEach(function(val) {
        const param = {};
        param.num = val.amount;
        param.skuId = val.id;
        parmas.push(param);
        e.selectCount++;
      });
      e.discountAmount = 0;
      const json_data = JSON.stringify(parmas)
      const sku_list = { sku_list: json_data}
      this.getPreferentialPrice(sku_list).then(res => {
        res.forEach(function(val) {
          // 选择指定的skuid
          data.forEach(function(val2) {
            if (val2.id === val.skuId) {
              
              e.selectedCartSumPrice += val.discountPrice;
            }
          });
          e.discountAmount += val.reducePrice;
        });
      });
    },
    // 跳转确认订单页
    goToPay() {
      // 检查是否选择商品
      const selectionList = this.$refs.selection.getSelection();
      if (selectionList.length === 0) {
        this.$Message.warning("请至少选择一件商品哟~");
        return;
      }
      // 设置被选中的购物车项
      this.SET_SELECTED_CARTITEMS_INFO(selectionList);
      // 附带优惠信息
      const selectedCartInfo = {};
      selectedCartInfo.discountAmount = this.discountAmount;
      selectedCartInfo.selectedCartItems = selectionList;
      this.SET_SELECTED_CART_INFO(selectedCartInfo);
      this.$router.push("/PayOrder");
    },
    remove(param) {
      const data = [];
      const row = param.row;
      const itemData = {
        sku_no: row.sku_no,
        amount: row.amount
      };
      data.push(itemData);
      const json_data = JSON.stringify(data)
      const sku_list = { sku_list: json_data}
      this.removeCartItems(sku_list).then(data => {
        if (data) {
          this.$Message.success("移除商品成功");
          this.loadShoppingCart();
        } else {
          this.$Message.error("移除购物车商品出错");
        }
      });
    },
    handleSelectAll(value) {
      this.isSelectAll = value;
      this.$refs.selection.selectAll(value);
    },
    // 移除部分购物车选中的商品
    removeCartItemList() {
      const selectionList = this.$refs.selection.getSelection();
      if (selectionList.length === 0) {
        this.$Message.warning("请至少选择一件商品哟~");
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
          this.$Message.success("移除购物车商品成功");
          this.handleSelectAll(false);
          this.loadShoppingCart();
        } else {
          this.$Message.error("移除购物车商品出错");
        }
      });
    },
    // 清空购物车
    clearCart() {
      this.clearShoppingCart().then(data => {
        if (data) {
          this.$Message.success("清空购物车商品成功");
          this.handleSelectAll(false);
          this.loadShoppingCart();
        } else {
          this.$Message.error("清空购物车商品出错");
        }
      });
    }
  },
  store
};
</script>

<style scoped>
.ivu-btn-pay {
  border-radius: 0px;
  font-size: 20px;
  height: 57px;
  width: 127px;
}

.amount-sum {
  color: #999;
  height: 44px;
  line-height: 30px;
  cursor: pointer;
}

.amount-sum em {
  color: #e2231a;
  font-family: verdana;
  font-weight: 700;
  margin: 0 3px;
}

.price-sum {
  height: 43px;
  line-height: 20px;
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
  color: #e2231a;
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
  font-family: verdana, "Microsoft YaHei", SimSun;
}

.cart-clear {
  font-weight: bold;
}
</style>

<style lang="less" scoped>
@media (max-width: 992px) {
  .page-card {
    padding-bottom: 94px;
    padding-left: 0;
    padding-right: 0;
    .nav-bar-operate {
      font-size: 16px;
    }
    .cart-table {
      border: none;

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
          left: 130px;
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
      .card-total-content {
        width: 100%;
        flex-shrink: 1;
        display: flex;
        justify-content: space-between;
        align-items: center;
        height: 48px;
        .card-total-btn-group {
          display: flex;
          align-items: center;
        }
        /deep/ .ivu-btn {
          border: 1px solid #8c8c8c;
          display: block;
          padding: 0 16px;
          height: 30px;
          line-height: 30px;
          text-align: center;
          font-size: 0.6rem;
          border-radius: 15px;
          margin-right: 12px;
        }
      }
      .card-pay-content {
        flex-shrink: 0;
      }
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
@media (min-width: 992px) {
  .page-card {
    margin-top: 48px;
  }
  .card-total {
    padding-left: 15px;
    margin-top: 24px;
    border: 1px solid #f0f0f0;
    .price-sum {
      margin-right: 12px;
    }
  }
}
.card-total {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: hsla(0, 0%, 100%, 0.95);
  .card-pay-content {
    display: flex;
    align-items: center;
  }
}
</style>
