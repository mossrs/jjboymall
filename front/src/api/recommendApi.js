import {post} from '@/utils/http';

// 随便看看，商品推荐
export const recommendLookProduct = (data) => {
  return post({
    url: '/goods/goods_cart_recommend?relProductId=%s'.replace("%s", data),
    data: data
  });
};



