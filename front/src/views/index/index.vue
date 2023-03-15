<template>
  <div class="page-index">
    <Sreach></Sreach>
    <HomeNav></HomeNav>
    <div class="container">
      <!-- 秒杀 -->
      <div class="seckill">
        <!-- 头部 -->
        <div class="seckill-head">
          <div class="seckill-icon">
            <img src="static/img/index/clock.png" />
          </div>
          <div class="seckill-text">
            <span class="seckill-title">限时秒杀</span>
            <span class="seckill-remarks hidden-xs hidden-sm">总有你想不到的低价</span>
          </div>
          <div class="count-down">
            <span class="count-down-text">当前场次</span>
            <span class="count-down-info">
              <span class="count-down-num count-down-hour">{{ seckillsHours }}</span>
              <span class="count-down-point">:</span>
              <span class="count-down-num count-down-minute">{{ seckillsMinutes }}</span>
              <span class="count-down-point">:</span>
              <span class="count-down-num count-down-seconds">{{ seckillsSeconds }}</span>
              <span class="count-down-text">后结束抢购</span>
            </span>
          </div>
        </div>
        <!-- 内容 -->
        <div class="seckill-content clearfix">
          <div
            class="seckill-item col-xs-6"
            v-for="(item, index) in seckills.goodsList"
            :key="index"
          >
            <div class="seckill-item-content">
              <div class="seckill-item-img">
                <router-link to="/goodsList">
                  <img :src="item.img" />
                </router-link>
              </div>
              <div class="seckill-item-info">
                <p>{{ item.intro }}</p>
                <p>
                  <span class="seckill-price text-danger">
                    <Icon type="social-yen"></Icon>
                    {{ item.price }}
                  </span>
                  <span class="seckill-old-price">
                    <s>{{ item.realPrice }}</s>
                  </span>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 新品推荐商品 -->
      <div class="item-class-new">
        <div class="item-class-head-new">
          <span class="item-class-title-new">新品推荐</span>
        </div>
        <div class="item-class-content-new">
          <div class="item-content-top-new">
            <div class="item-four-img-new clearfix">
              <div class="item-four-detail col-xs-6" v-for="(item, index) in news" :key="index">
                <div class="item-four-detail-text-subject">
                  <p class="pt_bi_tit_new">{{ item.product_name }}</p>
                  <div class="price-item-info-subject">
                    <Icon type="social-yen"></Icon>
                    {{ item.price }}
                  </div>
                </div>
                <div class="item-four-detail-img">
                  <router-link
                    :to="{
                      path: '/goodsDetail',
                      query: {
                        goodsId: item.id,
                        merchantId: 1,
                        relCategory3Id: item.rel_category3_id
                    }
                    }"
                  >
                    <img :src="item.default_pic" alt />
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 人气热搜商品 -->
      <div class="item-class-new">
        <div class="item-class-head-recommends">
          <span class="item-class-title-new">人气热搜</span>
        </div>
        <div class="item-class-content-new">
          <div class="item-content-top-new clearfix">
            <div class="item-four-img-new">
              <div
                class="item-four-detail col-xs-6"
                v-for="(item, index) in popRecommends"
                :key="index"
              >
                <div class="item-four-detail-text-subject">
                  <p class="pt_bi_tit_new">{{ item.product_name }}</p>
                  <div class="price-item-info-subject">
                    <Icon type="social-yen"></Icon>
                    {{ item.price }}
                  </div>
                </div>
                <div class="item-four-detail-img">
                  <router-link
                    :to="{
                      path: '/goodsDetail',
                      query: {
                        goodsId: item.id,
                        merchantId: 1,
                        relCategory3Id: item.rel_category3_id
                    }
                    }"
                  >
                    <img :src="item.default_pic" alt />
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 专题广场 -->
      <h3 class="floorhd_tit">专题广场</h3>

      <div class="item-class" v-for="(item1, index1) in recommendSubjects" :key="index1">
        <div class="item-class-head">
          <span class="item-class-title">{{ item1.title }}</span>
          <ul>
            <li v-for="(item2, index2) in item1.hotWordList" :key="index2">
              <router-link :to="{ path: '/goodsList', query: { sreachData: item2 } }">{{ item2 }}</router-link>
            </li>
          </ul>
        </div>
        <div class="item-class-content">
          <div class="item-content-top row">
            <div class="item-big-img col-md-2 visible-md-block visible-lg-block">
              <router-link class="link" :to="{ path: '/goodsList', query: { sreachData: '电脑' } }">
                <img :src="item1.pic" alt />
              </router-link>
            </div>
            <div class="col-xs-12 col-md-10">
              <div class="item-four-img">
                <div
                  class="item-four-detail col-xs-6"
                  v-for="(subItem, index) in item1.productList"
                  :key="index"
                >
                  <div class="item-four-detail-text-subject">
                    <p class="pt_bi_tit_new">{{ subItem.product_name }}</p>
                    <div class="price-item-info-subject">
                      <Icon type="social-yen"></Icon>
                      {{ subItem.price }}
                    </div>
                  </div>
                  <div class="item-four-detail-img">
                    <router-link
                      :to="{
                      path: '/goodsDetail',
                      query: {
                        goodsId: subItem.id,
                        merchantId: 1,
                        relCategory3Id: subItem.relCategory3Id
                    }
                    }"
                    >
                      <img :src="subItem.default_pic" alt />
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <goods-list-layout sreach-data="电脑" :goods-list="item1.albumPicList" />
      </div>

      <!-- 为你推荐 -->
      <h3 class="floorhd_tit">为你推荐</h3>
    </div>
    <Footer></Footer>
    <footer-bar :active-index="0" />
  </div>
