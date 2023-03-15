import * as baseApi from '@/api/baseApi'
import * as userApi from '@/api/userApi'
import * as cartApi from '@/api/cartApi'
import * as goodsApi from '@/api/goodsApi'
import * as tempData from '@/data/tempData'
import * as homeApi from '@/api/homeApi'
import * as promotingApi from '@/api/promotingApi'
import * as recommendApi from '@/api/recommendApi'


function sliceArray (array, size) {
  var result = []
  for (var x = 0; x < Math.ceil(array.length / size); x++) {
    var start = x * size
    var end = start + size
    result.push(array.slice(start, end))
  }
  return result
}

// 获取用户推荐
export const loadRecommend = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    recommendApi.recommendLookProduct(data.categoryId).then(res => {
      if (res.code === 200) {
        let infoList = res.data
        let length = infoList.length
        let dataList = sliceArray(infoList, length / 2)
        commit('SET_RECOMMEND_INFO', dataList)
      } else {
        resolve(false)
      }
    })

  })
}

// 获取优惠券列表信息
export const getCouponListByCategoryIds = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    promotingApi.getCouponListByCategoryIds(data).then(res => {
      const data = res.data
      commit('SET_COUPONLIST_INFO', data)
      resolve(data)
    }).catch(error => {
      reject(error)
    })
  })
}

// 购物车页面初步获取优惠价格信息
export const getPreferentialPrice = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    goodsApi.getPreferentialPrice(data).then(res => {
      const data = res.data
      // TODO 设置购物车优惠价
      resolve(data)
    }).catch(error => {
      reject(error)
    })
  })
}

// 查询首页数据
export const loadHomeData = ({ commit }) => {
  return new Promise((resolve, reject) => {
    homeApi.getHomeData().then(res => {
      if (res.code === 200) {
        const data = res.data
        commit('SET_NEWS_INFO', data.newProducts)
        commit('SET_POPRECOMMENDS_INFO', data.recommendProducts)
        commit('SET_RECOMMENDSUBJECTS_INFO', data.recommendSubjects)
        resolve(true)
      } else {
        resolve(false)
      }
    })
  })
}

// 登录
// 登录完成之后，将用户信息以及token写入本地缓存 TODO 可优化
export const login = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    baseApi.login(data).then(res => {
      const data = res.data
      commit('SET_USER_LOGIN_INFO', data)
      resolve(true)
    }).catch(error => {
      reject(error)
    })
  })
}

// 退出
export const logout = ({ commit }) => {
  return new Promise((resolve, reject) => {
    baseApi.logout().then(res => {
      if (res.data) {
        commit('SIGN_OUT_USER')
      }
    }).catch(error => {
      reject(error)
    })
  })
}

// 判断手机是否存在
export const isExist = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    baseApi.isExist(data).then(res => {   
      resolve(res)
    })
  })
}

// 发送验证码
export const sendSmsCode = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    baseApi.sendSmsCode(data).then(res => {
      const data = res.data
      resolve(data)
    }).catch(error => {
      reject(error)
    })
  })
}
// 校验 验证码
export const checkSmsCode = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    baseApi.checkSmsCode(data).then(res => {
      const data = res.data
      resolve(data)
    }).catch(error => {
      reject(error)
    })
  })
}

// 获得验证码图片
export const getPicBase64 = ({ commit }) => {
  return new Promise((resolve, reject) => {
    baseApi.getPicBase64().then(res => {
      if (res.code === 200) {
        let str = 'data:image/jpeg;base64,' + res.data
        commit('PIC_BASE64_STR', str)
        resolve(str)
      } else {
        resolve('')
      }
    })
  })
}

// 注册
export const signUp = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    baseApi.signUp(data).then(res => {
      if (res.code === 200) {
        resolve(true)
      } else {
        resolve(false)
      }
    })
  })
}

