<template>
  <div>
    <Sreach></Sreach>
    <GoodsListNav></GoodsListNav>
    <div class="goods-list-container">
      <Alert show-icon class="tips-box">
        <Icon type="ios-lightbulb-outline" slot="icon"></Icon>
        小提示 <template slot="desc">填写并核对订单信息</template>
      </Alert>
      <!-- 收货地址区域 -->
      <div class="address-container">
        <h3>收货人信息</h3>
        <div class="address-box">
          <div class="address-check">
            <div class="address-check-name">
              <span><Icon type="ios-checkmark-outline"></Icon>{{checkAddress.name}}</span>
            </div>
            <div class="address-detail">
              <p>{{checkAddress.address}}</p>
            </div>
          </div>
          <Collapse>
            <Panel>
                选择地址
                <p slot="content">
                  <RadioGroup vertical size="large" @on-change="changeAddress">
                    <Radio :label="item.id" v-for="(item, index) in address" :key="index">
                      <span>{{item.recipient}}  {{item.province}} {{item.city}} {{item.address}} {{item.telephone}} </span>
                    </Radio>
                  </RadioGroup>
                </p>
            </Panel>
          </Collapse>
        </div>
      </div>
      <!-- 支付方式区域 -->
      <div class="address-container">
        <h3>支付方式</h3>
        <div class="address-box">
          <div class="address-check">
            <div class="address-check-name">
              <span><Icon type="ios-checkmark-outline"></Icon>{{checkPay.name}}</span>
            </div>
          </div>
          <RadioGroup size="large" @on-change="changePay">
            <Radio :label="item.payType" v-for="(item, index) in payList" :key="index">
              <i :class="item.iconClass" size="24" ></i>
              <span>{{item.payTypeName}}</span>
            </Radio>
          </RadioGroup>
        </div>
      </div>
      <!-- 送货清单区域 -->
      <div class="address-container">
        <h3>送货清单</h3>
        <div class="address-box">
<!--          <Table ref="selection" :columns="columns" :data="shoppingCart" size="small" @on-selection-change="select" no-data-text="您的购物车没有商品，请先添加商品到购物车再点击购买"></Table>-->
          <Row v-for="(item,index) in selectedCartInfo.selectedCartItems" :key="index" class="pay-order-row pay-order-col">
            <Col span="4">
                <img :src="item.image" class="pay-order-img"/>
            </Col>
            <Col span="8">
              <div>
                {{item.title}}
              </div>
            </Col>
            <Col span="4">
              <div>
                {{item.specialPrice.toFixed(2)}}
              </div>
            </Col>
            <Col span="4">
              <div>
                x {{item.amount}}
              </div>
            </Col>
            <Col span="4">
              有货
            </Col>
          </Row>

        </div>
      </div>
      <!-- 备注区域 -->
      <div class="remarks-container">
        <h3>备注</h3>
        <i-input v-model="remarks" size="large" placeholder="在这里填写备注信息" class="remarks-input"></i-input>
      </div>
      <!-- 发票区域 -->
      <div class="invoices-container">
        <h3>发票信息</h3>
        <p>该商品不支持开发票</p>
      </div>
      <!-- 优惠券区域 -->
      <div class="address-container">
        <h3>使用优惠/礼品卡/抵用
          <Icon :type="discountShowValue===false ? 'ios-arrow-down' : 'ios-arrow-up'" @click="changeShowDiscount()"></Icon>
        </h3>
        <Tabs type="card" v-if="discountShowValue===true" class="discount-tab">
          <TabPane label="商品优惠券" icon="bag">
            <div class="coupon-scrollbar">
              <div class="ui-scrollbar-main">
                <div class="coupon-scroll">
                  <!--可用优惠券 -->
                  <div class="coupon-enable" v-for="(item1, index1) in couponList" :key="index1">
                    <Tag>{{item1.productCategoryName}}</Tag>
                    <ul>
                      <li v-for="(item, index) in item1.coupons" :key="index">
                        <div class="coupon-item c-nopointer coupon-item-new">
                          <div class="c-detail" :class="{'c-detail item-selected':item.checked}" @click="selectCoupon($event,item1,item,index1,index)">
                            <div class="c-msg c-dong c-nopointer">
                              <div class="c-top-dong"></div>
                              <div class="c-price">
                                <em>￥{{item.amount}}</em>
                              </div>
                              <div class="c-limit">
                                 <span>满{{item.minPoint}}</span>
                              </div>
                              <div class="c-time c-time-dong">
                                <span>有效期至{{new Date(item.endTime).toLocaleString()}}</span>
                              </div>
                            </div>
                            <div class="c-type c-type-dong">
                              <span class="c-type-l">[优惠券]</span>
                              <span class="c-type-r" id="119363094713">[限品类]</span>
                            </div>
                          </div>
                          <div class="c-info">
                          </div>
                        </div>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </TabPane>
        </Tabs>
      </div>

      <Row class-name="topDist">
        <Col span="3" offset="20" class="order-summary-item">
          <span><em class="ftx-01">{{num}}</em> 件商品，总商品金额：</span>
        </Col>
        <Col span="1">
          <em class="price">￥{{sumPrice.toFixed(2)}}</em>
        </Col>
      </Row>
      <Row>
        <Col span="3" offset="20" class="order-summary-item">
          商品优惠 :
        </Col>
        <Col span="1">
          <em class="price">￥{{discountSumPrice.toFixed(2)}}</em>
        </Col>
      </Row>

      <!-- 提交订单 -->
      <div class="trade-foot-detail-com topDist">
        <div class="fc-price-info">
          <span class="price-tit">应付总额：</span>
          <span class="price-num" id="sumPayPriceId">￥ {{totalPrice.toFixed(2)}}</span>
        </div>
        <div class="fc-consignee-info">
          <span class="mr20" id="sendAddr">寄送至： {{checkAddress.address}}</span>
          <span id="sendMobile">收货人：{{checkAddress.user}}</span>
        </div>
      </div>

      <div class="pay-btn">
        <Button type="error" @click="pay" size="large" class="submit-order">提交订单</Button>
      </div>
    </div>
    <Footer></Footer>
  </div>
