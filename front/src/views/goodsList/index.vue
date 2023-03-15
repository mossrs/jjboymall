<template>
  <div class="page-goods-list">
    <!-- 列表页搜索 BEGIN -->
    <div class="search-container">
      <i-input
        class="hidden-xs hidden-sm"
        v-model="searchData"
        size="large"
        icon="ios-search"
        placeholder="输入你想查找的商品"
      >
        <Button slot="append" icon="ios-search" @click="sreach"></Button>
      </i-input>
      <i-input
        class="hidden-lg hidden-md search-input"
        v-model="searchData"
        @on-enter="sreach"
        size="large"
        icon="ios-search"
        placeholder="输入你想查找的商品"
      >
      </i-input>
      <Tag
        class="hidden-xs hidden-sm"
        v-for="(item, index) in promotionTags"
        :key="index"
        closable
        @on-close="closeTags(index)"
        ><span @click="selectTags(index)">{{ item }}</span></Tag
      >
    </div>
    <!-- 列表页搜索 END -->
    <GoodsListNav class="hidden-xs hidden-sm"></GoodsListNav>
    <div class="container page-goods-list-container">
      <div class="bread-crumb hidden-xs hidden-sm">
        <Breadcrumb>
          <BreadcrumbItem to="/">
            <Icon type="ios-home-outline"></Icon> 首页
          </BreadcrumbItem>
          <BreadcrumbItem to="/goodsList?sreachData=">
            <Icon type="bag"></Icon>
            {{ searchItem }}
          </BreadcrumbItem>
          <!-- 被选中的查询条件展示 -->
          <Tag v-for="(item, index) in selectedCondtions" :key="index">
            <span>{{ item.specName }} : {{ item.optionName }}</span></Tag
          >
        </Breadcrumb>
      </div>
      <!-- 商品标签导航 -->
      <GoodsClassNav
        class="goods-select-nav"
        :searchConditionData="searchConditionData"
      ></GoodsClassNav>

      <!-- 商品展示容器 -->
      <div class="goods-box">
        <div class="as-box hidden-xs hidden-sm">
          <div class="item-as-title">
            <span>商品精选</span>
            <span>广告</span>
          </div>
          <div class="item-as" v-for="(item, index) in asItem" :key="index">
            <router-link
              :to="{
                path: '/goodsDetail',
                query: {
                  goodsId: item.goodsId,
                  merchantId: item.merchantId,
                  relCategory3Id: item.relCategory3Id
                }
              }"
            >
              <div class="item-as-img">
                <img :src="item.goodsImgs" alt="" @click="goDetail(item)" />
              </div>
              <div class="item-as-price">
                <span>
                  <Icon type="social-yen text-danger"></Icon>
                  <span class="seckill-price text-danger">{{
                    item.price.toFixed(2)
                  }}</span>
                </span>
              </div>
              <div class="item-as-intro">
                <span>{{ item.goodsName }}</span>
              </div>
              <div class="item-as-selled">
                已有<span>{{ item.salesNum }}</span
                >人购买
              </div>
            </router-link>
          </div>
        </div>
        <div class="goods-list-box">
          <div class="goods-list-tool">
            <ul class="clearfix">
              <li
                v-for="(item, index) in goodsTool"
                :key="index"
                @click="orderBy(item.en, index)"
              >
                <span :class="{ 'goods-list-tool-active': isAction[index] }"
                  >{{ item.title }} <Icon :type="icon[index]"></Icon
                ></span>
              </li>
            </ul>
          </div>

          <!-- 过滤、排序后的商品列表 -->
          <div class="goods-list">
            <router-link
              class="goods-show-info"
              v-for="(item, index) in goodsInfoByNameFilter"
              :key="index"
              tag="div"
              :to="{
                path: '/goodsDetail',
                query: {
                  goodsId: item.goodsId,
                  merchantId: item.merchantId,
                  relCategory3Id: item.relCategory3Id
                }
              }"
            >
              <div class="goods-show-img">
                <img :src="item.goodsImgs" />
              </div>
              <div class="goods-show-content">
                <div class="goods-show-price">
                  <span>
                    <Icon type="social-yen text-danger"></Icon>
                    <span class="seckill-price text-danger">{{
                      item.price.toFixed(2)
                    }}</span>
                  </span>
                </div>
                <div class="goods-show-detail multi-ellipsis--l2">
                  <span>{{ item.goodsName }}</span>
                </div>
                <div class="goods-show-num">
                  已有<span>{{ item.salesNum || 0 }}</span
                  >人购买
                </div>
                <div class="goods-show-seller">
                  <span>{{ item.merchantName }}</span>
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </div>

      <div class="goods-page">
        <Page
          :current="pageIndex"
          :pageSize="pageSize"
          :total="totalGoodNum"
          @on-change="changeGoodPage"
          show-sizer
        ></Page>
      </div>
    </div>
    <Footer></Footer>
    <Spin size="large" fix v-if="isLoading"></Spin>
  </div>
</template>

