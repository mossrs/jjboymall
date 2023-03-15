import {post, get, m_delete} from '@/utils/http';

// 添加购物车
export const addShoppingCart = (data) => {
  return post({
    url: '/cart/user_cart',
    data: data
  });
};

// 添加购物车
export const clearShoppingCart = () => {
  return post({
    url: '/cart/clear',
    data: {
    }
  });
};

// 移除购物车商品
export const removeCartItems = (data) => {
  return m_delete({
    url: '/cart/user_cart',
    data: data
  });
};

// 获取购物车信息
export const getShoppingCart = () => {
  return get({
    url: '/cart/user_cart'
  });
};

// 更新购物车商品
export const updateCartItem = (data) => {
  return post({
    url: '/cart/items/update',
    data: data
  });
};