</template>

<script>
import Sreach from '@/components/Sreach';
import GoodsListNav from '@/components/nav/GoodsListNav';
import Footer from '@/components/footer/Footer';
import store from '@/vuex/store';
import {mapState, mapActions, mapGetters} from 'vuex';

export default {
  name: 'PayOrder',
  data () {
    return {
      num: 0,
      sumPrice: 0.00,
      couponPrice: 0.00,
      discountShowValue: false,
      selectedCouponCidList: [],
      selectedCouponIdList: [],
      columns: [
        {
          title: '图片',
          key: 'image',
          width: 86,
          render: (h, params) => {
            return h('div', [
              h('img', {
                attrs: {
                  src: params.row.image,
                  style: 'height:100px;'
                }
              })
            ]);
          },
          align: 'center'
        },
        {
          title: '标题',
          key: 'title',
          align: 'center'
        },
        {
          title: '规格',
          width: 198,
          key: 'skuSpec',
          align: 'center',
          render: function (h, params) {
            var spec = this.row.skuSpec;
            // [{"specType":"主体","list":[{"name":"颜色","value":"粉色"},{"name":"尺寸","value":"6.3"},{"name":"网络","value":"5G"}]}]
            var objs = JSON.parse(spec);
            var description = '';
            for (var obj of objs) {
              var list = obj.list;
              for (var li of list) {
                description += li.name + ':' + li.value + ' ; ';
              }
            }
            return h('span', description);
          }
        },
        {
          title: '价格',
          width: 68,
          key: 'specialPrice',
          align: 'center',
          render: function (h, params) {
            return h('span', this.row.specialPrice.toFixed(2)); // 这里的this.row能够获取当前行的数据
          }
        },
        {
          title: '数量',
          key: 'amount',
          width: 100,
          align: 'center'
        }
      ],
      checkAddress: {
        flag: false,
        index: 999,
        name: '未选择',
        address: '请选择地址',
        user: '请选择收件人'
      },
      checkPay: {
        flag: false,
        index: 999,
        name: '未选择'
      },
      payList: [
        {
          payType: 1,
          payCode: 'aliPay',
          payTypeName: '支付宝',
          iconClass: 'icon-font icon-zhifubao'
        },
        {
          payType: 2,
          payCode: 'webChatPay',
          payTypeName: '微信',
          iconClass: 'icon-font icon-weixin'
        },
        {
          payType: 3,
          payCode: 'unionPay',
          payTypeName: '银联',
          iconClass: 'icon-font icon-yinlian'
        }
      ],
      remarks: '',
      htmls: ''

    };
  },
  computed: {
    ...mapState(['address', 'shoppingCart', 'userInfo', 'selectedCartItems', 'selectedCartInfo', 'couponList']),
    totalPrice () {
      return this.sumPrice - this.discountSumPrice;
    },
    discountSumPrice () {
      return this.selectedCartInfo.discountAmount + this.couponPrice;
    },
    tempVal () {
      return this;
    }
  },
  // 创建
  created () {
    // 选择多少件商品
    const e = this;
    const cidSet = new Set();
    this.selectedCartInfo.selectedCartItems.forEach(function (val) {
      // 总价
      e.sumPrice += val.amount * val.specialPrice;
      e.num += val.amount;
      cidSet.add(val.categoryId);
    });
    const info = JSON.parse(localStorage.getItem('info'));
    const username = info.data.username;
    this.loadAddress(username);

    // 查询优惠券
    const params = Array.from(cidSet).join(',');
    this.getCouponListByCategoryIds(params);
  },
  methods: {
    ...mapGetters(['isLogin']),
    ...mapActions(['loadAddress', 'addOrder', 'loadShoppingCart', 'updateCartItem', 'getCouponListByCategoryIds']),
    select (selection, row) {
      this.goodsCheckList = selection;
    },
    // 切换优惠券
    selectCoupon (e, item1, item, index1, index) {
      const cid = item1.productCategoryId;
      if (!item.checked) {
        // TODO 校验是否已经存在选中的该品类的优惠券，同一分类下只能选一张，提示信息
        if (this.selectedCouponCidList.indexOf(cid) > -1) {
          this.$Message.warning('同一品类的商品只能选择一张优惠券~');
          return;
        }
        let cost = 0.00;
        // 该分类下的商品金额是满足优惠券的优惠条件
        this.selectedCartInfo.selectedCartItems.forEach(function (val) {
          if (val.categoryId === cid) {
            cost += val.amount * val.specialPrice;
          }
        });
        if (cost < item.minPoint) {
          this.$Message.warning('所结算的该品类下的商品不符合改优惠券~');
          return;
        }
        // 更新优惠价 +
        this.couponPrice += item.amount;
        this.selectedCouponCidList.push(cid);
        this.selectedCouponIdList.push(item.id);
        item.checked = true;
        // 触发视图更新，常规的数组赋值是不触发视图更新的
        this.couponList[index1].coupons.splice(index, 1, item);
      } else {
        // TODO 取消选中，更新优惠金额
        // 更新优惠价 -
        this.couponPrice -= item.amount;
        this.selectedCouponCidList.splice(this.selectedCouponCidList.findIndex(v => v === cid), 1);
        this.selectedCouponIdList.splice(this.selectedCouponIdList.findIndex(v => v === item.id), 1);
        item.checked = false;
        this.couponList[index1].coupons.splice(index, 1, item);
      }
      console.info(this.selectedCouponIdList);
    },
    changeShowDiscount () {
      this.discountShowValue = !this.discountShowValue;
    },
    // 修改收货地址
    changeAddress (data) {
      const father = this;
      this.address.forEach((item, index) => {
        if (item.id === data) {
          father.checkAddress.index = index;
          father.checkAddress.flag = true;
          father.checkAddress.name = item.recipient;
          father.checkAddress.address = `${item.recipient} ${item.province} ${item.city} ${item.address} ${item.telephone}`;
        }
      });
    },
    // 修改支付方式
    changePay (data) {
      const father = this;
      this.payList.forEach((item, index) => {
        if (item.payType === data) {
          father.checkPay.index = index;
          if (father.checkPay.flag) {
            father.checkPay.flag = false;
          } else {
            father.checkPay.flag = true;
          }
          father.checkPay.name = item.payTypeName;
        }
      });
    },
    // 提交订单
    pay () {
      if (!this.checkAddress.flag) {
        this.$Message.error('请选择地址');
        return false;
      }
      if (!this.isLogin(this.$router)) {
        this.$Message.error('请先登录');
        this.$router.push('/login');
        return false;
      }
      console.log(this.address[this.checkAddress.index]);
      // 购物车商品列表
      const goodsList = [];
      for (const item of this.selectedCartInfo.selectedCartItems) {
        const goods = {
          quantity: item.amount,
          productSkuNo: item.skuNo,
          productId: item.skuId
        };
        goodsList.push(goods);
      }
      let address = this.address[this.checkAddress.index];
      let addressStr = address.province + address.city + address.address;
      let receiverPhone = address.telephone;
      // TODO 获取用户姓名
      let reserveName = 'msb';
      // 请求数据
      const data = {
        memberReceiveAddressId: address.address_id,
        receiverDetailAddress: addressStr,
        receiverPhone: receiverPhone,
        receiverName: reserveName,
        payType: this.payList[this.checkPay.index].payType,
        items: goodsList,
        useCouponIds: this.selectedCouponIdList
      };
      this.addOrder(data).then(result => {
        if (result) {
          // this.$router.push('/pay');
          // 跳转支付宝页面、加载表单
          // 返回参数
          let routerData = this.$router.resolve({path: '/applyText', query: {htmlData: result}});
          let htmlData = result;
          // 打开新页面
          window.open(routerData.href, '_ blank');
          const div = document.createElement('div');
          div.innerHTML = htmlData;
          document.body.appendChild(div);
          document.forms[0].submit();
        } else {
          this.$Message.error('下单失败');
        }
      });
    },
    // 更新购物车商品的信息
    updateCartItemNumber (num, param) {
      const row = param.row;
      const newCartItem = {
        skuNo: row.skuNo,
        amount: num
      };
      const oldCartItem = {
        skuNo: row.skuNo
      };
      const updateCartItem = {
        oldCartItem: oldCartItem,
        newCartItem: newCartItem
      };
      this.updateCartItem(updateCartItem).then(data => {
        if (data) {
          this.$Message.success('更新商品成功');
          this.loadShoppingCart();
        } else {
          this.$Message.error('更新购物车商品出错');
        }
      });
    }
  },
  // 计算属性
  mounted () {
    // setTimeout(() => {
    //   this.$refs.selection.selectAll(true);
    // }, 500);
  },
  components: {
    Sreach,
    GoodsListNav,
    Footer
  },
  store
};

