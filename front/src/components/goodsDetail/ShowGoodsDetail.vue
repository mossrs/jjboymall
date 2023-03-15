<template>
  <div>
    <div class="item-intro-show">
      <div class="item-intro-recommend hidden-xs hidden-sm">
        <div class="item-recommend-title">
          <p>店铺热销</p>
        </div>
        <div class="item-intro-recommend-column">
          <div
            class="item-recommend-column"
            v-for="(item, index) in merchantItem"
            :key="index"
          >
            <div class="item-recommend-img">
              <img :src="item.img" alt="" @click="goDetail(item)" />
            </div>
            <div class="item-recommend-intro">
              <span>{{ item.goodsName }}</span>
            </div>
            <div class="item-recommend-intro">
              <span>
                <span class="item-recommend-top-num">{{ index + 1 }}</span>
                热销{{ item.sale }}件</span
              >
              <span class="item-recommend-price"
                >￥{{ item.price.toFixed(2) }}</span
              >
            </div>
          </div>
        </div>
      </div>
      <div class="item-intro-detail" ref="itemIntroDetail">
        <div class="item-intro-nav item-tabs">
          <Tabs class="goods-tabs" v-model="tabsActive">
            <TabPane
              label="商品介绍"
              name="0"
              :class="{ 'goods-tabs-active': tabsActive === '0' }"
            >
              <div class="remarks-title  hidden-xs hidden-sm">
                <span>商品介绍</span>
              </div>
              <div class="item-intro-img" ref="itemIntroGoods">
                <p>{{ goodsDetail.detail_desc }}</p>
                <img
                  :src="item"
                  alt=""
                  v-for="(item, i) in getGoodsDetail.detailHtml"
                  :key="i"
                />
              </div>
            </TabPane>
            <!-- 规格参数展示 -->
            <TabPane
              label="规格参数"
              name="1"
              :class="{ 'goods-tabs-active': tabsActive === '1' }"
            >
              <div
                v-for="(item, index) in getGoodsDetail.specList"
                :key="index"
              >
                <div class="remarks-title  hidden-xs hidden-sm">
                  <span>{{ item.specType }}</span>
                </div>
                <div class="item-param-container">
                  <span
                    class="item-param-box"
                    v-for="(subItem, i) in item.list"
                    :key="i"
                  >
                    <span class="item-param-title">{{ subItem.name }}: </span>
                    <span class="item-param-content">{{ subItem.value }}</span>
                  </span>
                </div>
              </div>
            </TabPane>
            <TabPane
              label="售后保障"
              name="2"
              :class="{ 'goods-tabs-active': tabsActive === '2' }"
            >
              <ShowProductWarranty></ShowProductWarranty>
            </TabPane>
            <TabPane
              label="商品评价"
              name="3"
              :class="{ 'goods-tabs-active': tabsActive === '3' }"
            >
              <div class="remarks-container">
                <div class="remarks-title  hidden-xs hidden-sm">
                  <span>商品评价</span>
                </div>
                <div class="remarks-analyse-box">
                  <div class="remarks-analyse-goods">
                    <i-circle
                      :percent="getGoodsDetail.remarks.goodAnalyse"
                      stroke-color="#e4393c"
                    >
                      <span class="remarks-analyse-num"
                        >{{ getGoodsDetail.remarks.goodAnalyse }}%</span
                      >
                      <p class="remarks-analyse-title">好评率</p>
                    </i-circle>
                  </div>
                  <div class="remarks-analyse-tags">
                    <Tag
                      checkable
                      :color="tagsColor[index % 4]"
                      v-for="(item, index) in getGoodsDetail.remarks
                        .remarksTags"
                      :key="index"
                      >{{ item }}</Tag
                    >
                  </div>
                </div>
                <div class="remarks-bar">
                  <span
                    >追评({{
                      getGoodsDetail.remarks.remarksNumDetail[0]
                    }})</span
                  >
                  <span
                    >好评({{
                      getGoodsDetail.remarks.remarksNumDetail[1]
                    }})</span
                  >
                  <span
                    >中评({{
                      getGoodsDetail.remarks.remarksNumDetail[2]
                    }})</span
                  >
                  <span
                    >差评({{
                      getGoodsDetail.remarks.remarksNumDetail[3]
                    }})</span
                  >
                </div>
                <div
                  class="remarks-box"
                  v-for="(item, index) in getGoodsDetail.remarks.detail"
                  :key="index"
                >
                  <div class="remarks-user">
                    <Avatar icon="person" />
                    <span class="remarks-user-name">{{ item.username }}</span>
                  </div>
                  <div class="remarks-content-box">
                    <p>
                      <Rate
                        disabled
                        :value="item.values"
                        allow-half
                        class="remarks-star"
                      ></Rate>
                    </p>
                    <p class="remarks-content">{{ item.content }}</p>
                    <p class="remarks-sub">
                      <span class="remarks-item">{{ item.goods }}</span>
                      <span class="remarks-time">{{ item.time }}</span>
                    </p>
                  </div>
                </div>
                <div class="remarks-page">
                  <Page
                    :total="40"
                    size="small"
                    show-elevator
                    show-sizer
                  ></Page>
                </div>
              </div>
            </TabPane>
          </Tabs>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ShowProductWarranty from "@/components/goodsDetail/ShowProductWarranty";