</template>

<script>
import footerBar from '@/components/footerBar'
import goodsListLayout from '@/components/goodsListLayout'
import Sreach from '@/components/Sreach'
import HomeNav from '@/components/nav/HomeNav'
import Footer from '@/components/footer/Footer'
import store from '@/vuex/store'
import { mapState, mapActions, mapGetters, mapMutations } from 'vuex'
export default {
  created() {
    window.scrollTo(0, 0)
    this.loadSeckillsInfo()
    this.loadCarouselItems()
    this.loadEat()
    this.loadShoppingCart()
    // this.loadHomeData()
    this.loadNews()
    this.loadPopRecommends()
    this.loadRecommendSubjects()
  },
  mounted() {
    const father = this
    this.setIntervalObj = setInterval(function() {
      father.REDUCE_SECKILLS_TIME()
    }, 1000)
  },
  data() {
    return {
      setIntervalObj: null
    }
  },
  methods: {
    ...mapActions([
      'loadSeckillsInfo',
      'loadCarouselItems',
      'loadComputer',
      'loadEat',
      'loadShoppingCart',
      'loadNews',
      'loadPopRecommends',
      'loadRecommendSubjects',
      'loadHomeData'
    ]),
    ...mapMutations(['REDUCE_SECKILLS_TIME'])
  },
  computed: {
    ...mapState([
      'seckills',
      'computer',
      'eat',
      'news',
      'popRecommends',
      'recommendSubjects'
    ]),
    ...mapGetters(['seckillsHours', 'seckillsMinutes', 'seckillsSeconds'])
  },
  components: {
    Sreach,
    HomeNav,
    Footer,
    footerBar,
    goodsListLayout
  },
  destroyed() {
    clearInterval(this.setIntervalObj)
  },
  store
}
</script>

