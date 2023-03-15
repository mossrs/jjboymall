<template>
  <div>
    <div class="pay-done-box">
      <img src="static/img/pay-success.png">
      <!-- <p @click="skipToHome">支付成功，点击到我的主页查看</p> -->
      <Button type="success" @click="skipToHome" 
      size="large" class="submit-order">支付成功，点击到我的主页查看</Button>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import Footer from '@/components/footer/Footer';
export default {
  name: 'PayDone',
  components: {
    Footer
  },
  methods: {
    skipToHome () { // 跳转我的主页
      this.$router.push('/home')
    }
  },
};
</script>

<style scoped>
.pay-done-box {
  height: 600px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
p {
  text-align: center;
  line-height: 80px;
  font-size: 16px;
  color: rgb(155, 155, 155);
}
@media (max-width: 992px) {
  .pay-done-box img{
    display: block;
    width: 90%;
    transform: translate(5%);
  }
}
@media (min-width: 992px) {
  p{
    display: none;
  }
}
</style>