// 判断登陆有没有过期
export const isExp = () => {
  return new Promise((resolve, reject) => {
    let info = localStorage.getItem('info')
    if (!info) {
      resolve(false)
      return
    }
    info = JSON.parse(info)
    const now = new Date().getTime()
    if (info.exp > now) {
      resolve(true)
      return
    }
    resolve(false)
    return false
  })
}

// 获取秒杀数据
export const loadSeckillsInfo = ({ commit }) => {
  return new Promise((resolve, reject) => {
    const data = [
      {
        intro: '【赠小风扇】维他 柠檬茶250ml*32盒 礼品装 整箱',
        img: 'static/img/index/seckill/seckill-item1.jpg',
        price: 71.9,
        realPrice: 89.6
      },
      {
        intro: 'Kindle Paperwhite 全新升级版6英寸护眼非反光电子墨水',
        img: 'static/img/index/seckill/seckill-item2.jpg',
        price: 989.0,
        realPrice: 1299.0
      },
      {
        intro: '粮悦 大吃兄糯米锅巴 安徽特产锅巴糯米原味400g*2盒',
        img: 'static/img/index/seckill/seckill-item3.jpg',
        price: 21.8,
        realPrice: 49.0
      },
      {
        intro: '【京东超市】清风（APP）抽纸 原木纯品金装系列 3层',
        img: 'static/img/index/seckill/seckill-item4.jpg',
        price: 49.9,
        realPrice: 59.0
      },
      {
        intro: 'NIKE耐克 男子休闲鞋 AIR MAX 90 ESSENTIAL 气垫',
        img: 'static/img/index/seckill/seckill-item5.jpg',
        price: 559.9,
        realPrice: 759.9
      }
    ]
    const date = new Date()
    const hours = date.getHours()
    const minute = date.getMinutes()
    const seconds = date.getSeconds()
    console.log([hours, minute, seconds])
    // 距离开始秒杀时间
    const deadline = {
      hours: 1,
      minute: 38,
      seconds: 36
    }
    commit('SET_SECKILLS_INFO', [data, deadline])
  })
}

// 获取轮播(营销)图片
export const loadCarouselItems = ({ commit }) => {
  return new Promise((resolve, reject) => {
    const data = {
      carouselItems: [
        'static/img/nav/1.jpg',
        'static/img/nav/2.jpg',
        'static/img/nav/3.jpg',
        'static/img/nav/4.jpg',
        'static/img/nav/5.jpg'
      ],
      activity: [
        'static/img/nav/nav_showimg1.jpg',
        'static/img/nav/nav_showimg2.jpg'
      ]
    }
    commit('SET_CAROUSELITEMS_INFO', data)
  })
}

// 加载电脑专栏数据
export const loadComputer = ({ commit }) => {
  return new Promise((resolve, reject) => {
    const computer = {
      title: '电脑数码',
      link: ['电脑馆', '游戏极品', '装机大师', '职场焕新', '女神频道', '虚拟现实', '二合一平板', '电子教育', '万物周刊'],
      detail: [
        {
          bigImg: 'static/img/index/computer/item-computer-1.jpg',
          itemFour: [
            {
              title: '电脑馆',
              intro: '笔记本999元限量秒！',
              img: 'static/img/index/computer/item-computer-2.jpg'
            },
            {
              title: '外设装备',
              intro: '1000减618',
              img: 'static/img/index/computer/item-computer-1-3.jpg'
            },
            {
              title: '电脑配件',
              intro: '联合满减最高省618',
              img: 'static/img/index/computer/item-computer-1-4.jpg'
            },
            {
              title: '办公生活',
              intro: '5折神券 精品文具',
              img: 'static/img/index/computer/item-computer-1-5.jpg'
            },
            {
              title: '电脑馆',
              intro: '笔记本999元限量秒！',
              img: 'static/img/index/computer/item-computer-2.jpg'
            },
            {
              title: '外设装备',
              intro: '1000减618',
              img: 'static/img/index/computer/item-computer-1-3.jpg'
            },
            {
              title: '电脑配件',
              intro: '联合满减最高省618',
              img: 'static/img/index/computer/item-computer-1-4.jpg'
            },
            {
              title: '办公生活',
              intro: '5折神券 精品文具',
              img: 'static/img/index/computer/item-computer-1-5.jpg'
            }
          ],
          itemContent: [
            'static/img/index/computer/item-computer-1-6.jpg',
            'static/img/index/computer/item-computer-1-7.jpg',
            'static/img/index/computer/item-computer-1-8.jpg',
            'static/img/index/computer/item-computer-1-6.jpg',
            'static/img/index/computer/item-computer-1-7.jpg'
          ]
        }
      ]
    }
    commit('SET_COMPUTER_INFO', computer)
  })
}

