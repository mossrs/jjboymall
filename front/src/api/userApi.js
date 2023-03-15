import {post, get, update} from '@/utils/http';

// 添加收货地址
export const addAddress = (data) => {
  return post({
    url: '/address/user_address',
    data: data,
  });
};

// 获取收货地址
export const getAddressList = (data) => {
  console.log(data);
  return get({
    url: '/address/user_address?username='+data,
  });
};

// 删除地址
export const delAddress = (data) => {
  return update({
    url: '/address/user_address?id='+data,
    method: 'DELETE'
  });
};

// 修改地址
export const editAddress = (data) => {
  return update({
    url: '/address/user_address',
    data:  data,
    method: 'put'
  });
};

// 生成订单
export const addOrder = (data) => {
  return post({
    url: '/order/shopping_order',
    data: data
  });
};

// 获取订单
export const getOrder = (pageDto) => {
  console.log(pageDto);
  return get({
    url: '/order/shopping_order_list?pageIndex=' 
    + pageDto.pageIndex + "&pageSize=" + pageDto.pageSize
  });
};

// 完成订单支付
export const finishOrder = (data) => {
  return update({
    url: '/order/shopping_order',
    data:  data,
    method: 'put'
  });
};

// 获取订单
export const getOrderItems = (data) => {
  console.log('订单详情的订单编号' + data);
  return get({
    url: '/order/shopping_order?orderNumber=' + data.orderNumber
  });
};
// 退款
export const refund = (data) => {
  console.log('退款订单的订单编号');
  console.log(data);
  return post({
    url: '/oms/orderRefund/orderRefund',
    data: data
  });
};
// 促销活动
export const getPromotion = (data) => {
  return get({
    url: '/goods/good_fullReduction',
    params: {
      good_id: data
    }
  });
};
// 优惠券活动
export const getDiscount = (data) => {
  return get({
    url: '/coupon/goods_coupon?productCategoryId=' + data.productCategoryId + '&spuId=' + data.spuId
  });
};
// 领取优惠券
export const receiveReduction = (data) => {
  console.log("请求请求 ---------------" +data)
  return post({
    url: '/coupon/user_coupon?couponId='+data
  })
};
// 我的优惠券
export const getMyDiscount = () => {
  return get({
    url: '/coupon/user_coupon'
  })
}

