<template>
<Layout class="layout">
  <nav-bar title="我的优惠券" />
  <Content class="content">
    <transition mode="out-in">
       <div>
        <div class="address-box" v-for="(item, index) in getMyDiscountList" :key="index">
          <div class="address-content">
            <p>
              <span class="address-content-title" style="font-size: large; color: #2d8cf0">¥{{item.amount}}</span>
              <span class="address-content-title" v-if="item.type == 0" style="font-size: small; color: #2d8cf0">全场赠券</span>
              <span class="address-content-title" v-if="item.type == 1" style="font-size: small; color: #2d8cf0">会员赠券</span>
              <span class="address-content-title" v-if="item.type == 2" style="font-size: small; color: #2d8cf0">购物赠券</span>
              <span class="address-content-title" v-if="item.type == 3" style="font-size: small; color: #2d8cf0">注册赠券</span>
            </p>
            <p><span class="address-content-title">满{{item.min_point}}减{{item.amount}}</span></p>
            <p><span class="address-content-title">仅可购买马士兵商铺官方</span></p>
            <p><span class="address-content-title">有效期至{{item.end_time}}</span></p>
          </div>
        </div>
      </div>
    </transition>
  </Content>
  <Footer class="layout-footer-center">2018 &copy; Gavin</Footer>
</Layout>
</template>

<script>
import store from '@/vuex/store';
import { mapActions, mapGetters } from 'vuex';
import navBar from '@/components/navBar'
export default {
  name: 'MyDiscount',
  data () {
    return {

    };
  },
  created () {
    this.getMyDiscount()
  },
  computed: {
    ...mapGetters(['getMyDiscountList'])
  },
  methods: {
    ...mapActions(['getMyDiscount']),
  },
  components: {
    navBar
  },
  store
};
</script>

<style scoped>
.layout{
  /* padding-top: 44px; */
}
.address-box {
  padding: 15px;
  margin: 15px;
  border-radius: 30px;
  box-shadow: 0px 0px 5px #ccc;
  border-right: 20px;
}
.address-header {
  height: 35px;
  display: flex;
  justify-content: space-between;
  color: #232323;
  font-size: 18px;
}
.address-content {
  font-size: 14px;
}
.address-content-title {
  color: #999;
}
.address-action span{
  margin-left: 15px;
  font-size: 14px;
  color: #2d8cf0;
  cursor: pointer;
}
.content {
  /* margin: 15px; */
  background-color: #fff;
  padding: 15px;
}
.layout-footer-center {
  padding: 0px 15px;
  padding-bottom: 15px;
  text-align: center;
}
</style>
