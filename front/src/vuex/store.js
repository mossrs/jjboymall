import Vue from 'vue';
import Vuex from 'vuex';
import * as actions from './actions';
import * as mutations from './mutations';
import * as getters from './getters';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    isLoading: false, // 是否展示loading动画
    orderBy: 'sale', // 根据什么字段排序
    goodsInfoByName: [], // 根据商品名称的列表
    goodsDetail: {}, // 商品详情
    skuGoodsDetail: {}, // SKU商品详情
    goodsInfoByMerchanrtId: [], // 商户热卖商品
    categoryList: [], // 规格列表
    userInfo: {}, // 用户信息
    picBase64: '', // 图片的base64编码串
    signUpStep: 0, // 登陆步骤
    totalGoodNum: 0, // 搜索条件下，所以商品总页数
    marketing: { // 营销
      CarouselItems: [], // 轮播图
      activity: [] // 活动
    },
    order: [], // 订单信息
    orderTotal: 0, // 订单信息的总条数
    orderItems: {}, // 订单详情
    seckills: { // 秒杀
      deadline: {
        hours: 0,
        minute: 0,
        seconds: 0
      },
      goodsList: []
    },
    news: [], // 新品推荐
    popRecommends: [], // 人气商品推荐
    recommendSubjects: [], // 专题推荐
    computer: {}, // 电脑专栏
    eat: {}, // 爱吃专栏
    asItems: [], // 广告
    goodsList: [], // 商品列表
    shoppingCart: [], // 购物车
    newShoppingCart: [], // 刚加入的购物车，作为展示
    recommend: [], // 推荐购买,可能还需要
    address: [{
      address_id: 1,
      name: '马士兵教育北京总公司1',
      province: '北京市',
      city: '北京市',
      address: '海淀区文教园A座117',
      phone: '17611111111',
      postalcode: '300457'
    }],
    // 商品列表查询条件
    searchConditionData: [],
    // 选中的查询规格项
    selectedCondtions: [],
    addr: {},
    // 立即购买
    atOnceByGoods: [],
    // 被选中的购物车列表
    selectedCartItems: [],
    // 被选中的购物车信息
    selectedCartInfo: {
      discountAmount: 0.00,
      selectedCartItems: []
    },
    // 优惠券列表
    couponList: [{
      productCategoryId: 0,
      productCategoryName: '',
      coupons: []
    }],
    // 优惠券活动
    discount: [],
    // 促销活动
    promotion: [],
    // 我的优惠券
    myDiscount: []
  },
  getters,
  actions,
  mutations
});
