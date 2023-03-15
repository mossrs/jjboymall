import Vue from 'vue'
import Router from 'vue-router'
import CheckPhone from '@/views/signUp/signForm/CheckPhone'
import InputInfo from '@/views/signUp/signForm/InputInfo'
import SignUpDone from '@/views/signUp/signForm/SignUpDone'
import Freeback from '@/components/Freeback'
import Home from '@/components/Home'
import MyAddress from '@/components/home/MyAddress'
import AddAddress from '@/components/home/AddAddress'
import MyOrder from '@/components/home/MyOrder'
import OrderItems from '@/components/home/OrderItems'
import MyShoppingCart from '@/components/home/MyShoppingCart'
import Merchant from '@/components/Merchant'
import ApplyText from '@/components/ApplyText'

import MyDiscount from '@/components/home/MyDiscount'
// 解决不允许跳转当前路由
const originalPush = Router.prototype.push
Router.prototype.push = function push (location) {
  return originalPush.call(this, location).catch(err => err)
}

Vue.use(Router)
export default new Router({
  // 开启History模式
  mode: process.env.NODE_ENV === 'production' ? 'history' : 'hash',
  routes: [
    {
      path: '/', // 首页
      name: 'Index',
      component: () => import('@/views/index')
    },
    {
      path: '/category', // 分类
      name: 'Category',
      component: () => import('@/views/category')
    },
    {
      path: '/Login', // 登陆
      name: 'Login',
      component: () => import('@/views/login/Login')
    },
    {
      path: '/SignUp', // 注册
      name: 'SignUp',
      component: () => import('@/views/signUp'),
      children: [
        {
          path: '/',
          name: 'index',
          component: CheckPhone
        },
        {
          path: 'checkPhone',
          name: 'CheckPhone',
          component: CheckPhone
        },
        {
          path: 'inputInfo',
          name: 'InputInfo',
          component: InputInfo
        },
        {
          path: 'signUpDone',
          name: 'SignUpDone',
          component: SignUpDone
        }
      ]
    },
    {
      path: '/goodsList', // 商品列表
      name: 'GoodsList',
      component: () => import('@/views/goodsList')
    },
    {
      path: '/goodsDetail', // 商品详情
      name: 'GoodsDetail',
      component: () => import('@/views/goodsDetail')
    },
    {
      path: '/shoppingCart', // 商品详情
      name: 'ShoppingCart',
      component: () => import('@/views/shoppingCart')
    },
    {
      path: '/order', // 订单页面
      name: 'Order',
      component: () => import('@/views/cart')
    },
    {
      path: '/applyText', // 支付宝跳转支付页面
      name: 'ApplyText',
      component: ApplyText
    },
    {
      path: '/pay', // 支付页面
      name: 'Pay',
      component: () => import('@/views/pay')
    },
    {
      path: '/payDone', // 支付成功页面
      name: 'PayDone',
      component: () => import('@/views/pay/payDone')
    },
    {
      path: '/freeback', // 反馈页面
      name: 'Freeback',
      component: Freeback
    },
    {
      path: '/home', // 主页
      name: 'Home',
      component: Home,
      children: [
        {
          path: '/',
          name: 'index',
          component: MyOrder
        },
        {
          path: 'myAddress',
          name: 'MyAddress',
          component: MyAddress
        },
        {
          path: 'addAddress',
          name: 'AddAddress',
          component: AddAddress
        },
        {
          path: 'myOrder',
          name: 'MyOrder',
          component: MyOrder
        },
        {
          path: 'orderItems',
          name: 'OrderItems',
          component: OrderItems
        },
        {
          path: 'myShoppingCart',
          name: 'MyShoppingCart',
          component:  () => import('@/views/cart')
        },
        {
          path: 'myDiscount',
          name: 'MyDiscount',
          component: MyDiscount
        }
      ]
    },
    {
      path: '/merchant',
      name: 'Merchant',
      component: Merchant
    },
    {
      path: '/showShoppingCart',
      name: 'ShowShoppingCart',
      component: () => import('@/views/cart')
    },
    {
      path: '/PayOrder',
      name: 'PayOrder',
      component: () => import('@/views/payOrder')
    }
  ]
})
