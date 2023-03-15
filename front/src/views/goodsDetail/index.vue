<template>
  <div class="page-detail page-nav-bar page-footer-bar">
    <Sreach class="hidden-xs hidden-sm"></Sreach>
    <div class="shop-item-path hidden-xs hidden-sm">
      <div class="shop-nav-container container ">
        <Breadcrumb>
          <BreadcrumbItem to="/">首页</BreadcrumbItem>
          <BreadcrumbItem to="/goodsList">数码</BreadcrumbItem>
          <BreadcrumbItem to="/goodsList">手机</BreadcrumbItem>
          <BreadcrumbItem>MIUI/小米</BreadcrumbItem>
        </Breadcrumb>
      </div>
    </div>
    <div class="container">
      <!-- 商品信息展示 -->
      <ShowGoods></ShowGoods>
      <!-- 商品详细展示 -->
      <ShowGoodsDetail></ShowGoodsDetail>
      <Spin size="large" fix v-if="isLoading"></Spin>
    </div>
    <Footer />
  </div>
</template>

<script>
import Footer from "@/components/footer/Footer";
import Sreach from "@/components/Sreach";
import ShowGoods from "@/components/goodsDetail/ShowGoods";
import ShowGoodsDetail from "@/components/goodsDetail/ShowGoodsDetail";
import { mapState, mapActions } from "vuex";
export default {
  name: "GoodsDetail",
  beforeRouteEnter(to, from, next) {
    window.scrollTo(0, 0);
    next();
  },
  watch: {
    $route(n, o) {
      // 监听路由参数是否变化
      if (n.fullPath !== o.fullPath) {
        // methods中封装的加载数据函数
        this.loadGoodsInfo(this.$route.query.goodsId);
      }
    }
  },
  created() {
    console.log("---------------" + JSON.stringify(this.$route.query));
    this.loadGoodsInfo(this.$route.query.goodsId);
    this.getMerchantHotsalesAction(this.$route.query.merchantId);
    const data = {
      spuId: this.$route.query.goodsId,
      productCategoryId: this.$route.query.relCategory3Id
    };
    this.getPromotion(this.$route.query.goodsId);
    this.getDiscount(data);
  },
  data() {
    return {
      tagsColor: ["blue", "green", "red", "yellow"]
    };
  },
  methods: {
    ...mapActions([
      "loadGoodsInfo",
      "getMerchantHotsalesAction",
      "getPromotion",
      "getDiscount"
    ])
  },
  computed: {
    ...mapState(["goodsInfo", "isLoading"])
  },
  components: {
    ShowGoods,
    Sreach,
    ShowGoodsDetail,
    Footer
  }
};
</script>

<style scoped>
.shop-item-path {
  height: 38px;
  background-color: rgb(236, 235, 235);
  line-height: 38px;
  color: #2c2c2c;
}
.container {
  position: relative;
}
@media (max-width: 992px) {
  .container {
    padding: 0;
  }
}
</style>