<style scoped>
.container {
  /* background-color: #f6f6f6; */
}
.content {
  /* width: 1008px; */
  margin: 0px auto;
}
/*****************************秒杀专栏开始*****************************/
/*秒杀专栏*/
.seckill {
  width: 100%;
  background-color: #fff;
}
.seckill-head {
  width: 100%;
  height: 50px;
  background-color: #e01222;
}
.seckill-icon {
  width: 68px;
  height: 100%;
  float: left;
}
.seckill-icon img {
  width: 35px;
  height: 35px;
  margin-top: 6px;
  margin-left: 15px;
  animation-name: shake-clock;
  animation-duration: 0.3s;
  animation-iteration-count: infinite; /*设置无线循环*/
}
/*定义闹钟震动动画关键帧*/
@keyframes shake-clock {
  0% {
    transform: rotate(-8deg);
  }
  50% {
    transform: rotate(8deg);
  }
  100% {
    transform: rotate(-8deg);
  }
}
.seckill-text {
  width: 300px;
  height: 100%;
  float: left;
}
.seckill-text .seckill-title {
  font-size: 22px;
  line-height: 50px;
  color: #fff;
}
.seckill-text .seckill-remarks {
  margin-left: 5px;
  font-size: 10px;
  color: #fff;
}
/*倒计时*/
.count-down {
  height: 100%;
  margin-right: 30px;
  line-height: 50px;
  float: right;
}
.count-down-text {
  color: #fff;
}
.count-down-num {
  padding: 3px;
  border-radius: 5px;
  background-color: #440106;
  font-size: 26px;
  font-weight: bold;
  color: #f90013;
}
.count-down-point {
  font-size: 26px;
  font-weight: bold;
  color: #440106;
}

.seckill-content {
  width: 100%;
}
.seckill-item {
  /* height: 250px; */
  padding: 15px;
  cursor: pointer;
  float: left;
}
.seckill-item-img {
  /* width: 160px; */
  height: 160px;
  margin: 0px auto;
  overflow: hidden;
  border-bottom: 1px solid #ccc;
  background-color: #fff;
}
.seckill-item-img img {
  width: 130px;
  height: 130px;
  margin-left: 15px;
  margin-top: 15px;
  transition: margin-top 0.3s;
}
.seckill-item-img:hover img {
  margin-top: 6px;
  transition: margin-top 0.3s;
}
.seckill-item-info {
  padding: 5px;
  padding-left: 15px;
  padding-right: 15px;
  font-size: 12px;
  color: #009688;
}
.seckill-item-info p {
  max-height: 36px;
  overflow: hidden;
}
.seckill-item-info i:first-child {
  font-size: 14px;
}
.seckill-price {
  margin-right: 5px;
  font-size: 25px;
  font-weight: bold;
}
.seckill-item-content {
  box-shadow: 0px 0px 8px #ccc;
}
/*****************************秒杀专栏结束*****************************/

/*****************************商品专栏开始*****************************/
.item-class {
  width: 100%;
  margin-top: 15px;
  background-color: #fff;
}
.item-class-head {
  width: 100%;
  height: 50px;
  background-color: #4488a7;
}
.item-class-eat-head {
  background-color: #ecb226;
}
.item-class-head ul {
  list-style: none;
  float: right;
  margin-right: 30px;
  line-height: 50px;
}
.item-class-head a {
  padding: 6px;
  margin-left: 15px;
  font-size: 12px;
  background-color: #6da6be;
  border: 1px solid #6da6be;
  text-decoration: none;
  color: #fff;
}
.item-class-eat-head a {
  background-color: #eeb955;
  border: 1px solid #eeb955;
}
.item-class-head a:hover {
  border: 1px solid #fff;
}
.item-class-head li {
  float: left;
}
.item-class-title {
  font-size: 25px;
  line-height: 50px;
  color: #fff;
  margin-left: 15px;
}
.item-class-content {
  width: 100%;
  cursor: pointer;
  /*border-right: 1px solid #ccc;*/
  /* margin-left: 0.9%; */
  /*background-color: #cff;*/
}
.item-class-content:nth-child(odd) {
  border: none;
}
.item-big-img {
  overflow: hidden;
  float: left;
}
.item-big-img img {
  margin-left: 0px;
  transition: margin-left 0.3s;
  width: 100%;
  height: 100%;
}
.item-big-img:hover img {
  margin-left: -15px;
  transition: margin-left 0.3s;
}
/* .item-four-img {
  width: 80%;
  margin-left: 8px;
  float: left;
} */
.item-four-detail img {
  margin-left: 0px;
  transition: margin-left 0.3s;
  width: 100%;
  height: 100%;
}
.item-four-detail:hover img {
  margin-left: -6px;
  transition: margin-left 0.3s;
}
.item-four-detail {
  /* width: 160px; */
  height: 130px;
  margin-left: 0px;
  float: left;
  border-top: 1px solid #ccc;
  border-left: 1px solid #ccc;
  border-right: 1px solid #ccc;
  border-bottom: 1px solid #ccc;
}
.item-four-detail:first-child {
  border-right: 1px solid #ccc;
  border-bottom: 1px solid #ccc;
}
.item-four-detail:last-child {
  border-top: 1px solid #ccc;
  border-left: 1px solid #ccc;
}
.item-four-detail-text {
  width: 50px;
  margin-left: 5px;
  margin-top: 15px;
  float: left;
}
.item-four-detail-img {
  width: 96px;
  margin-top: 15px;
  overflow: hidden;
  float: left;
}
.item-four-detail-img img {
  margin-left: 5px;
  width: 90px;
}
.pt_bi_tit {
  font-weight: bold;
  font-size: 12px;
  color: #4488a7;
}
.pt_bi_tit-eat {
  color: #ecb127;
}
.pt_bi_promo {
  color: #00695c;
}
.item-content-bottom {
  width: 100%;
  margin-top: 8px;
}
.item-content-bottom-img {
  width: 192px;
  margin-right: 8px;
  overflow: hidden;
  float: left;
}
.item-content-bottom-img img {
  margin-left: 0px;
  transition: margin-left 0.3s;
}
.item-content-bottom-img:hover img {
  margin-left: -15px;
  transition: margin-left 0.3s;
}
/*****************************商品专栏结束*****************************/

