import {get, post} from '@/utils/http';

// 店铺热销商品
export const getMerchantHotsales = (data) => {
  return get({
    url: '/goods/merchant_hotsales',
    params: {
      merchant_id: data
    }
  });
};

// 获取优惠价格信息
export const getPreferentialPrice = (data) => {
  return post({
    url: `/goods/goods_cart_sku_detail`,
    data: data
  });
};
