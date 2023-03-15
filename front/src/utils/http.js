import axios from 'axios';
import store from '@/vuex/store';
import { Message } from 'iview';
import Router from '@/router/index'

const http = axios.create({
  // baseURL: process.env.NODE_ENV === 'development' ? '' : '/api',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
  },
  transformRequest: [function (data) {
    let ret = ''
    for (let it in data) {
      ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
    }
    return ret
  }],
  baseURL: '/api',
  // baseURL: '',
  timeout: 5000
});

export const post = (data) => {
  const info = JSON.parse(localStorage.getItem('info'));
  console.log(info);
  data.method = 'POST';
  if (info) {
    data.headers = { 'token': info.data.token ,
      'Authorization': info.data.jwtTokenHead + info.data.jwtToken};
  }
  return http(data);
};

export const get = (data) => {
  const info = JSON.parse(localStorage.getItem('info'));
  // console.log('localStorage:', info);
  data.method = 'GET';
  if (info) {
    data.headers = { 'token': info.data.token ,
      'Authorization': info.data.jwtTokenHead + info.data.jwtToken};
  }
  return http(data);
};

export const m_delete = (data) => {
  const info = JSON.parse(localStorage.getItem('info'));
  // console.log('localStorage:', info);
  data.method = 'delete';
  if (info) {
    data.headers = { 'token': info.data.token ,
      'Authorization': info.data.jwtTokenHead + info.data.jwtToken};
  }
  return http(data);
};

export const update = (data) => {
  const info = JSON.parse(localStorage.getItem('info'));
  // data.method = 'POST';
  if (info) {
    data.headers = { 'token': info.data.token ,
      'Authorization': info.data.jwtTokenHead + info.data.jwtToken};
  }
  return http(data);
};

// 响应拦截器
http.interceptors.request.use(
  config => {
    // do something before request is sent
    if (store.getters.token) {
      // let each request carry token
      // ['X-Token'] is a custom headers key
      // please modify it according to the actual situation
      // config.headers['x-access-token'] = getToken();
    }
    return config;
  },
  error => {
    // do something with request error
    console.log(error);
    return Promise.reject(error);
  }
);

// response interceptor
http.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
   */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
   response => {
    const res = response.data;
    // if the custom code is not 20000, it is judged as an error.
    // {"code":{"code":-1,"msg":"库存不足,无法添加购车"},"data":null}
    if (res.code !== 200) {
      Message.error(res.message || 'Error');
      return Promise.reject(new Error(res.message || 'Error'));
    } else {
      return res;
    }
  },
  error => {
    // for debug
    const data = error.response.data
    console.log('err:' + data.message);
    Message.error(data.message || 'Error');
    if (error.response.status === 401) {
        localStorage.removeItem('info');
        store.state.userInfo = {};
        Router.replace('login');
    }
    return Promise.reject(error);
  }
);

export default http;