Date.prototype.toLocaleString = function () {
  // 补0   例如 2018/7/10 14:7:2  补完后为 2018/07/10 14:07:02
  function addZero (num) {
    if (num < 10) {
      return '0' + num;
    }
    return num;
  }
  // 按自定义拼接格式返回
  return this.getFullYear() + '年' + addZero(this.getMonth() + 1) + '月' + addZero(this.getDate()) + '日';
};

</script>

<style scoped>
  /** 订单价格简要计算开始 */
  .topDist {
    margin-top: 20px;
  }
  .ftx-01 {
    color: #e4393c;
  }

  .order-summary-item {
    text-align: end;
  }
  .order-summary-item .price {
    color: #333;
    float: left;
    width: 100px;
    text-align: right;
    font-family: verdana;
  }
  .trade-foot-detail-com {
    padding: 15px 10px 15px 0;
    line-height: 20px;
    text-align: right;
    border-top: 1px solid #e6e6e6;
    width: 100%;
    color: #999;
    background-color: #f4f4f4;
  }
  .trade-foot-detail-com .fc-price-info .price-tit, .trade-foot-detail-com .presale-price-info .price-tit {
    color: #666;
  }
  .trade-foot-detail-com .fc-price-info, .trade-foot-detail-com .presale-price-info {
    margin-right: 10px;
    line-height: 25px;
  }
  .trade-foot-detail-com .fc-price-info .price-num, .trade-foot-detail-com .presale-price-info .price-num {
    color: #e4393c;
    font-family: Verdana;
    font-weight: 700;
    font-size: 18px;
    min-width: 122px;
    _width: 122px;
    float: right;
    *float: none;
    text-align: right;
  }
  /** 优惠券开始 */