<script>
import GoodsListNav from "@/components/nav/GoodsListNav";
import GoodsClassNav from "@/components/nav/GoodsClassNav";
import Footer from "@/components/footer/Footer";
import store from "@/vuex/store";
import { mapState, mapActions, mapGetters, mapMutations } from "vuex";
export default {
  name: "GoodsList",
  beforeRouteEnter(to, from, next) {
    window.scrollTo(0, 0);
    next();
  },
  data() {
    return {
      searchItem: "",
      isAction: [false, false],
      isDesc: [false, false],
      icon: ["arrow-up-a", "arrow-up-a"],
      pageIndex: 1,
      pageSize: 30,
      pageSum: 10,
      searchKey: "",
      sortField: "",
      sortDesc: true,
      goodsTool: [
        { title: "销量", en: "salesNum" },
        { title: "价格", en: "price" }
      ],
      searchData: "",
      promotionTags: ["手机", "华为", "移动", "学生", "免息"]
    };
  },
  computed: {
    ...mapState(["totalGoodNum", "searchConditionData"]),
    ...mapState(["isLoading", "selectedCondtions"]),
    ...mapGetters([
      "goodsInfoByNameFilter",
      "asItem",
      "getterSelectedCondtions"
    ])
  },
  methods: {
    ...mapActions(["getGoodsByName", "getSearchCondition"]),
    ...mapMutations(["SET_GOODS_ORDER_BY"]),
    initList() {
      const data = {};
      const category1Id = this.$route.query.category1_id;
      if (
        category1Id !== null &&
        category1Id !== undefined &&
        category1Id !== ""
      ) {
        data.relCategory1Id = category1Id;
      }
      const category2Id = this.$route.query.category2_id;
      if (
        category2Id !== null &&
        category2Id !== undefined &&
        category2Id !== ""
      ) {
        data.relCategory2Id = category2Id;
      }
      const category3Id = this.$route.query.category3_id;
      if (
        category3Id !== null &&
        category3Id !== undefined &&
        category3Id !== ""
      ) {
        data.relCategory3Id = category3Id;
      }
      const productName = this.$route.query.sreachData;
      if (
        productName !== null &&
        productName !== undefined &&
        productName !== ""
      ) {
        data.productName = productName;
      }
      this.getSearchCondition(data);
      this.getGoodsByName(data);
    },
    // 改变页数
    changeGoodPage(value) {
      this.pageIndex = value;
      this.sreach(value);
    },
    orderBy(data, index) {
      this.isAction = [false, false];
      this.isAction[index] = true;
      this.isDesc[index] = !this.isDesc[index];
      this.pageIndex = 1;
      this.icon[index] = this.isDesc[index] ? "arrow-down-a" : "arrow-up-a";
      this.sortField = data;
      this.sortDesc = this.isDesc[index];
      this.sreach();
      this.SET_GOODS_ORDER_BY(data);
    },
    closeTags(index) {
      this.promotionTags.splice(index, 1);
    },
    selectTags(index) {
      this.searchData = this.promotionTags[index];
    },
    // 当前多条件查询
    sreach(index) {
      this.pageIndex = 1;
      console.log("---- index = ", index);
      if (
        index !== null &&
        index !== undefined &&
        index !== "" &&
        !isNaN(index)
      ) {
        this.pageIndex = index;
      }
      const data = {};
      const category1Id = this.$route.query.category1_id;
      if (
        category1Id !== null &&
        category1Id !== undefined &&
        category1Id !== ""
      ) {
        data.relCategory1Id = category1Id;
      }
      const category2Id = this.$route.query.category2_id;
      if (
        category2Id !== null &&
        category2Id !== undefined &&
        category2Id !== ""
      ) {
        data.relCategory2Id = category2Id;
      }
      const category3Id = this.$route.query.category3_id;
      if (
        category3Id !== null &&
        category3Id !== undefined &&
        category3Id !== ""
      ) {
        data.relCategory3Id = category3Id;
      }

      const productName = this.$route.query.sreachData;
      if (
        this.searchData !== null &&
        this.searchData !== undefined &&
        this.searchData !== ""
      ) {
        data.productName = this.searchData;
      } else if (
        productName !== null &&
        productName !== undefined &&
        productName !== ""
      ) {
        data.productName = productName;
      }

      if (this.sortField !== null && this.sortField !== "") {
        data.sortField = this.sortField;
      }
      if (this.sortDesc !== null) {
        data.sortDesc = this.sortDesc;
      }

      const optionIds = [];
      for (var option of this.selectedCondtions) {
        optionIds.push(option.optionId);
      }
      if (optionIds.length > 0) {
        data.specOptions = optionIds;
      }
      data.pageNum = this.pageIndex - 1;
      data.pageSize = this.pageSize;
      this.getGoodsByName(data);
    }
  },
  created() {
    this.initList();
  },
  mounted() {
    const queryName = this.$route.query.sreachData;
    // 优先匹配查询字段
    if (queryName !== null && queryName !== undefined && queryName !== "") {
      this.searchItem = queryName;
    } else {
      // 再进行分类的匹配
      this.searchItem = this.$route.query.categoryName;
    }
  },
  components: {
    GoodsListNav,
    GoodsClassNav,
    Footer
  },
  store
};
</script>