// 加载新产品列表
export const loadNews = ({ commit }) => {
  return new Promise((resolve, reject) => {
    homeApi.getNewProduct().then((data)=>{
      console.log('返回新产品:',data)
      commit('SET_NEWS_INFO', data.data)
    }).catch((err)=>{

    })
  })
}

// 加载人气推荐商品
export const loadPopRecommends = ({ commit }) => {
  return new Promise((resolve, reject) => {
    homeApi.getPopProduct().then((data)=>{
      console.log('获取人气商品')
      console.log('返回新产品:',data)
      commit('SET_POPRECOMMENDS_INFO', data.data)
      // popRecommends
    }).catch((err)=>{

    })
  })
}

// 加载主题推荐
export const loadRecommendSubjects = ({ commit }) => {
  return new Promise((resolve, reject) => {
    homeApi.getRecommendProduct().then((data)=>{
      console.log('获取专题')
      for (var key in data.data)
      { 
        data.data[key].hotWordList = data.data[key].hot_words.split(',')
        data.data[key].albumPicList = data.data[key].album_pics.split(',')
      }
      commit('SET_RECOMMENDSUBJECTS_INFO', data.data)
      // popRecommends
    }).catch((err)=>{

    })
  })
}

// 加载爱吃专栏数据
export const loadEat = ({ commit }) => {
  return new Promise((resolve, reject) => {
    const eat = {
      title: '爱吃',
      link: ['休闲零食', '坚果', '牛奶', '饮料冲调', '食用油', '大米', '白酒', '红酒', '烧烤食材', '牛排', '樱桃'],
      detail: [
        {
          bigImg: 'static/img/index/eat/item-eat-1-1.jpg',
          itemFour: [
            {
              title: '粮油调味',
              intro: '买2免1',
              img: 'static/img/index/eat/item-eat-1-2.jpg'
            },
            {
              title: '饮料冲调',
              intro: '第二件半价',
              img: 'static/img/index/eat/item-eat-1-3.jpg'
            },
            {
              title: '休闲零食',
              intro: '满99减40',
              img: 'static/img/index/eat/item-eat-1-4.jpg'
            },
            {
              title: '中外名酒',
              intro: '满199减100',
              img: 'static/img/index/eat/item-eat-1-5.jpg'
            }
          ],
          itemContent: [
            'static/img/index/eat/item-eat-1-6.jpg',
            'static/img/index/eat/item-eat-1-7.jpg',
            'static/img/index/eat/item-eat-1-8.jpg'
          ]
        },
        {
          bigImg: 'static/img/index/eat/item-eat-2-1.jpg',
          itemFour: [
            {
              title: '东家菜',
              intro: '丰富好味',
              img: 'static/img/index/eat/item-eat-2-2.jpg'
            },
            {
              title: '东家菜',
              intro: '丰富好味',
              img: 'static/img/index/eat/item-eat-2-2.jpg'
            },
            {
              title: '东家菜',
              intro: '丰富好味',
              img: 'static/img/index/eat/item-eat-2-2.jpg'
            },
            {
              title: '东家菜',
              intro: '丰富好味',
              img: 'static/img/index/eat/item-eat-2-2.jpg'
            }
          ],
          itemContent: [
            'static/img/index/eat/item-eat-2-6.jpg',
            'static/img/index/eat/item-eat-2-7.jpg',
            'static/img/index/eat/item-eat-2-8.jpg'
          ]
        },
        {
          bigImg: 'static/img/index/eat/item-eat-2-1.jpg',
          itemFour: [
            {
              title: '东家菜',
              intro: '丰富好味',
              img: 'static/img/index/eat/item-eat-2-2.jpg'
            },
            {
              title: '东家菜',
              intro: '丰富好味',
              img: 'static/img/index/eat/item-eat-2-2.jpg'
            },
            {
              title: '东家菜',
              intro: '丰富好味',
              img: 'static/img/index/eat/item-eat-2-2.jpg'
            },
            {
              title: '东家菜',
              intro: '丰富好味',
              img: 'static/img/index/eat/item-eat-2-2.jpg'
            }
          ],
          itemContent: [
            'static/img/index/eat/item-eat-2-6.jpg',
            'static/img/index/eat/item-eat-2-7.jpg',
            'static/img/index/eat/item-eat-2-8.jpg'
          ]
        },
        {
          bigImg: 'static/img/index/eat/item-eat-2-1.jpg',
          itemFour: [
            {
              title: '东家菜',
              intro: '丰富好味',
              img: 'static/img/index/eat/item-eat-2-2.jpg'
            },
            {
              title: '东家菜',
              intro: '丰富好味',
              img: 'static/img/index/eat/item-eat-2-2.jpg'
            },
            {
              title: '东家菜',
              intro: '丰富好味',
              img: 'static/img/index/eat/item-eat-2-2.jpg'
            },
            {
              title: '东家菜',
              intro: '丰富好味',
              img: 'static/img/index/eat/item-eat-2-2.jpg'
            }
          ],
          itemContent: [
            'static/img/index/eat/item-eat-2-6.jpg',
            'static/img/index/eat/item-eat-2-7.jpg',
            'static/img/index/eat/item-eat-2-8.jpg'
          ]
        }
      ]
    }
    commit('SET_EAT_INFO', eat)
  })
}