.coupon-scrollbar {
  width: 100%;
}

.coupon-scroll {
  overflow: hidden;
  width: 100%;
}

.coupon-scroll .coupon-enable {
  display: block;
  width: 100%;
}

.coupon-scroll li {
  display: inline;
}

.coupon-scroll .coupon-item.coupon-item-new {
  height: 125px;
}

.coupon-scroll .coupon-item {
  height: 105px;
  width: 201px;
  float: left;
  margin-right: 26px;
  margin-bottom: 15px;
  padding: 1px;
  position: relative;
}

.coupon-scroll .coupon-item .item-selected {
  border: 2px solid #e43a3d;
  background-image: url(//misc.360buyimg.com/user/purchase/2.0.0/css/i/coupon-selected.png);
  background-repeat: no-repeat;
  background-position: bottom right;
}

.coupon-scroll .coupon-item .c-detail .c-type-dong {
  color: #74d2d4;
  border: 1px solid #cef0f1;
}

.coupon-scroll .coupon-item .c-detail .c-msg {
  cursor: pointer;
  height: 70px;
  width: 100%;
  position: relative;
}

.coupon-scroll .coupon-item .c-detail .c-dong {
  border-left: 1px solid #74d2d4;
  border-right: 1px solid #74d2d4;
  background-color: #74d2d4;
}

.coupon-scroll .coupon-item .c-detail .c-type span.c-type-r {
  margin: 0;
  cursor: pointer;
}

.coupon-scroll .coupon-item .c-info {
  height: 40px;
  width: 210px;
  color: #333;
}

.coupon-scroll .coupon-item .c-detail .c-top-dong {
  height: 3px;
  width: 100%;
}

.coupon-scroll .coupon-item .c-detail .c-msg .c-price {
  color: #fff;
  font: 24px Arial,Verdana,'Microsoft YaHei',SimSun;
  display: inline;
  position: relative;
  top: 8px;
  margin-left: 12px;
  vertical-align: bottom;
  *float: left;
}

.coupon-scroll .coupon-item .c-detail .c-msg .c-limit, .coupon-scroll .coupon-item .c-detail .c-msg .c-over {
  color: #f5f5f5;
  font-size: 12px;
  display: inline;
  position: relative;
  top: 7px;
}

.coupon-scroll .coupon-item .c-detail .c-msg .c-time-dong {
  color: #cef0f1;
}

.coupon-scroll .coupon-item .c-detail .c-msg .c-time-dong span {
  float: left;
}

.coupon-scroll .coupon-item .c-detail .c-msg .c-time {
  padding-left: 12px;
  margin-top: 10px;
  *clear: both;
}

.coupon-scroll .coupon-item .c-detail .c-type {
  height: 25px;
  width: 100%;
  padding-top: 5px;
}

.coupon-scroll .coupon-item .c-detail .c-type span.c-type-l {
    margin: 0 5px 0 12px;
}
/** 优惠券结束 */

.goods-list-container {
  margin: 15px auto;
  width: 80%;
}
.tips-box {
  margin-bottom: 15px;
}
.address-container {
  margin-top: 15px;
}
.address-box {
  margin-top: 15px;
  padding: 15px;
  border: 1px #ccc dotted;
}
.address-check {
  margin: 15px 0px;
  height: 36px;
  display: flex;
  align-items: center;
}
.address-check-name {
  width: 120px;
  display: flex;
  justify-content: center;
  align-content: center;
  background-color: #ccc;
}
.address-check-name span {
  width: 120px;
  height: 36px;
  font-size: 14px;
  line-height: 36px;
  text-align: center;
  color: #fff;
  background-color: #f90013;
}

.pay-check-name span {
  width: 120px;
  height: 36px;
  font-size: 14px;
  line-height: 36px;
  text-align: center;
  color: #fff;
  background-color: #0070f9;
}

.address-detail {
  padding-left: 15px;
  font-size: 14px;
  color: #999999;
}
.remarks-container {
  margin: 15px 0px;
}
.remarks-input {
  margin-top: 15px;
}
.invoices-container p{
  font-size: 12px;
  line-height: 30px;
  color: #999;
}

.pay-box {
  font-size: 18px;
  font-weight: bolder;
  color: #495060;
}
.money {
  font-size: 26px;
  color: #f90013;
}
.pay-btn {
  margin: 15px 0px;
  display: flex;
  justify-content: flex-end;
}

.submit-order {
  float: right;
  position: relative;
  width: 135px;
  height: 36px;
  line-height: 36px;
  margin: 8px 10px 0 0;
  padding: 0;
  background-color: #e00;
  overflow: hidden;
  color: #fff;
  font-weight: 700;
  font-size: 16px;
  font-family: arial,"Microsoft YaHei";
  display: inline-block;
  border-radius: 3px;
  cursor: pointer;
  border: 0;
}

.pay-order-img {
  height: 100px;
  width: 100px;
}

.pay-order-row {
  border: 1px #ccc dotted;
}

.pay-order-col {
  display: flex;
  justify-content: center;
  text-align: center;
  vertical-align: center;
  height:100px;
  line-height:100px;
  overflow:hidden;
}
.discount-tab {
  margin-top: 8px;
}

.invoices-container {
  margin-top: 10px;
}
</style>
