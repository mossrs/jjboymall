import {post, get} from '@/utils/http';

// 登录
export const login = (data) => {
  return post({
    url: '/user/login',
    method: 'POST',
    data: data
  });
};

// 用户退出
export const logout = (data) => {
  return post({
    url: '/user/loginOut',
    method: 'POST',
    data: data  
  });
};
// 注册
export const signUp = (user) => {
  return post({
    url: '/user/register',
    method: 'POST',
    data: user
  });
};

// 判断手机是否注册过
export const isExist = (data) => {
  return post({
    url: '/user/isExist',
    method: 'POST',
    data: {
      phone: data
    }
  });
};

// 发送验证码
export const sendSmsCode = (data) => {
  return get({
    url: '/user/sms',
    params:{
      phone:data
    }   
  });
};
// 校验 手机验证码
export const checkSmsCode = (data) => {
  return post({
    url: '/user/authorization',
    method: 'POST',
    data: data  
  });
};

// 获得验证码图片
export const getPicBase64 = () => {
  return get({
    url: '/admin/getPic?t=' + Math.random()
  });
};

// 查找商品
export const goodsList = (data, pageNum, pageSize) => {
  let param = '';
  var page = data.pageNum || 1;
  var num = data.pageSize || 30;
  if(data.pageNum) page = data.pageNum
  param += `page=${page}&size=${num}`;
  console.log(param);
  return post({
    url: `/goods/goods_list?${param}`,
    method: 'POST',
    data: data
  });
};

export const searchProduct = (data, pageNum, pageSize) =>{
  let param = '';
  var page = pageNum  || 0;
  var num = pageSize || 16;
  if(data.pageNum) page = data.pageNum
  if(data.key) param += `key=${data.key}&`;
  if (data.value) param += `value=${data.value}&`;
  param += `page=${page}&pageSize=${num}`;
  console.log(param);
  return post({
    url: `/pms/product/findByCondition?${param}`,
    method: 'POST',
    data: {
      productName: 'Fred',
      relCategory1Id: 1
    }
  })
}

// 根据商品ID 查询商品
export const getOneGoods = (id) => {
  return get({
    url: `/goods/good_detail`,
    method: 'GET',
    params: {
      good_id: id
    }
  });
};

// 获取规格树
export const categoryList = () => {
  return get({
    url: '/index/category'
  });
};

// 根据条件查询SKU商品
export const getSkuGoods = (data) => {
  return post({
    url: '/goods/good_sku_detail',
    method: 'POST',
    data: data
  });
};

// 查询商品分类
export const getSearchCondition = (data) => {
  return post({
    url: '/goods/goods_specification',
    method: 'POST',
    data: data
  });
};
