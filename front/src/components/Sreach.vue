<template>
  <div class="clearfix search-wrap">
    <div class="col-md-6 col-md-offset-3 search-clear">
      <div class="search-content">
        <router-link :to="'/category'">
          <Icon type="navicon-round" class="hidden-lg hidden-md"></Icon>
        </router-link>
        <i-input
          v-model="sreachData"
          @on-enter="sreach"
          size="large"
          class="search-input"
          placeholder="输入你想查找的商品"
        >
          <Button
            class="hidden-xs hidden-sm"
            slot="append"
            icon="ios-search"
            @click="sreach"
          ></Button>
        </i-input>
      </div>
      <div class="tag-list">
        <Tag
          class="hidden-xs hidden-sm"
          v-for="(item, index) in promotionTags"
          :key="index"
          closable
          @on-close="closeTags(index)"
        >
          <span @click="selectTags(index)">{{ item }}</span>
        </Tag>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Sreach",
  data() {
    return {
      sreachData: "",
      promotionTags: ["手机", "华为", "移动", "学生", "免息"]
    };
  },
  methods: {
    closeTags(index) {
      this.promotionTags.splice(index, 1);
    },
    selectTags(index) {
      this.sreachData = this.promotionTags[index];
    },
    // 全局查询
    sreach() {
      this.$router.push({
        path: "/goodsList",
        query: { sreachData: this.sreachData }
      });
    }
  }
};
</script>

<style scoped>
.container {
  padding-top: 15px;
  margin: 10px auto;
  margin-bottom: 15px;
  /* width: 460px; */
}
.sreach {
  margin: 2px 0px;
}
</style>

<style lang="less" scoped>
@media (max-width: 992px) {
  .search-wrap {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 21;
    margin-bottom: 15px;
    .search-clear {
      background: #e43130;
      padding: 0 15px;
    }
    .search-content {
      display: flex;
      align-items: center;
      height: 44px;
      /deep/ .ivu-icon-navicon-round {
        font-size: 20px;
        margin-right: 15px;
        color: #fff;
      }
      .search-input {
        display: block;
        border-radius: 15px;
        height: 30px;
        overflow: hidden;
        line-height: 30px;
        /deep/ .ivu-input {
          padding: 0 7px;
          height: 30px;
          line-height: 30px;
          &:hover {
            border-color: transparent;
          }
        }
      }
    }
  }
}

@media (min-width: 992px) {
  .search-wrap {
    margin-top: 30px;
    margin-bottom: 30px;
  }
}
</style>