import store from "@/vuex/store";
import { mapState, mapGetters } from "vuex";
export default {
  name: "ShowGoodsDetail",
  data() {
    return {
      tabsActive: "0",
      tagsColor: ["blue", "green", "red", "yellow"]
    };
  },
  computed: {
    ...mapState(["goodsDetail"]),
    ...mapGetters(["merchantItem", "getGoodsDetail"])
  },
  updated() {
    this.$nextTick(() => {
      const father = this;
      // setTimeout(() => {
      let heightCss = window.getComputedStyle(father.$refs.itemIntroGoods)
        .height;
      console.log(heightCss);
      heightCss = parseInt(heightCss.substr(0, heightCss.length - 2)) + 89;
      father.$refs.itemIntroDetail.style.height = heightCss + "px";
      // }, 100);
      // setTimeout(() => {
      //   let heightCss = window.getComputedStyle(father.$refs.itemIntroGoods)
      //     .height;
      //   console.log(heightCss);
      //   heightCss = parseInt(heightCss.substr(0, heightCss.length - 2)) + 89;
      //   father.$refs.itemIntroDetail.style.height = heightCss + "px";
      // }, 2000);
    });
  },
  components: {
    ShowProductWarranty
  },
  methods: {
    // 跳转详情
    goDetail(item) {
      this.$router.push({
        path: "/goodsDetail",
        query: { goodsId: item.goodsId, merchantId: item.merchantId }
      });
    }
  },
  store
};
</script>

