<template>
  <div class="wrap page-footer-bar page-nav-bar">
    <nav-bar title="全部分类" left-arrow></nav-bar>
    <div class="category">
      <div class="menu-wrapper" ref="menuWrapper">
        <div class="menu-list">
          <div
            v-for="(item, index) in category"
            :key="index"
            class="menu-item"
            :class="{ current: currentIndex === index }"
            @click="selectIndex(index, $event)"
          >
            <div class="text-wrapper">
              <span class="text">{{ item.name }}</span>
            </div>
          </div>
        </div>
      </div>
      <div class="cls-wrapper bgfff" ref="clsWrapper">
        <ul class="cls-list">
          <li v-for="(item, index) in category" :key="index" class="cls-item hairline--bottom">
            <div v-for="(item2, index) in item.list" :key="index">
              <div class="item-name">{{ item2.name }}</div>
              <div class="item-content clearfix">
                <router-link
                  v-for="item3 in item2.list"
                  :key="item3.id"
                  class="col-xs-4 ellipsis"
                  tag="div"
                  :to="{ path: '/goodsList', query: {category1_id:item3.id,categoryName:item3.name}}"
                >{{ item3.name }}</router-link>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
    <footer-bar :active-index="1" />
  </div>
</template>

<script>
import { categoryList } from '@/api/baseApi'
import footerBar from '@/components/footerBar'
import navBar from '@/components/navBar'
import BScroll from 'better-scroll'
export default {
  components: {
    navBar,
    footerBar
  },
  data() {
    return {
      category: [],
      heightList: [],
      scrollY: 0,
      currentIndex: 0,
      timestamp: new Date().getTime()
    }
  },
  watch: {
    scrollY() {
      if (new Date().getTime() - this.timestamp > 500) {
        for (let i = 0; i < this.heightList.length; i++) {
          let height1 = this.heightList[i]
          let height2 = this.heightList[i + 1]
          if (!height2 || (this.scrollY >= height1 && this.scrollY < height2)) {
            this.currentIndex = i
            return
          }
        }
        this.currentIndex = 0
      }
    }
  },
  methods: {
    selectIndex($index, $event) {
      if (!$event._constructed) {
        return
      }
      this.timestamp = new Date().getTime()
      this.currentIndex = $index
      let clsList = this.$refs.clsWrapper.getElementsByClassName('cls-item')
      this.clsScroll.scrollToElement(clsList[$index], 300)
    },
    initscroll() {
      this.menuScroll = new BScroll(this.$refs.menuWrapper, {
        click: true
      })
      this.clsScroll = new BScroll(this.$refs.clsWrapper, {
        probeType: 3,
        click: true
      })
      this.clsScroll.on('scroll', pos => {
        this.scrollY = Math.abs(Math.round(pos.y))
      })
    },
    caculateHeight() {
      let clsList = this.$refs.clsWrapper.getElementsByClassName('cls-item')
      let height = 0
      this.heightList.push(height)
      for (let i = 0; i < clsList.length; i++) {
        let item = clsList[i]
        height += item.clientHeight
        this.heightList.push(height)
      }
    }
  },
  created() {
    categoryList().then(res => {
      if (res.code === 200) {
        this.category = res.data
        this.$nextTick(() => {
          this.initscroll()
          this.caculateHeight()
        })
      }
    })
  }
}
</script>

<style lang="less" scoped>
.category {
  display: flex;
  position: absolute;
  top: 44px;
  bottom: 0;
  left: 0;
  right: 0;
  width: 100%;
  overflow: hidden;
  background: #fff;
  .menu-wrapper {
    flex-shrink: 0;
    width: 115px;
    background: #f5f5f5;
    .menu-item {
      font-size: 0;
      line-height: 16px;
      .text-wrapper {
        text-align: center;
        font-size: 14px;
        line-height: 46px;
        font-weight: 400;
      }
      &.current {
        position: relative;
        margin-top: -1px;
        background-color: #ffffff;
        .text-wrapper {
          color: #e93b3d;
        }
      }
    }
  }
  .cls-wrapper {
    flex: 1;
    padding-left: 10px;
    .cls-list {
      list-style: none;
    }
    .cls-item {
      padding: 5px 0;
      font-size: 14px;
      color: #333;
      font-weight: 700;
      .promotion {
        img {
          width: 100%;
          border-radius: 5px;
        }
      }
      .item-title {
        display: flex;
        align-items: center;
        margin-bottom: 8px;
        position: relative;
        .item-icon {
          width: 20px;
          height: 20px;
          margin-right: 10px;
          img {
            width: 100%;
            height: 100%;
          }
        }
        .item-name {
          font-size: 14px;
          color: #333;
        }
        .item-arrow {
          position: absolute;
          right: 0;
        }
      }
      .item-content {
        text-align: center;
        font-size: 12px;
        color: #666;
        line-height: 30px;
        margin-bottom: 5px;
      }
    }
  }
}
</style>
