<template>
  <div>
    <nav-bar title="商品详情" />
    <div class="item-detail-show">
      <!-- 左边商品图 -->
      <div class="item-detail-left">
        <div class="item-detail-big-img">
          <img :src="getGoodsDetailBase.goodsImgs[imgIndex]" alt="" />
        </div>
        <div class="item-detail-img-row">
          <div
            class="item-detail-img-small"
            v-for="(item, i) in getGoodsDetailBase.goodsImgs"
            :key="i"
            @mouseover="showBigImg(i)"
          >
            <img :src="item" alt="" />
          </div>
        </div>
      </div>
      <!-- 右边商品信息 -->
      <div class="item-detail-right">
        <div class="item-detail-title">
          <p>
            <span class="item-detail-express">校园配送</span>
            {{ getGoodsDetailBase.title }}
          </p>
        </div>
        <!-- 商品标签 -->
        <div class="item-detail-tag">
          <p>
            <span v-for="(item, index) in getGoodsDetailBase.tags" :key="index"
              >【{{ item }}】</span
            >
          </p>
        </div>
        <!-- 商品当前价格 -->
        <div class="item-detail-price-row">
          <div class="item-price-left">
            <div class="item-price-row">
              <p>
                <span class="item-price-title">会员价格</span>
                <span class="item-price"
                  >￥{{ price && price.toFixed(2) }}</span
                >
              </p>
            </div>
            <!-- 优惠价格 -->
            <div class="item-price-row">
              <p v-if="getDiscountList != ''">
                <span class="item-price-title">优 惠 券</span>
                <span
                  class="item-price-full-cut"
                  v-for="(item, index) in getDiscountList"
                  :key="index"
                  @click="receiveDiscount(item.id)"
                  >{{ item.note }}</span
                >
              </p>
            </div>
            <!-- 促销活动 -->
            <div class="item-price-row">
              <p v-if="getPromotionList != null">
                <span class="item-price-title"
                  >促&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;销</span
                >
                <span
                  class="item-price-full-cut"
                  v-for="(item, index) in getPromotionList"
                  :key="index"
                  >满{{ item.full_price }}减{{ item.reduce_price }}</span
                >
              </p>
            </div>
          </div>
          <!-- 销量 -->
          <div class="item-price-right">
            <div class="item-remarks-sum">
              <p>累计销售</p>
              <p>
                <span class="item-remarks-num"
                  >{{ getGoodsDetailBase.salesNum }} +件</span
                >
              </p>
            </div>
          </div>
        </div>
        <!-- 遍历规格项组合 BEGIN  -->
        <div
          class="item-select"
          v-for="(spec, indexFirst) in getGoodsDetailBase.specList"
          :key="indexFirst"
        >
          <!-- 规格项名称 -->
          <div class="item-select-title">
            <p>选择{{ spec.name }}</p>
          </div>
          <div class="item-select-container">
            <div
              class=""
              v-for="(item, i) in spec.optionDTOS"
              :key="i"
              @click="select(item.id, indexFirst, i)"
            >
              <div
                class="item-select-box"
                :class="{ 'item-select-box-active': item.enabled == true }"
              >
                <!-- 规格项值 图片 -->
                <div
                  class="item-select-img"
                  v-if="item.image != null && item.image != ''"
                >
                  <img :src="item.image" alt="" />
                </div>
                <!-- 规格项值 描述 -->
                <div class="item-select-intro">
                  <p>{{ item.name }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="item-select  hidden-lg hidden-md">
          <div class="item-select-title">
            <p>数量</p>
          </div>
          <div class="item-select-container">
            <InputNumber
              class="item-select-step"
              :min="1"
              :max="getSkuGoodsDetail.num"
              v-model="amount"
            ></InputNumber>
            <span> 库存 {{ getSkuGoodsDetail.num || 0 }} 件</span>
          </div>
        </div>
        <!-- 遍历规格项组合 END  -->
        <!-- 添加购物车 -->
        <div class="add-buy-car-box">
          <div class="add-buy-car hidden-xs hidden-sm">
            <InputNumber
              :min="1"
              :max="getSkuGoodsDetail.num"
              v-model="amount"
              size="large"
            ></InputNumber>
            <span> 库存 {{ getSkuGoodsDetail.num || 0 }} 件</span>
          </div>
          <div class="btn-group">
            <Button
              class="btn-cart"
              type="error"
              size="large"
              @click="addShoppingCartBtn()"
              >加入购物车</Button
            >
            <Button class="btn-buy" type="error" size="large" @click="goBuy()"
              >立即购买</Button
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import store from "@/vuex/store";
import navBar from "@/components/navBar";
import { mapState, mapActions, mapGetters } from "vuex";
export default {
  name: "ShowGoods",
  components: {
    navBar
  },
  data: () => {
    return {
      stockNum: 0,
      amount: 1,
      selectBoxIndex: 0,
      imgIndex: 0,
      skuList: [],

      specList: []
    };
  },
  created() {},
  computed: {
    ...mapState(["goodsDetail"]),
    ...mapGetters([
      "getGoodsDetailBase",
      "getSkuGoodsDetail",
      "getPromotionList",
      "getDiscountList"
    ]),
    // 商品金额
    price() {
      return this.getSkuGoodsDetail.price || this.getGoodsDetailBase.price;
    },
    // 被选中id集合
    select_ids() {
      const ids = [];
      this.getGoodsDetailBase.specList.forEach(item =>
        item.optionDTOS.filter(e => e.enabled).forEach(e => ids.push(e.id))
      );
      return ids;
    }
  },
  methods: {
    ...mapActions(["addShoppingCart", "loadSkuGoodsInfo", "receive"]),
    /**
     * 切换规格
     * index 和i用来控制点击项的高亮展示，同时需要id、push进对应索引的 select_id[]
     * @param id 当前商品id
     * @param index 大规格的索引，具体点击的是颜色，还是尺寸
     * @param i 小规格的索引，点击的是颜色规格下的黑色，还是白色
     */
    sortNumber(a, b) {
      return a - b;
    },
    select(id, index, i) {
      /**
       this.select_id[index]
       1.如果此时你点击的是第一项：号码，那么 index == 0，循环this.sku[0].list
       如果满足item.id == id 这个条件，就返回item这个数据，把该数据的id、赋值给this.select_id[0]
       2.如果此时你点击的是第二项：颜色，那么 index == 1，循环this.sku[1].list
       如果满足item.id == id 这个条件，就返回item这个数据，把该数据的id、赋值给this.select_id[1]
       3.这样我们就拿到了[10，15] 这样的数据(黑色,43号)，用这个数据去跟后台返回的skuPrice做对比，如果值相同，则展示对应的价格和库存
      */
      this.select_ids[index] = this.getGoodsDetailBase.specList[
        index
      ].optionDTOS.filter(item => {
        return item.id === id;
      })[0].id;
      // 高亮处理
      this.getGoodsDetailBase.specList[index].optionDTOS.forEach(item => {
        if (item.id === id) {
          this.getGoodsDetailBase.specList[index].optionDTOS[i].enabled = true;
        } else {
          item.enabled = false;
        }
      });

      /*
        如果 selectIds 的 length 等于 this.specList.length，说明此时规格已全部选择完毕，
        将规格值id顺序排序后请求后台接口获取对应的sku商品价格和库存
      */
      // A方案: 一次性返回前端所有的sku列表数据，前端做匹配，走的缓存，不具有实时性
      // B方案: 直接请求后台接口，返回对应的数据，但是接口消耗太大，没有必要
      // C: 先走前端缓存,再走后端请求
      // let skuData = this.getGoodsDetailBase.skuList.filter(item => {
      //   return this.select_id.length === item.spec.length && this.select_id.every(a => item.spec.some(b => a === b)) && item.spec.every(_b => this.select_id.some(_a => _a === _b));
      // });
      // for (let i = 0; i < this.getGoodsDetailBase.specList.length; i++) {
      //   if (this.select_ids[i] === undefined) {
      //     return;
      //   }
      // }
      if (this.select_ids.length < this.getGoodsDetailBase.specList.length) {
        return this.$Message.error("继续选择完整规格");
      }

      const reqParam = {};
      this.select_ids.sort(this.sortNumber);
      reqParam.optionIds = this.select_ids.join(",");
      reqParam.productId = this.getGoodsDetailBase.goodsId;
      this.loadSkuGoodsInfo(reqParam).then(data => {
        console.info("111");
      });
    },
    // 显示大图
    showBigImg(index) {
      console.info(this.getGoodsDetailBase.goodsImgs[index]);
      this.imgIndex = index;
    },
    // 添加购物车
    addShoppingCartBtn() {
      for (let i = 0; i < this.getGoodsDetailBase.specList.length; i++) {
        if (this.select_ids[i] === undefined) {
          return this.$Message.error("请选择完整规格");
        }
      }
      // 组装购物车数据
      const data = {
        categoryId: this.goodsDetail.rel_category3_id,
        amount: this.amount,
        skuId: this.getSkuGoodsDetail.id,
        skuNo: this.getSkuGoodsDetail.skuNo,
        salePrice: this.getSkuGoodsDetail.price,
        specialPrice: this.getSkuGoodsDetail.price
      };

      this.addShoppingCart(data).then(data => {
        if (data) {
          this.$Message.success("添加购物车成功");
          this.$router.push("/shoppingCart");
        } else {
          this.$Message.error("添加购物车出错");
        }
      });
    },
    // 立即购买
    goBuy() {
      for (let i = 0; i < this.getGoodsDetailBase.specList.length; i++) {
        if (this.select_ids[i] === undefined) {
          return this.$Message.error("请选择完整规格");
        }
      }
      // 组装购物车数据
      const data = {
        categoryId: this.goodsDetail.rel_category3_id,
        amount: this.amount,
        skuId: this.getSkuGoodsDetail.id,
        skuNo: this.getSkuGoodsDetail.skuNo,
        salePrice: this.getSkuGoodsDetail.price,
        specialPrice: this.getSkuGoodsDetail.price
      };
      this.addShoppingCart(data).then(data => {
        if (data) {
          this.$Message.success("添加购物车成功");
          this.$router.push("/shoppingCart");
        } else {
          this.$Message.error("添加购物车出错");
        }
      });
    },

    receiveDiscount(index) {
      this.receive(index).then(result => {
        if (result) {
          this.$Message.success("领取成功");
        } else {
          this.$Message.error("领取失败");
        }
      });
    }
  },
  store
};
</script>

<style scoped>
/******************商品图片及购买详情开始******************/
.item-detail-show {
  margin: 15px auto;
  display: flex;
  flex-direction: row;
  background-color: #fff;
}
.item-detail-left {
  width: 350px;
  margin-right: 30px;
}
.item-detail-big-img {
  width: 350px;
  height: 350px;
  box-shadow: 0px 0px 8px #ccc;
  cursor: pointer;
}
.item-detail-big-img img {
  width: 100%;
}
.item-detail-img-row {
  margin-top: 15px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  background: #fff;
}
.item-detail-img-small {
  width: 68px;
  height: 68px;
  box-shadow: 0px 0px 8px #ccc;
  cursor: pointer;
}
.item-detail-img-small img {
  width: 100%;
}
/*商品选购详情*/
.item-detail-right {
  display: flex;
  flex-direction: column;
}
.item-detail-title p {
  color: #666;
  font-size: 20px;
}
.item-detail-express {
  font-size: 14px;
  padding: 2px 3px;
  border-radius: 3px;
  background-color: #e4393c;
  color: #fff;
}
/*商品标签*/
.item-detail-tag {
  font-size: 12px;
  color: #e4393c;
}
/*价格详情等*/
.item-detail-price-row {
  padding: 5px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  background-color: #f3f3f3;
}
.item-price-left {
  display: flex;
  flex-direction: column;
}
.item-price-title {
  color: #999999;
  font-size: 14px;
  margin-right: 15px;
}
.item-price-row {
  margin: 5px 0px;
}
.item-price {
  color: #e4393c;
  font-size: 23px;
  cursor: pointer;
}
.item-price-full-cut {
  margin-right: 5px;
  padding: 3px;
  color: #e4393c;
  font-size: 12px;
  background-color: #ffdedf;
  border: 1px dotted #e4393c;
  cursor: pointer;
}
.item-remarks-sum {
  padding-left: 8px;
  border-left: 1px solid #ccc;
}
.item-remarks-sum p {
  color: #999999;
  font-size: 12px;
  line-height: 10px;
  text-align: center;
}
.item-remarks-num {
  line-height: 18px;
  color: #005eb7;
}
.item-select {
  display: flex;
  flex-direction: row;
  margin-top: 15px;
}
.item-select-title {
  color: #999999;
  font-size: 14px;
  margin-right: 15px;
}
.item-select-column {
  display: flex;
  flex-direction: column;
}
.item-select-row {
  display: flex;
  flex-direction: row;
  margin-bottom: 8px;
}
.item-select-container {
  display: flex;
  display: row;
  flex-wrap: wrap;
  align-items: center;
}
.item-select-box {
  display: flex;
  flex-direction: row;
  align-items: center;
  padding: 5px;
  margin-right: 8px;
  margin-bottom: 15px;
  background-color: #f7f7f7;
  border: 0.5px solid #ccc;
  cursor: pointer;
}
.item-select-img {
  width: 36px;
}
.item-select-box:hover {
  border: 0.5px solid #e3393c;
}
.item-select-box-active {
  border: 0.5px solid #e3393c;
}
.item-select-img img {
  width: 100%;
}
.item-select-intro p {
  margin: 0px;
  padding: 5px;
}
.item-select-class {
  padding: 5px;
  margin-right: 8px;
  background-color: #f7f7f7;
  border: 0.5px solid #ccc;
  cursor: pointer;
}
.item-select-class:hover {
  border: 0.5px solid #e3393c;
}
.add-buy-car-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  margin-top: 15px;
  border-top: 1px dotted #ccc;
}
.add-buy-car {
  margin-top: 15px;
}
/******************商品图片及购买详情结束******************/
</style>