<style scoped>
/***************商品详情介绍和推荐侧边栏开始***************/
.item-intro-show {
  /* width: 80%; */
  margin: 15px auto;
  display: flex;
  flex-direction: row;
  background-color: #fff;
}
.item-intro-recommend {
  width: 200px;
  display: flex;
  flex-direction: column;
}
.item-intro-recommend-column {
  display: flex;
  flex-direction: column;
  box-shadow: 0px 0px 5px #999;
}
.item-recommend-title {
  width: 100%;
  height: 38px;
  font-size: 16px;
  line-height: 38px;
  color: #fff;
  background-color: #e4393c;
  box-shadow: 0px 0px 5px #e4393c;
  text-align: center;
}
.item-recommend-column {
  margin-top: 15px;
  border-color: red;
  border-width: 15px;
}
.item-recommend-intro {
  padding: 5px 15px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  font-size: 12px;
  color: #999;
  cursor: pointer;
}
.item-recommend-img {
  width: 80%;
  margin: 0px auto;
  cursor: pointer;
}
.item-recommend-img img {
  width: 100%;
}
.item-recommend-top-num {
  color: #fff;
  margin: 0px 2px;
  padding: 1px 5px;
  border-radius: 12px;
  background-color: #e4393c;
}
.item-recommend-price {
  color: #e4393c;
  font-weight: bolder;
}
.item-intro-detail {
  margin-left: 30px;
  width: calc(80vw - 300px);
  height: auto !important;
}
.item-intro-nav {
  width: 100%;
  /* height: 38px; */
  /* background-color: #F7F7F7; */
}
.item-intro-nav ul {
  margin: 0px;
  padding: 0px;
  list-style: none;
}
.item-intro-nav li {
  float: left;
  height: 100%;
  width: 120px;
  line-height: 38px;
  text-align: center;
  color: #e4393c;
}
.item-intro-nav li:first-child {
  background-color: #e4393c;
  color: #fff;
}
.item-intro-img {
  width: 100%;
}
.item-intro-img img {
  width: 100%;
}
/************* 商品参数 *************/
.item-param-container {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  justify-content: space-between;
}
.item-param-box {
  padding: 5px;
  padding-left: 30px;
  width: 240px;
  height: 36px;
  font-size: 14px;
  /* text-align: center; */
  /* background-color: #ccc; */
}
.item-param-title {
  color: #232323;
}
.item-param-content {
  color: #999;
}
.remarks-title {
  padding-left: 15px;
  height: 36px;
  font-size: 16px;
  font-weight: bolder;
  line-height: 36px;
  color: #666666;
  /* background-color: #F7F7F7; */
}
.remarks-analyse-box {
  padding: 15px;
  display: flex;
  align-items: center;
}
.remarks-analyse-goods {
  margin-left: 15px;
  margin-right: 15px;
}
.remarks-analyse-num {
  font-size: 26px;
}
.remarks-analyse-title {
  font-size: 12px;
  line-height: 20px;
}
.remarks-bar {
  padding-left: 15px;
  height: 36px;
  line-height: 36px;
  color: #666666;
  background-color: #f7f7f7;
}
.remarks-bar span {
  margin-right: 15px;
}
.remarks-box {
  padding: 15px;
  display: flex;
  flex-direction: row;
  border-bottom: 1px #ccc dotted;
}
.remarks-user {
  width: 180px;
}
.remarks-user-name {
  padding-left: 15px;
}
.remarks-content-box {
  width: calc(100% - 180px);
}
.remarks-star {
  background-color: #fff;
}
.remarks-content {
  font-size: 14px;
  color: #232323;
  line-height: 28px;
}
.remarks-sub {
  margin-top: 15px;
  color: #ccc;
}
.remarks-time {
  margin-left: 15px;
}
.remarks-page {
  margin: 15px;
  display: flex;
  justify-content: flex-end;
}
/***************商品详情介绍和推荐侧边栏结束***************/
</style>

<style>
/* 改变便签页样式 */
.ivu-tabs-ink-bar {
  background-color: #e4393c !important;
}
.item-tabs > .ivu-tabs > .ivu-tabs-bar .ivu-tabs-tab {
  border-radius: 0px;
  color: #999;
  height: 38px;
  /* background: #F7F7F7; */
}
.item-tabs > .ivu-tabs > .ivu-tabs-bar .ivu-tabs-tab-active {
  color: #fff;
  background-color: #e4393c;
}
.item-tabs > .ivu-tabs > .ivu-tabs-bar .ivu-tabs-tab-active:before {
  content: "";
  display: block;
  width: 100%;
  height: 1px;
  color: #fff;
  background: #f7f7f7;
  position: absolute;
  top: 0;
  left: 0;
}
.ivu-rate-star-full:before,
.ivu-rate-star-half .ivu-rate-star-content:before {
  color: #e4393c;
}
</style>

<style lang="less" scoped>
.goods-tabs {
  /deep/ .ivu-tabs-bar {
    border-bottom: 1px solid #e4393c;
  }
  /deep/ .ivu-tabs-tabpane {
    > div {
      display: none;
    }
    &.goods-tabs-active > div {
      display: block;
      visibility: visible;
    }
  }
}
@media (max-width: 992px) {
  .item-intro-show {
    width: 100%;
    .item-intro-detail {
      width: 100%;
      margin: 0;
      flex-wrap: wrap;
      height: auto !important;
      /deep/ .item-intro-nav {
        background: #fff;
        border: none;
      }
    }
  }
  .goods-tabs {
    /deep/ .ivu-tabs-bar {
      margin-bottom: 0;
      border-bottom: 1px solid #ed3f14;
      background: #fff;
      .ivu-tabs-tab {
        padding: 8px;
        margin-right: 0;
        background: #fff;
        &.ivu-tabs-tab-active {
          background-color: #e4393c;
        }
      }
      .ivu-tabs-nav-container {
        margin-bottom: 0;
      }
    }
    /deep/ .ivu-tabs-nav-scroll {
      .ivu-tabs-ink-bar {
        display: none;
      }
    }
  }
}
</style>
