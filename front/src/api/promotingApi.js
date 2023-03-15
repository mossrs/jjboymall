import {get} from '@/utils/http';

// 获取优惠券列表
export const getCouponListByCategoryIds = (data) => {
  return get({
    url: `/coupon/user_coupon`,
    params: {
      productCategoryIdsS: data
    }
  });
};