// 请求获得商品详细信息，根据商品ID
export const loadGoodsInfo = ({ commit }, data) => {
  commit('SET_LOAD_STATUS', true)
  return new Promise((resolve, reject) => {
    baseApi.getOneGoods(data).then(res => {
      console.log(res.data)
      commit('SET_GOODS_DETAIL', res.data)
      // 设置默认SKU的vuex值
      commit('SET_SKU_GOODS_DETAIL', res.data.skuList[0])
      commit('SET_LOAD_STATUS', false)
    })
    // commit('SET_GOODS_DETAIL', tempData.tempGoodsDetail);
    // commit('SET_LOAD_STATUS', false);
  })
}

// 获取SKU商品详细信息，根据商品SPU的ID、规格参数组合
export const loadSkuGoodsInfo = ({ commit }, data) => {
  commit('SET_LOAD_STATUS', true)
  return new Promise((resolve, reject) => {
    baseApi.getSkuGoods(data).then(res => {
      console.log(res.data)
      commit('SET_SKU_GOODS_DETAIL', res.data)
      commit('SET_LOAD_STATUS', false)
    })
    // TODO 判断是否是库存不足码
    // commit('SET_SKU_GOODS_DETAIL', tempData.tempSkuGoodsDetail);
    // resolve(tempData.tempSkuGoodsDetail);
    // commit('SET_LOAD_STATUS', false);
  })
}

// 加载收货地址
export const loadAddress = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    userApi.getAddressList(data).then(res => {
      if (res.code === 200) {
        if(res.data.code){
          commit('SET_USER_ADDRESS', [])
        }else
        {
          commit('SET_USER_ADDRESS', res.data)
        }
        
      } else {
        resolve(false)
      }
    })
  })
}