/*****************************新品推荐开始*****************************/

.pt_bi_tit_new {
  font-weight: bold;
  font-size: 12px;
  color: #4488a7;
  height: 70px;
  overflow: hidden;
}

.pt_bi_promo_new {
  color: #00695c;
}

.item-class-new {
  width: 100%;
  margin-top: 15px;
  background-color: #fff;
}

.item-class-head-new {
  width: 100%;
  height: 50px;
  background-color: #ff4400d4;
}

.item-class-title-new {
  font-size: 25px;
  line-height: 50px;
  color: #fff;
  margin-left: 15px;
}

.item-class-content-new:nth-child(odd) {
  border: none;
}
.item-content-top-new {
  width: 100%;
}
.item-big-img-new {
  width: 180px;
  overflow: hidden;
  float: left;
}
.item-big-img-new img {
  margin-left: 0px;
  transition: margin-left 0.3s;
}
.item-big-img-new:hover img {
  margin-left: -15px;
  transition: margin-left 0.3s;
}
.item-four-img-new {
  width: 100%;
  /* margin-left: 8px;
  margin-top: 5px; */
  /* float: left; */
}
.item-four-detail-new img {
  margin-left: 0px;
  transition: margin-left 0.3s;
}
.item-four-detail-new:hover img {
  margin-left: -6px;
  transition: margin-left 0.3s;
}
.item-four-detail-new {
  /* width: 198px;
  height: 130px; */
  margin-left: 0px;
  float: left;
  border-left: 1px solid #ccc;
  border-right: 1px solid #ccc;
  border-bottom: 1px solid #ccc;
}
.item-four-detail-new:first-child {
  border-right: 1px solid #ccc;
  border-bottom: 1px solid #ccc;
}
.item-four-detail-new:last-child {
  border-top: 1px solid #ccc;
  border-left: 1px solid #ccc;
}
.item-four-detail-text {
  width: 70px;
  margin-left: 5px;
  margin-top: 15px;
  float: left;
}
.item-four-detail-img-new {
  width: 120px;
  margin-top: 15px;
  overflow: hidden;
  float: left;
}
.item-four-detail-img-new img {
  margin-left: 5px;
  width: 105px;
}

.item-four-detail-text-new {
  width: 70px;
  margin-left: 5px;
  margin-top: 15px;
  float: left;
}

.price-item-info-new {
  padding: 5px;
  padding-left: 5px;
  font-size: 18px;
  color: #009688;
}

.item-four-detail-text-subject {
  width: 50px;
  margin-top: 15px;
}