<style lang="less" scoped>
@media (max-width: 992px) {
  .item-detail-show {
    width: 100%;
    margin: 0;
    flex-wrap: wrap;
    .item-detail-right,
    .item-detail-left {
      width: 100%;
      margin-right: 0;
    }
    .item-detail-big-img {
      margin: 0;
      width: 100%;
      height: auto;
      img {
        width: 100%;
      }
    }
    .item-detail-img-row {
      margin-top: 0;
    }
    .item-detail-right {
      padding: 12px 18px;
      .item-select {
        flex-wrap: wrap;
        margin-top: 0;
        .item-select-title {
          font-size: 13px;
          color: #262626;
          font-weight: 700;
          height: 40px;
          line-height: 40px;
        }
        .item-select-container {
          width: 100%;
          span {
            color: #262626;
            font-weight: 400;
          }
          .item-select-box {
            padding: 0 18px;
            height: 30px;
            line-height: 30px;
            float: left;
            text-align: center;
            margin-right: 12px;
            margin-bottom: 10px;
            font-size: 11px;
            background: #f2f2f2;
            border-radius: 15px;
            border: none;
            .item-select-intro p {
              color: #262626;
            }
            &.item-select-box-active {
              background: #fcedeb;
              border: 1px solid #f2270c;
              font-size: 11px;
              font-weight: 700;
              height: 28px;
              .item-select-intro p {
                color: #f2270c;
              }
            }
          }
          .item-select-step {
            margin-right: 5px;
          }
        }
      }
      .item-detail-title p {
        font-size: 16px;
      }
    }
  }
  .add-buy-car-box {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 23;
    background: #fff;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 6px 18px;
    border: none;
    margin-top: 0;
    .btn-group {
      display: flex;
      flex-grow: 1;
    }
    button {
      flex-grow: 1;
      height: 38px;
      border-radius: 21px;
      color: #fff;
      font-size: 13px;
      font-weight: 700;
      text-align: center;
      border: none;
      + button {
        margin-left: 12px;
      }
      span {
        line-height: 38px;
      }
    }
    .btn-cart {
      background-image: linear-gradient(135deg, #f2140c, #f2270c 70%, #f24d0c);
    }
    .btn-buy {
      background-image: linear-gradient(135deg, #ffba0d, #ffc30d 69%, #ffcf0d);
    }
  }
}
</style>
