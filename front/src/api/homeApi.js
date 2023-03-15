import {get} from '@/utils/http';

// 首页数据查询
export const getHomeData = (data) => {
  return get({
    url: `/home/index`
  });
};

// 获取新品推荐
export const getNewProduct = (data) => {
  return get({
    url: '/index/home_new_product'
  });
};

// 获取人气搜索
export const getPopProduct = (data) => {
  return get({
    url: '/index/home_recommend_product'
  });
};

// 获取专题数据
export const getRecommendProduct = (data) => {
  return get({
    url: '/index/recommend_subject',  
  });
};
