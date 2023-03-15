<template>
  <div class="container">
    <div class="nav-item hidden-xs hidden-sm col-md-offset-2">
      <ul class="clearfix">
        <li v-for="(item,index) in nav" :key="index">
          <a href="#">{{item}}</a>
        </li>
      </ul>
    </div>
    <div class="nav-body clearfix">
      <!-- 侧边导航 -->
      <div class="nav-side col-md-2 hidden-xs hidden-sm" ref="navSide">
        <router-link
          :to="{ path: '/goodsList', query: {category1_id:cate.id,categoryName:cate.name}}"
          v-for="(cate, index) in categoryList"
          :key="index"
        >
          <ul>
            <li @mouseenter="showDetail(index)" @mouseleave="hideDetail()">
              <span class="nav-side-item">{{cate.name}}</span>
            </li>
          </ul>
        </router-link>
      </div>
      <div class="nav-content clearfix col-md-10 col-xs-12 col-sm-12">
        <!-- 幻灯片 -->
        <Carousel autoplay loop>
          <CarouselItem v-for="(item, index) in marketing.CarouselItems" :key="index">
            <router-link :to="{path: '/goodsList', query: { sreachData: '电脑'}}">
              <img class="nav-content-carousel-img" :src="item" />
            </router-link>
          </CarouselItem>
        </Carousel>
        <div class="nav-show hidden-xs hidden-sm row">
          <div
            class="nav-show-img col-md-6"
            v-for="(item, index) in marketing.activity"
            :key="index"
          >
            <router-link :to="{path: '/goodsList', query: { sreachData: '电脑'}}">
              <img :src="item" />
            </router-link>
          </div>
        </div>
      </div>
    </div>
    <!-- 菜单栏 -->
    <transition name="fade" v-for="(first, index) in categoryList" :key="index">
      <div
        class="detail-item-panel"
        :duration="{ enter: 100, leave: 100 }"
        v-show="actionNav ===index"
        @mouseenter="showDetail(index)"
        :ref="index"
        :style="{left: left + 'px', top: top + 'px'}"
        @mouseleave="hideDetail()"
      >
        <div class="nav-detail-item">
          <router-link
            :to="{ path: '/goodsList', query: {category2_id:second.id,categoryName:second.name}}"
            v-for="(second, index2) in first.list"
            :key="index2"
          >
            <span>{{second.name}}></span>
          </router-link>
        </div>
        <ul>
          <router-link
            :to="{ path: '/goodsList', query: {category2_id:second.id}}"
            v-for="(second, index2) in first.list"
            :key="index2"
          >
            <li class="detail-item-row">
              <span class="detail-item-title">
                {{second.name}}
                <span class="glyphicon glyphicon-menu-right"></span>
              </span>
              <router-link
                :to="{ path: '/goodsList', query: {category3_id:third.id,categoryName:third.name}}"
                v-for="(third, subIndex) in second.list"
                :key="subIndex"
              >
                <span class="detail-item">{{third.name}}</span>
              </router-link>
            </li>
          </router-link>
        </ul>
      </div>
    </transition>
  </div>
</template>

<script>
import store from '@/vuex/store'
import { mapActions, mapGetters, mapState } from 'vuex'
export default {
  name: 'HomeNav',
  data() {
    return {
      left: 0,
      top: 0,
      actionNav: -1,
      nav: [
        '秒杀',
        '优惠券',
        '闪购',
        '拍卖',
        '服装城',
        '超市',
        '生鲜',
        '全球购',
        '金融'
      ]
    }
  },
  created() {
    this.getCategoryList()
  },
  computed: {
    ...mapState(['marketing', 'categoryList']),
    ...mapGetters(['getterCategoryList'])
  },
  methods: {
    ...mapActions(['getCategoryList']),
    showDetail(index) {
      this.actionNav = index
    },
    hideDetail() {
      this.actionNav = -1
    }
  },
  updated() {
    this.left = this.$refs.navSide.offsetLeft + this.$refs.navSide.offsetWidth
    this.top = this.$refs.navSide.offsetTop
  },
  store
}
</script>

<style scoped>
.nav-item {
  padding-left: 15px;
  height: 36px;
}
.nav-item ul {
  list-style: none;
}
.nav-item li {
  float: left;
  font-size: 16px;
  font-weight: bold;

  margin-right: 30px;
}
.nav-item a {
  text-decoration: none;
  color: #555555;
}
.nav-item a:hover {
  color: #d9534f;
}
/*大的导航信息，包含导航，幻灯片等*/
.nav-body {
  /* width: 1020px;
  height: 485px; */
  margin: 0px auto;
  margin-bottom: 15px;
  margin-top: 15px;
  display: flex;
}
.nav-side {
  /* width: 200px; */
  /* height: 100%; */
  padding: 0px;
  color: #fff;
  float: left;
  background-color: #6e6568;
}

.nav-side a {
  color: #fff;
}

.nav-side ul {
  width: 100%;
  padding: 0px;
  padding-top: 15px;
  list-style: none;
}
.nav-side li {
  padding: 7.5px;
  padding-left: 15px;
  font-size: 14px;
  line-height: 18px;
}
.nav-side li:hover {
  background: #999395;
}
.nav-side-item:hover {
  cursor: pointer;
  color: #c81623;
}

/*导航图片*/
.nav-show-img {
  margin-top: 10px;
}

/*显示商品*/
.content {
  width: 100%;
}
/*显示商品详细信息*/
.detail-item-panel {
  width: 815px;
  height: 485px;
  background-color: #fff;
  position: absolute;
  top: 168px;
  left: 389px;
  z-index: 999;
}
.nav-detail-item {
  margin-left: 26px;
  margin-top: 15px;
  margin-bottom: 15px;
  cursor: pointer;
  color: #eee;
}
.nav-detail-item a {
  color: #fff;
}
.nav-detail-item span {
  padding: 6px;
  padding-left: 12px;
  margin-left: 15px;
  font-size: 12px;
  background-color: #6e6568;
}
.nav-detail-item span:hover {
  margin-left: 15px;
  background-color: #f44336;
}
.detail-item-panel ul {
  list-style: none;
}
.detail-item-panel li {
  line-height: 38px;
  margin-left: 40px;
}
.detail-item-title {
  padding-right: 6px;
  font-weight: bold;
  font-size: 12px;
  cursor: pointer;
  color: #555555;
}
.detail-item-title:hover {
  color: #d9534f;
}
.detail-item-row a {
  color: #555555;
}
.detail-item {
  font-size: 14px;
  padding-left: 12px;
  padding-right: 8px;
  cursor: pointer;
  border-left: 1px solid #ccc;
}
.detail-item:hover {
  color: #d9534f;
}
</style>


<style lang="less" scoped>
@media (max-width: 768px) {
  .nav-content {
    border-radius: 7px;
    height: 135px;
    overflow: hidden;
    margin: 0;
    padding: 0;
    .nav-content-carousel-img {
      width: 100%;
      height: 135px;
    }
  }
}

@media (min-width: 992px) {
  .nav-content {
    padding-right: 0;
    .nav-content-carousel-img {
      width: 100%;
      height: 345px;
    }
    .nav-show-img:nth-child(1) {
      padding-right: 7.5px;
    }
    .nav-show-img:nth-child(2) {
      padding-left: 7.5px;
    }
    .nav-show-img img {
      width: 100%;
    }
  }
}
</style>