<style scoped>
.container {
  margin: 15px auto;
  /* width: 93%; */
  /* min-width: 1000px; */
}
.text-danger {
  color: #a94442;
}
.seckill-price {
  margin-right: 5px;
  font-size: 25px;
  font-weight: bold;
}
.goods-box {
  display: flex;
}
/* ---------------侧边广告栏开始------------------- */
.as-box {
  width: 200px;
  border: 1px solid #ccc;
}
.item-as-title {
  width: 100%;
  height: 36px;
  color: #b1191a;
  line-height: 36px;
  font-size: 18px;
}
.item-as-title span:first-child {
  margin-left: 20px;
}
.item-as-title span:last-child {
  float: right;
  margin-right: 15px;
  font-size: 10px;
  color: #ccc;
}
.item-as {
  width: 160px;
  margin: 18px auto;
}
.item-as-img {
  width: 160px;
  height: 160px;
  margin: 0px auto;
}
.item-as-img img {
  width: 100%;
}
.item-as-price span {
  font-size: 18px;
}
.item-as-intro {
  margin-top: 5px;
  font-size: 12px;
}
.item-as-selled {
  margin-top: 5px;
  font-size: 12px;
}
.item-as-selled span {
  color: #005aa0;
}
/* ---------------侧边广告栏结束------------------- */

/* ---------------商品栏开始------------------- */
.goods-list-box {
  margin-left: 15px;
  width: calc(100% - 215px);
}
.goods-list-tool {
  width: 100%;
  height: 38px;
  border: 1px solid #ccc;
  background-color: #f1f1f1;
}
.goods-list-tool ul {
  padding-left: 15px;
  list-style: none;
}
.goods-list-tool li {
  cursor: pointer;
  float: left;
}
.goods-list-tool span {
  padding: 5px 8px;
  border: 1px solid #ccc;
  border-left: none;
  line-height: 36px;
  background-color: #fff;
}
.goods-list-tool span:hover {
  border: 1px solid #e4393c;
}
.goods-list-tool i:hover {
  color: #e4393c;
}
.goods-list-tool-active {
  color: #fff;
  border-left: 1px solid #ccc;
  background-color: #e4393c !important;
}

.goods-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
}
.goods-show-info {
  width: 24%;
  padding: 10px;
  margin: 15px 1.33% 0 0;
  border: 1px solid #fff;
  cursor: pointer;
}
.goods-show-info:nth-child(4n) {
  margin-right: 0;
}
.goods-show-info:hover {
  border: 1px solid #ccc;
  box-shadow: 0px 0px 15px #ccc;
}
.goods-show-price {
  margin-top: 6px;
}
.goods-show-img img {
  width: 100%;
}
.goods-show-detail {
  font-size: 12px;
  margin: 6px 0px;
}
.goods-show-num {
  font-size: 12px;
  margin-bottom: 6px;
  color: #009688;
}
.goods-show-num span {
  color: #005aa0;
  font-weight: bold;
}
.goods-show-seller {
  font-size: 12px;
  color: #e4393c;
}
.goods-page {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
/* ---------------商品栏结束------------------- */

.search-container {
  padding-top: 15px;
  margin: 0px auto;
  margin-bottom: 15px;
  width: 460px;
}
.sreach {
  margin: 5px 0px;
}
</style>

<style lang="less" scoped>
.page-goods-list-container {
  min-height: calc(100vh - 630px);
}
@media (max-width: 992px) {
  .page-goods-list {
    background: #fff;
  }
  .search-container {
    width: 100%;
    padding: 10px 10px 0;
    .search-input {
      width: 100%;
      /deep/ .ivu-input {
        border-radius: 20px;
        border: none;
        background: #f2f2f7;
      }
    }
  }
  .container {
    margin: 0;
    padding: 0 0 15px 0;
    background: #fff;
  }
  .goods-select-nav {
    position: relative;
    top: 34px;
    min-height: 52px;
  }
  .goods-list-box {
    margin-left: 0;
    width: 100%;
    .goods-list-tool {
      position: relative;
      top: -57px;
    }
    .goods-show-info {
      width: 100%;
      padding: 0;
      display: flex;
      padding: 6px 0;
      margin: 0;
      border-bottom: 1px solid #e5e5e5;
      .goods-show-img {
        width: 120px;
        height: 120px;
        flex-shrink: 0;
      }
      .goods-show-content {
        flex-grow: 1;
        position: relative;
        margin-left: 5px;
        .goods-show-price {
          position: absolute;
          top: 30px;
        }
        .goods-show-detail {
          height: 32px;
          margin-bottom: 30px;
        }
      }
    }
  }
  .goods-page {
    justify-content: center;
    /deep/ .ivu-page-options {
      display: none;
    }
  }
}
</style>