.price-item-info-subject {
  padding: 5px 0;
  font-size: 12px;
  color: #009688;
}

/*****************************新品推荐结束*****************************/

.item-class-subject {
  width: 100%;
  margin-top: 15px;
  background-color: #fff;
}
.ivu-layout-header {
  background-color: #f6f6f6;
  height: 130px;
}

.item-class-head-recommends {
  width: 100%;
  height: 50px;
  background-color: #8200ff87;
}
.line {
  height: 0;
  border-top: 1px solid #000;
  text-align: center;
}
.text {
  position: relative;
  top: -14px;
  background-color: rgba(255, 255, 255, 0.99);
  position: relative;
  width: 150px;
  height: 45px;
  font-size: 28px;
  font-weight: 700;
  text-align: center;
  line-height: 45px;
  padding: 0 30px;
  margin: 0 auto 20px;
  overflow: hidden;
  color: #333;
}

.floorhd_tit {
  position: relative;
  width: 200px;
  height: 45px;
  font-size: 28px;
  font-weight: 700;
  text-align: center;
  line-height: 45px;
  padding: 0 30px;
  margin: 0 auto 20px;
  overflow: hidden;
  color: #333;
  margin-top: 10px;
}

.floorhd_tit:before {
  content: '';
  position: absolute;
  top: 50%;
  margin-top: -10px;
}

.floorhd_tit:before {
  background-image: url(//misc.360buyimg.com/mtd/pc/index_2019/1.0.0/assets/sprite/floor_hd/sprite.png);
  background-position: 0 0;
  width: 25px;
  height: 20px;
  left: 0;
}
.floorhd_tit:after {
  content: '';
  position: absolute;
  top: 50%;
  margin-top: -10px;
}

.floorhd_tit:after {
  background-image: url(//misc.360buyimg.com/mtd/pc/index_2019/1.0.0/assets/sprite/floor_hd/sprite.png);
  background-position: -25px 0;
  width: 25px;
  height: 20px;
  right: 0;
}
</style>

<style lang="less" scoped>
.item-four-detail {
  display: flex;
  .item-four-detail-text-subject {
    flex-grow: 1;
  }
  .item-four-detail-img {
    flex-shrink: 0;
  }
}
.item-big-img {
  height: 260px;
  overflow: hidden;
  margin-left: 15px;
  margin-right: -15px;
}
.item-big-img .link {
  width: 100%;
  height: 100%;
  display: block;
  overflow: hidden;
}
@media (min-width: 992px) {
  .item-four-detail-new,
  .seckill-item,
  .item-four-detail {
    width: 20%;
  }
}
@media (max-width: 992px) {
  .page-index {
    padding: 44px 0 50px 0;
  }
  .seckill-head {
    display: flex;
    align-items: center;
    .seckill-icon {
      width: auto;
      height: 20px;
      margin-right: 3px;
      img {
        margin-top: 0;
        width: 20px;
        height: 20px;
      }
    }
    .seckill-text {
      width: auto;
      .seckill-title {
        font-size: 14px;
        font-weight: 400;
      }
    }
    .count-down {
      display: inline-flex;
      border: 1px solid #fff;
      border-radius: 10px;
      height: 20px;
      line-height: 20px;
      vertical-align: middle;
      margin-left: 5px;
      padding-left: 7px;
      .count-down-info {
        height: 18px;
        line-height: 18px;
        background: #fff;
        margin-left: 7px;
        padding-right: 7px;
        padding-left: 7px;
        border-top-right-radius: 10px;
        border-bottom-right-radius: 10px;
        .count-down-text,
        .count-down-point,
        .count-down-num {
          padding: 0;
          font-size: 12px;
          color: #f2270c;
          background-color: transparent;
        }
      }
    }
  }
  .seckill-item {
    margin-bottom: 15px;
  }
}
@media (max-width: 1200px) {
  .seckill-content {
    .seckill-item {
      padding: 0;
      &:nth-child(2n) {
        padding-left: 7.5px;
      }
      &:nth-child(2n - 1) {
        padding-right: 7.5px;
      }
    }
  }
}
</style>
