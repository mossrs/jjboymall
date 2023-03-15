<template>
  <div class="order-wrap">
    <div class="order-container">
      <div class="order-header">
        <h2>订单号: {{orderItems.order_number}}</h2>
      </div>
      <div>
        <p><span class="order-content-title"> 收 货 人 :</span> {{orderItems.receiver_name}}</p>
        <p><span class="order-content-title"> 收货电话 :</span> {{orderItems.receiver_phone}}</p>
        <p><span class="order-content-title"> 收货地址 :</span> {{orderItems.receiver_detail_address}}</p>
        <p><span class="order-content-title"> 付款总额 :</span> {{orderItems.pay_amount}}
          <Button type="error" v-show="this.show" v-if="orderItems.order_status === 1" size="large"  @click="refundOrder">退款</Button>
        </p>
        <h3>下面是订单详情</h3>
      </div>
      <div>
        <Collapse >
          <Panel  v-for="(orderDetail, oIndex) in orderItems.items" :key="oIndex">
            <p slot="content"><span class="order-content-title"> 商品名称 :</span>
              <router-link :to="{ path: '/goodsDetail', query: { goodsId: orderDetail.product_spu_id, merchantId: '1' ,relCategory3Id:orderDetail.product_category_id } }">{{orderDetail.product_name}}</router-link>
            </p>
            <p slot="content"><span class="order-content-title"> 商品数量 :</span>{{orderDetail.product_quantity}}</p>
            <p slot="content"><span class="order-content-title"> 商品正常价格 :</span>{{orderDetail.product_normal_price}}</p>
            <p slot="content"><span class="order-content-title"> 商品销售价格 :</span>{{orderDetail.product_price}}</p>
            <!--
                        <p slot="content"><span class="order-content-title"> 商品结算价格 :</span>{{orderDetail.productSettlementPrice}}</p>
            -->
            <!--
                        <p slot="content"><span class="order-content-title"> 商品总价格 :</span>{{orderDetail.productQuantity * orderDetail.productSettlementPrice}}</p>
            -->
            <!-- <p slot="content"><span class="order-content-title"> 商品属性 :</span>{{orderDetail.productAttr}}</p>-->
            <!--
                        <p slot="content"><span class="order-content-title"> 商品套餐 :</span>{{orderDetail.attrTitle}}</p>
            -->
            <!--
                        <p slot="content"><span class="order-content-title"> 商品图片 :</span><img :src="orderDetail.img"></p>
            -->
          </Panel>
        </Collapse>
      </div>
    </div>
  </div>
</template>

<script>
  import store from '@/vuex/store';
  import {mapState, mapActions} from 'vuex';

  export default {
    name: 'OrderItems',
    created() {
      const orderNumber = this.$route.query;
      console.log(orderNumber);
      this.getOrderItems(orderNumber);
    },
    compile (template) {
      console.log(this.orderItems);
    },
    data () {
      return {
        self: this,
        show: true
      };
    },
    computed: {
      ...mapState(['orderItems'])
    },
    methods: {
      ...mapActions(['getOrderItems', 'refund']),
      refundOrder () {
        let data = {
          orderNumber: this.orderItems.orderNumber,
          reason: '退货'
        };
        this.refund(data).then(data => {
          if (data) {
            this.$Message.success('退款成功');
            this.show = false;
            console.log(this.orderItems);
          } else {
            this.$Message.error('退款失败, 请稍后重试');
          }
        });
        return 1;
      }
    },
    store
  };
</script>

<style scoped>
  .order-wrap {
    flex: 1;
  }
  .order-container {
    width: 80%;
    margin: 15px auto;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0px 0px 5px #ccc;
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
  .order-header h2{
    word-wrap: break-word;
  }

  .page-size {
    margin: 15px 0px;
    display: flex;
    justify-content: flex-end;
    align-items: center;
  }
</style>