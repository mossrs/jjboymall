<template>
  <div>
    <nav-bar title="支付" left-arrow></nav-bar>
    <div class="pay-container">
      <Alert show-icon>
        扫码支付
        <Icon type="qr-scanner" slot="icon"></Icon>
        <template slot="desc">请扫描右边二维码进行支付</template>
      </Alert>
      <div class="pay-box">
        <div class="pay-demo">
          <img src="static/img/pay/pay-demo.png">
        </div>
        <div class="pay-qr-scan">
          <img src="static/img/pay/pay-qrscan.png">
          <div class="pay-tips">
            <!-- <router-link to="/payDone"><p>点击我, 完成支付</p></router-link> -->
            <Button type="error" @click="finishPay" 
            size="large" class="submit-order">点击我, 完成支付</Button>
          </div>
        </div>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import Footer from '@/components/footer/Footer'
import navBar from '@/components/navBar'
import { mapActions } from 'vuex'
export default {
  name: 'Pay',
  data(){
    return{
      orderId : ''
    }
  },
  components: {
    Footer,
    navBar
  },
  created(){
    this.orderId = this.$route.query.orderId
  },
  methods:{
    ...mapActions([
        'finishOrder'
      ]),
    finishPay(){
      const data = {'orderId': this.orderId }
      this.finishOrder(data).then(data => {
          if (data) {
            this.$router.push('payDone')
          } else {
            this.$Message.error('超时，请重试')
          }
        })
    }
  }
};
</script>

<style scoped>
.pay-container {
  margin: 15px auto;
  width: 80%;
  min-width: 1000px;
}
.pay-box {
  height: 500px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.pay-demo {
  width: 50%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.pay-demo img{
  height: 80%;
}
.pay-qr-scan {
  width: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.pay-tips {
  width: 50%;
  text-align: center;
  font-size: 14px;
  line-height: 30px;
}
.pay-tips a {
  color: #999999;
}
</style>
<style lang="less" scoped>
@media (max-width: 992px) {
  .pay-container{
    min-width: 0;
    margin-top: 55px;
    .pay-box{
      flex-direction: column;
      .pay-tips{
        p {
          width: 150px;
          transform: translate(-23%);
        }
      }
    }
    .pay-demo{
      img{
        width: 80%;
        height: 80%;
        // transform: translate(0, -50%)
      }
    }
  }
}
</style>
