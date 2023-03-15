<template>
  <div class="container">
    <nav-bar title="我的购物车" />
    <Layout class="layout" :style="{height: winHeight + 'px'}">
      <Sider class="side-bar" :style="{'display': showSideBar ? 'block' : 'none'}" ref="side" :collapsed-width="78">
        <Menu active-name="1-2" theme="light" width="auto" @on-select="onSelect">
          <div class="user-icon">
            <div class="user-img">
              <img src="static/img/head.png">
            </div>
            <!--<p>Gavin</p>-->
          </div>
          <Submenu name="1">
            <template slot="title">
                <Icon type="location"></Icon>
                <span>收货地址</span>
            </template>
            <MenuItem name="myAddress">我的收货地址</MenuItem>
            <MenuItem name="addAddress">添加收货地址</MenuItem>
          </Submenu>
          <Submenu name="2">
            <template slot="title">
                <Icon type="clipboard"></Icon>
                <span>购物订单</span>
            </template>
            <MenuItem name="myOrder">我的订单</MenuItem>
          </Submenu>
          <Submenu name="3">
            <template slot="title">
                <Icon type="ios-cart"></Icon>
                <span>购物车</span>
            </template>
            <MenuItem name="myShoppingCart">我的购物车</MenuItem>
          </Submenu>
          <Submenu name="4">
            <template slot="title">
              <Icon type="ios-cart"></Icon>
              <span>卡包</span>
            </template>
            <MenuItem name="myDiscount">我的优惠券</MenuItem>
          </Submenu>
        </Menu>
      </Sider>
      <router-view></router-view>
    </Layout>
    <footer-bar :active-index="3" />
  </div>
</template>

<script>
import footerBar from '@/components/footerBar'
import { IsPC } from '@/common/common.js'
import navBar from '@/components/navBar'
export default {
  name: 'Home',
  data () {
    return {
      activeTitle: '我的订单',
      bar: {
        'myAddress': '我的收货地址',
        'addAddress': '添加收货地址',
        'myOrder': '我的订单',
        'myShoppingCart': '我的购物车',
        'myDiscount': '我的优惠券'
      },
      showSideBar: true,
      winHeight:window.innerHeight,
    };
  },
  components: {
    footerBar,
    navBar
  },
  methods: {
    onSelect (name) {
      if(name === 'myShoppingCart') {
        this.$router.push(`/ShowShoppingCart`);
        return
      }
      this.activeTitle = this.bar[name];
      this.$router.push(`/home/${name}`);
      this.showSideBar = IsPC ? true : false
    }
  },
  watch:{
    $route(to,from){
      if(to.path === '/home'){
        this.showSideBar = true
      }
    }
  }
};
</script>

<style lang="less" scoped>
/deep/.side-bar{
  height: calc(100vh - 35px);
  background: #fff;
  overflow: auto;
}
.side-bar a{
  color: #232323;
}
.user-icon {
  height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.user-icon span {
  font-size: 96px;
}
.user-img {
  margin-bottom: 15px;
  width: 96px;
  height: 96px;
  border-radius: 48px;
  overflow: hidden;
}
.user-img img{
  width: 100%;
}
.layout-footer-center {
  padding: 0px 15px;
  padding-bottom: 15px;
  text-align: center;
}

.container{
  padding-top: 44px;
  padding-bottom: 40px;
}
@media (min-width: 992px) {
  /deep/.side-bar{
    margin-right: 20px;
  }
}

@media (max-width: 992px) {
  .container{
    padding-left: 0;
    padding-right: 0;
  }
  /deep/.side-bar{
    width: 100% !important;
    min-width: 100% !important;
  }
}


</style>
