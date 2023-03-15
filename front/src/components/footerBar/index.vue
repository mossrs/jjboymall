<template>
  <ul class="footer-nav-list hidden-lg hidden-md">
    <li class="footer-nav-item" v-for="(item, index) in navList" :key="item.index">
      <router-link :to="item.path">
        <img
          class="footer-nav-item-icon"
          :src="index === activeIndex ? item.activeIcon : item.icon"
        />
      </router-link>
    </li>
  </ul>
</template>

<script>
import indexIcon from '@img/navBar/index.png'
import indexActiveIcon from '@img/navBar/indexActive.png'
import categoryIcon from '@img/navBar/category.png'
import categoryActiveIcon from '@img/navBar/categoryActive.png'
import cartIcon from '@img/navBar/cart.png'
import cartActiveIcon from '@img/navBar/cartActive.png'
import loginIcon from '@img/navBar/login.png'
import userIcon from '@img/navBar/user.png'
import userActiveIcon from '@img/navBar/userActive.png'
import { mapState } from 'vuex'
export default {
  props: {
    activeIndex: Number
  },
  data() {
    return {}
  },
  computed: {
    ...mapState(['userInfo']),
    navList() {
      const navList = [
        {
          icon: indexIcon,
          activeIcon: indexActiveIcon,
          path: '/',
          title: '首页'
        },
        {
          icon: categoryIcon,
          activeIcon: categoryActiveIcon,
          path: '/category',
          title: '分类'
        },
        {
          icon: cartIcon,
          activeIcon: cartActiveIcon,
          path: '/ShowShoppingCart',
          title: '购物车'
        }
      ]
      if (this.userInfo.data) {
        return [
          ...navList,
          {
            icon: userIcon,
            activeIcon: userActiveIcon,
            path: '/home',
            title: '我的'
          }
        ]
      } else {
        return [
          ...navList,
          {
            icon: loginIcon,
            activeIcon: loginIcon,
            path: '/login',
            title: '登录'
          }
        ]
      }
    }
  }
}
</script>

<style lang="less" scoped>
.footer-nav-list {
  display: flex;
  position: fixed;
  height: 50px;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 31;
  width: 100vw;
  list-style: none;
  background-color: #fff;
  font-size: 16px;
  justify-content: space-around;
  box-shadow: 0 0 10px 0 hsla(0, 6%, 58%, 0.6);
  align-items: center;
  .footer-nav-item {
    &-icon {
      height: 45px;
    }
  }
}
</style>