// 删除收货地址
export const delAddress = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    userApi.delAddress(data).then(res => {
      if (res.code === 200) {
        resolve(true)
      } else {
        resolve(false)
      }
    })
  })
}

// 修改收货地址
export const editAddress = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    userApi.editAddress(data).then(res => {
      if (res.code === 200) {
        resolve(true)
      } else {
        resolve(false)
      }
    })
  })
}

// 添加购物车
export const addShoppingCart = ({ commit }, data) => {
  const item = {
    amount: data.amount,
    skuNo: data.skuNo,
    salePrice: data.salePrice,
    specialPrice: data.specialPrice
  }
  return new Promise((resolve, reject) => {
    cartApi.addShoppingCart(data).then(res => {
      if (res.code === 200) {
        commit('ADD_SHOPPING_CART', res.data)
        resolve(true)
      } else {
        resolve(false)
      }
    })
  })
}

// 加载购物车
export const loadShoppingCart = ({ commit }) => {
  return new Promise((resolve, reject) => {
    cartApi.getShoppingCart().then(res => {
      console.log(res.data)
      commit('SET_SHOPPING_CART', res.data)
    })
  })
}

// 清空购物车
export const clearShoppingCart = ({ commit }) => {
  return new Promise((resolve, reject) => {
    cartApi.clearShoppingCart().then(res => {
      if (res.code === 200) {
        resolve(true)
      } else {
        resolve(false)
      }
    })
  })
}

// 移除购物车商品
export const removeCartItems = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    cartApi.removeCartItems(data).then(res => {
      if (res.code === 200) {
        resolve(true)
      } else {
        resolve(false)
      }
    })
  })
}

// 更新购物车中的商品
export const updateCartItem = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    cartApi.updateCartItem(data).then(res => {
      if (res.code === 200) {
        resolve(true)
      } else {
        resolve(false)
      }
    })
  })
}

// 添加收货地址
export const addAddress = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    userApi.addAddress(data).then(res => {
      if (res.code === 200) {
        commit('SET_ADDRESS', data)
        resolve(true)
      } else {
        resolve(false)
      }
    })
  })
}

// 按标签获取商品
export const getGoodsByName = ({ commit }, data) => {
  console.log('获取商品列表')
  commit('SET_LOAD_STATUS', true)
  return new Promise((resolve, reject) => {
    baseApi.goodsList(data).then(res => {
      console.log(res.data.content)

      const goodsList = []
      if(res.data.content)
      {
        for (const item of res.data.content) {
          console.log(item.basicPrice)
          const temp = {
            id: item.id,
            goodsName: item.product_name,
            goodsImgs: item.default_pic,
            relCategory3Id: item.rel_category3_id,
            basicPrice: item.price,
            salesNum: item.sales_num
          }
          goodsList.push(temp)
        }
      }
      
      console.log("res.data.totalPages = ", res.data.totalElements)
      commit("SET_TOTAL_GOODS_NUMS", res.data.total - 1)
      commit('SET_GOODS_INFO_BY_NAME', goodsList)
      commit('SET_LOAD_STATUS', false)
    })
  })
}

// 生成订单
export const addOrder = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    userApi.addOrder(data).then(res => {
      if (res.code === 200) {
        resolve(res.data)
        // commit('REMOVE_SHOPPING_CART', data.cart);
      } else {
        resolve('')
      }
    })
  })
}

// 完成订单
export const finishOrder = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    userApi.finishOrder(data).then(res => {
      if (res.code === 200) {
        resolve(res.data)
        // commit('REMOVE_SHOPPING_CART', data.cart);
      } else {
        resolve('')
      }
    })
  })
}

// 获取订单
export const getOrder = ({ commit }, pageDto) => {
  return new Promise((resolve, reject) => {
    userApi.getOrder(pageDto).then(res => {
      console.log("获取订单列表" + res)
      if (res.code === 200) {
        commit('SET_USER_ORDER_INFO', res.data.content)
        commit('SET_USER_ORDER_SIZE', res.data.totalElements)
        console.log('总记录条数是', res.data.totalElements)
      }
    })
  })
}

