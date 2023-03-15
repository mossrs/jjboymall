import * as tempData from '@/data/tempData';

// 字段排序函数
const compare = property => {
  return function (a, b) {
    var value1 = a[property];
    var value2 = b[property];
    return value1 - value2;
  };
};

// 获取排序后的列表
export const goodsInfoByNameFilter = state => {
  const goodsList = [];
  for (const item of state.goodsInfoByName) {
    console.log(item.basicPrice);
    const temp = {
      goodsId: item.id,
      relCategory3Id: item.relCategory3Id,
      goodsName: item.goodsName.substring(0, 39) + '...',
      merchantName: '马士兵商铺',
      merchantId: 1,
      goodsImgs: item.goodsImgs.split(',')[0],
      price: item.basicPrice,
      salesNum: item.salesNum
    };
    goodsList.push(temp);
  }
  return goodsList || [];
};

// 获取商品侧边广告栏
export const merchantItem = state => {
  if (state.goodsInfoByMerchanrtId.length <= 0) return [];
  const all = state.goodsInfoByMerchanrtId;
  const asItem = [];
  for (let i = 0; i < all.length; i++) {
    const temp = {
      goodsId: all[i].id,
      goodsName: all[i].product_name.substring(0, 30) + '...',
      relCategory3Id: all[i].rel_category3_id,
      merchantName: 'MaShiBing',//all[i].tenantName,
      merchantId: all[i].relTenantId,
      img: all[i].default_pic,
      price: all[i].price,
      sale: all[i].sales_num
    };
    asItem.push(temp);
  }
  return asItem || [];
};

export const getTotalGoodNum = state => {
  return state.totalGoodNum;
}

// 商家侧边栏
export const asItem = state => {
  if (state.goodsInfoByName.length <= 0) return [];
  const asAll = state.goodsInfoByName.sort(compare('salesNum'));
  const asItem = [];
  const len = asAll.length>5 ? 5 : asAll.length 
  for (let i = 0; i < len; i++) {
    console.log('asas', asAll[i])
    const temp = {
      goodsId: asAll[i].id,
      relCategory3Id: asAll[i].relCategory3Id,
      goodsName: asAll[i].goodsName.substring(0, 30) + '...',
      merchantName: '马士兵商铺',
      merchantId: 1,
      goodsImgs: asAll[i].goodsImgs.split(',')[0],
      price: asAll[i].basicPrice,
      salesNum: asAll[i].salesNum
    };
    asItem.push(temp);
  }
  return asItem || [];
};

// 获取商品详情基础展示
export const getGoodsDetailBase = state => {
  const goodsImgs = state.goodsDetail.album_pics ? state.goodsDetail.album_pics.split(',') : [];
  const data = {
    goodsImgs: goodsImgs,
    goodsId: state.goodsDetail.id || 0,
    merchantId: state.goodsDetail.relTenantId,
    title: state.skuGoodsDetail.title || state.goodsDetail.productName,
    productNo: state.goodsDetail.productNo,
    price: state.skuGoodsDetail.price || state.goodsDetail.price,
    specList: state.goodsDetail.specList,
    salesNum: state.goodsDetail.sales_num,
    skuList: state.goodsDetail.skuList,
    // 暂无...
    // 商品标签
    tags: ['满69-20元', '关注产品★送钢化膜', '配次日达'],
    // 商品折扣 TODO 领券
    // discount: ['满148减10', '满218减20', '满288减30'],
    // 促销 TODO 促销活动
    // promotion: ['跨店满减', '多买优惠']
  };
  return data;
};

// 获取商品详情
export const getGoodsDetail = state => {
  const data = {
    specList: state.goodsDetail.skuList[0].specTypeList || [],
    detailDesc: state.goodsDetail.detail_desc,
    // 暂时以多图逗号分割处理
    detailHtml: state.goodsDetail.album_pics.split(','),
    // 模拟数据
    remarks: tempData.tempRemarks
  };
  return data;
};

// 获取SKU商品详情
export const getSkuGoodsDetail = state => {
  const data = {
    specList: state.skuGoodsDetail.specTypeList || [],
    sellPoint: state.skuGoodsDetail.sellPoint,
    price: state.skuGoodsDetail.price,
    productNo: state.skuGoodsDetail.productNo,
    skuNo: state.skuGoodsDetail.sku_no,
    num: state.skuGoodsDetail.num
  };
  return data;
};

// 获取热卖商品
export const getHot = state => {
  // const data = {
  //   specList: state.skuGoodsDetail.specTypeList || [],
  //   sellPoint: state.skuGoodsDetail.sellPoint,
  //   price: state.skuGoodsDetail.price,
  //   productNo: state.skuGoodsDetail.productNo,
  //   skuNo: state.skuGoodsDetail.skuNo
  // };
  const data = [
    {
      img: 'static/img/goodsDetail/hot/1.jpg',
      price: 28.0,
      sale: 165076
    },
    {
      img: 'static/img/goodsDetail/hot/2.jpg',
      price: 36.0,
      sale: 135078
    },
    {
      img: 'static/img/goodsDetail/hot/3.jpg',
      price: 38.0,
      sale: 105073
    },
    {
      img: 'static/img/goodsDetail/hot/4.jpg',
      price: 39.0,
      sale: 95079
    },
    {
      img: 'static/img/goodsDetail/hot/5.jpg',
      price: 25.0,
      sale: 5077
    },
    {
      img: 'static/img/goodsDetail/hot/6.jpg',
      price: 20.0,
      sale: 3077
    }
  ];
  return data;
};

// 获取秒杀的小时
export const seckillsHours = state => {
  return state.seckills.deadline.hours < 10 ? '0' + state.seckills.deadline.hours : state.seckills.deadline.hours;
};

// 获取秒杀的分钟
export const seckillsMinutes = state => {
  return state.seckills.deadline.minute < 10 ? '0' + state.seckills.deadline.minute : state.seckills.deadline.minute;
};

// 获取秒杀的秒
export const seckillsSeconds = state => {
  return state.seckills.deadline.seconds < 10 ? `0${state.seckills.deadline.seconds}` : state.seckills.deadline.seconds;
};

// 获取收货地址
export const getAddress = state => {
  return state.address;
};

// 获取订单
export const getOrder = state =>{
  return state.order;
};

// 获取订单详情
export const getOrderItems = state =>{
  return state.orderItems;
};

// 获取规格树
export const getterCategoryList = state => {
  return state.categoryList;
};
// 是否登录
export const isLogin = state => {
  if (state.userInfo.data === undefined || state.userInfo.data === '') {
    return false;
  }
  return true;
};

// 获取选中的查询规格条件
export const getterSelectedCondtions = state => {
  return state.selectedCondtions;
};
// 促销活动
export  const  getPromotionList = state => {
  return state.promotion;
};
// 优惠券活动
export  const  getDiscountList = state => {
  return state.discount;
};
// 我的优惠券
export  const  getMyDiscountList = state => {
  if(!state.myDiscount.code)
  {
    state.myDiscount.forEach(element => {
      // const date = String(element.end_time)
      var date = new Date(element.end_time)
      var result = date.getFullYear() + "-"+ 
      ("0" + (date.getMonth() + 1)).slice(-2)
       +"-"+ ("0" + date.getDate()).slice(-2)
  
      // const reg=/^(\d{4})(\d{2})(\d{2})$/;
      // const str = date.replace(reg,"$1-$2-$3");
      
      element.end_time = result
    });
    return state.myDiscount
  }else
  {
    return null
  }
}


