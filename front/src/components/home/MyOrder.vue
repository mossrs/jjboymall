<template>
<Layout class="layout">
  <nav-bar title="我的订单" />
    <div class="page-card">
      <Table border class="cart-table" :columns="columns" :data="order" size="large" no-data-text="你还没有订单，快点去购物吧"  :stripe="true"></Table>
      <div class="page-size">
        <Page
         :total='orderTotal' 
         :current="pageIndex" 
         :pageSize="pageSize" 
         @on-change="changePage">
         </Page>
      </div>
    </div>
  <Footer class="layout-footer-center">2018 &copy; Gavin</Footer>
</Layout>
  
</template>

<script>
import store from '@/vuex/store';
import {mapState, mapActions} from 'vuex';
import navBar from '@/components/navBar'
export default {
  name: 'MyOrder',
  created () {
    const pageDto = {
      pageIndex: 1,
      pageSize: this.pageSize
    };
    this.getOrder(pageDto);
  },
  data () {
    return {
      self: this,
      pageIndex: 1,
      pageSize: 10,
      columns: [
        {
          title: '序号',
          width: 60,
          align: 'center',
          className: 'cart-column-number',
          render: (h, params) => {
            return h('span', params.index + (this.pageIndex - 1) * this.pageSize + 1);
          }
        },
        {
          title: '订单号',
          key: 'order_number',
          width: 400,
          className: ' cart-column-absolute cart-column-order',
          align: 'center'
        },
        {
          title: '下单日期',
          width: 198,
          key: 'gmt_create',
          className: 'cart-column-absolute cart-column-date',
          align: 'center',
          render: function (h, params) {
            let date = new Date(this.row.gmt_create);
            return h('div', {props: {}},
              // 这里的this.row能够获取当前行的数据
              date.toLocaleString());
          }
        },
        {
          title: '支付金额',
          key: 'pay_amount',
          width: 200,
          className: 'cart-column-absolute cart-column-goal',
          align: 'center'
        },
        {
          title: '订单状态',
          width: 150,
          key: 'order_status',
          className: 'cart-column-absolute cart-column-status',
          align: 'center',
          render (h, param) {
            const orderStatus = this.row.order_status;
            let orderStatusStr = '';
            if (orderStatus === 0) {
              orderStatusStr = '待付款';
            } else if (orderStatus === 2) {
              orderStatusStr = '待发货';
            } else if (orderStatus === 11) {
              orderStatusStr = '已退款';
            } else {
              orderStatusStr = '已取消';
            }
            return h('div', {props: {}}, orderStatusStr);
          }
        },
        {
          title: '支付方式',
          width: 120,
          key: 'payType',
          className: 'cart-column-absolute cart-column-type',
          align: 'center',
          render (h, param) {
            const payType = this.row.payType;
            let payTypeStr = '';
            if (payType === 1) {
              payTypeStr = '支付宝';
            } else {
              payTypeStr = '微信支付';
            }
            return h('div', {props: {}}, payTypeStr);
          }
        },
        {
          title: '操作',
          key: 'action',
          fixed: 'right',
          className: 'cart-column-absolute cart-column-opatation',
          width: 120,
          render (h, param) {
            const orderNumber = this.row.order_number;
            let detail = h('router-link', {style: {type: 'text', size: 'small'},
              on: {
                click: () => {
                  console.log(this);
                }
              },
              props: {to: {path: '/home/orderItems', query: {orderNumber}}}}, '查看详情');
            return detail;
          }
        }
      ]
    };
  },
  computed: {
    ...mapState(['order', 'orderTotal'])
  },
  methods: {
    ...mapActions(['getOrder']),
    changePage (index) {
      this.pageIndex = index;
      const pageDto = {
        pageIndex: index,
        pageSize: this.pageSize
      };
      this.getOrder(pageDto);
    }
  },
  components: {
    navBar
  },
  store
};

Date.prototype.toLocaleString = function () {
  // 补0   例如 2018/7/10 14:7:2  补完后为 2018/07/10 14:07:02
  function addZero (num) {
    if (num < 10) {
      return '0' + num;
    }
    return num;
  }
  // 按自定义拼接格式返回
  return this.getFullYear() + '/' + addZero(this.getMonth() + 1) + '/' + addZero(this.getDate()) + ' ' +
    addZero(this.getHours()) + ':' + addZero(this.getMinutes()) + ':' + addZero(this.getSeconds());
};
</script>

<style lang="less" scoped>
.layout{
  // padding-top: 44px;
}
.order-container {
  width: 80%;
  margin: 15px auto;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0px 0px 5px #ccc;
}

.order-header {
  height: 38px;
}

.order-container p {
  font-size: 14px;
  line-height: 26px;
}

.order-container h3 {
  line-height: 30px;
}

.order-content-title {
  color: #999;
}

.page-size {
  margin: 15px 0px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
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

@media (max-width: 992px) {
  .page-card {
    padding-left: 0;
    padding-right: 0;
    .cart-table {
      border: none;

      /deep/.ivu-table-fixed-header{
        display: none;
      }
      /deep/.ivu-table-fixed-right{
        box-shadow: none;
      }

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
        .cart-column-absolute {
          position: absolute;
        }
        .cart-column-number{
          padding: 26px 0;
          width: 10px !important;
        }
        .cart-column-order{
          height: 20px;
        }
        .cart-column-type {
          margin-top: 20px;
          height: 20px;
        }
        .cart-column-goal {
          height: 20px;
          right: 20px;
          margin-top: 20px;
        }
        .cart-column-date {
          height: 20px;
          margin-top: 40px;
        }
        .cart-column-status {
          height: 20px;
          right: 20px;
        }
        .cart-column-opatation{
          height: 20px;
          margin-top: 40px;
          right: 20px;
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