// 获取订单详情
export const getOrderItems = ({ commit }, orderNumber) => {
  console.log("获取订单详情" + orderNumber)
  return new Promise((resolve, reject) => {
    userApi.getOrderItems(orderNumber).then(res => {
      console.log(res)
      if (res.code === 200) {
        commit('SET_USER_ORDER_ITEMS_INFO', res.data)
      }
    })
  })
}

// 获取规格列表
export const getCategoryList = ({ commit }) => {
  return new Promise((resolve, reject) => {
    baseApi.categoryList().then(res => {
      if (res.code === 200) {
        commit('SET_CATEGORY_LIST', res.data)
        // console.log(res.data)
      }
    })
  })
}

// 查询商品列表筛选条件
export const getSearchCondition = ({ commit }, data) => {
  commit('SET_LOAD_STATUS', true)
  return new Promise((resolve, reject) => {
    baseApi.getSearchCondition(data).then(res => {
      commit('SET_SEARCH_CONDITION', res.data)
      commit('SET_LOAD_STATUS', false)
    })
  })
}

// 退款
export const refund = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    userApi.refund(data).then(res => {
      if (res.code === 200) {
        console.log(res.data)
        resolve(res.data)
      }
    })
  })
}

// 获取商家的商品
export const getGoodsByMerchantId = ({ commit }, data) => {
  commit('SET_LOAD_STATUS', true)
  return new Promise((resolve, reject) => {
    // baseApi.goodsList(null, data).then(res => {
    //   console.log(res.data.result);
    //   commit('SET_GOODS_INFO_BY_MERCHANT_ID', res.data.result.data);
    //   commit('SET_LOAD_STATUS', false);
    // });
    commit('SET_GOODS_INFO_BY_MERCHANT_ID', tempData.tempResult)
    commit('SET_LOAD_STATUS', false)
  })
}

// 店铺热销
export const getMerchantHotsalesAction = ({ commit }, data) => {
  commit('SET_LOAD_STATUS', true)
  return new Promise((resolve, reject) => {
    goodsApi.getMerchantHotsales(data).then(res => {
      if (res.code === 200) {
        commit('SET_GOODS_INFO_BY_MERCHANT_ID', res.data)
        commit('SET_LOAD_STATUS', false)
        resolve(res.data)
      }
    })
  })
}

// 促销活动
export const getPromotion = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    userApi.getPromotion(data).then(res => {
      if (res.code === 200) {
        commit('SET_PROMOTION', res.data)
        resolve(res.data)
      }
    })
  })
}
// 优惠券活动
export const getDiscount = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    if (!isLogin()) {
      resolve(null)
      return
    }
    userApi.getDiscount(data).then(res => {
      if (res.code === 200) {
        commit('SET_DISCOUNT', res.data)
        resolve(res.data)
      }
    })
  })
}
// 领取优惠券
export const receive = ({ commit }, data) => {
  return new Promise((resolve, reject) => {
    if (!isLogin()) {
      resolve(false)
      return
    }
    userApi.receiveReduction(data).then(res => {
      if (res.code === 200) {
        resolve(true)
      } else {
        resolve(false)
      }
    })
  })
}


function isLogin () {
  let info = localStorage.getItem('info')
  if (!info) {
    return false
  }
  info = JSON.parse(info)
  const now = new Date().getTime()
  return info.exp > now

}

// 我的优惠券
export const getMyDiscount = ({ commit }) => {
  return new Promise((resolve, reject) => {
    userApi.getMyDiscount().then(res => {
      console.log('当前返回',res )
      if (res.code === 200) {
        commit('SET_MY_DISCOUNT', res.data)
        resolve(res.data)
      }
    })
  })
}
