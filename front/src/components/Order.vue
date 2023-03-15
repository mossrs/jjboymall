<template>
  <div>
    <Sreach></Sreach>
    <GoodsListNav></GoodsListNav>
    <div class="goods-list-container">
      <Alert show-icon class="tips-box">
        小提示
        <Icon type="ios-lightbulb-outline" slot="icon"></Icon>
        <template slot="desc">请点击商品前的选择框，选择购物车中的商品，点击付款即可。</template>
      </Alert>
      <Table border ref="selection" :columns="columns" :data="shoppingCart" size="large" @on-selection-change="select" no-data-text="您的购物车没有商品，请先添加商品到购物车再点击购买"></Table>
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
      <div class="address-container">
        <h3>支付方式选择</h3>
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
      <div class="remarks-container">
        <h3>备注</h3>
        <i-input v-model="remarks" size="large" placeholder="在这里填写备注信息" class="remarks-input"></i-input>
      </div>
      <div class="invoices-container">
        <h3>发票信息</h3>
        <p>该商品不支持开发票</p>
      </div>
      <div class="pay-container">
        <div class="pay-box">
          <p><span>提交订单应付总额：</span> <span class="money"><Icon type="social-yen"></Icon> {{totalPrice.toFixed(2)}}</span></p>
          <div class="pay-btn">
            <Button type="error" @click="pay" size="large">支付订单</Button>
          </div>
        </div>
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
  name: 'Order',
  data () {
    return {
      goodsCheckList: [],
      columns: [
        {
          type: 'selection',
          width: 58,
          align: 'center'
        },
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
          title: '套餐',
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
          key: 'action',
          width: 100,
          align: 'center',
          // <InputNumber :max="10" :min="1" v-model="value1"></InputNumber>
          render: (h, params) => {
            return h('div', [
              h('InputNumber', {
                props: {
                  max: 10,
                  min: 1,
                  size: 'small',
                  value: params.row.amount
                },
                style: {
                  width: '50px'
                },
                on: {
                  'on-change': (e) => {
                    this.updateCartItemNumber(e, params);
                  }
                }
              })
            ]);
          }
        }
      ],
      checkAddress: {
        flag: false,
        index: 999,
        name: '未选择',
        address: '请选择地址'
      },
      checkPay: {
        flag: false,
        index: 999,
        name: '请选择支付方式'
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
    ...mapState(['address', 'shoppingCart', 'userInfo']),
    totalPrice () {
      let price = 0;
      this.goodsCheckList.forEach(item => {
        price += item.specialPrice * item.amount;
      });
      return price;
    },
    tempVal () {
      return this;
    }
  },
  // 创建
  created () {
    const info = JSON.parse(localStorage.getItem('info'));
    const username = info.data.username;
    this.loadAddress(username);
  },
  methods: {
    ...mapGetters(['isLogin']),
    ...mapActions(['loadAddress', 'addOrder', 'loadShoppingCart', 'updateCartItem']),
    select (selection, row) {
      this.goodsCheckList = selection;
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

      if (this.goodsCheckList.length <= 0) {
        this.$Message.error('请选择商品');
        return false;
      }

      if (!this.isLogin(this.$router)) {
        this.$Message.error('请先登录');
        this.$router.push('/login');
        return false;
      }

      console.log(this.remarks);
      console.log(this.address[this.checkAddress.index]);
      console.log(this.goodsCheckList);
      // 购物车商品列表
      const goodsList = [];
      for (const item of this.goodsCheckList) {
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
        items: goodsList
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
    setTimeout(() => {
      this.$refs.selection.selectAll(true);
    }, 500);
  },
  components: {
    Sreach,
    GoodsListNav,
    Footer
  },
  store
};
</script>

<style scoped>
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
.pay-container {
  margin: 15px;
  display: flex;
  justify-content: flex-end;
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
</style>
