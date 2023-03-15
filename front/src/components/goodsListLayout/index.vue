<template>
  <div class="goods-list">
    <div class="goods-item" v-for="(item, index) in goodsList" :key="index">
      <router-link :to="{ path: '/goodsList', query: { sreachData: sreachData } }">
        <img class="goods-item-img" :src="item" />
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    goodsList: Array,
    sreachData: String
  }
}
</script>

<style lang="less" scoped>
.goods-list {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  .goods-item {
    width: calc(50% - 8px);
    margin-right: 8px;
    margin-bottom: 4px;
    &-img {
      width: 100%;
      &:hover {
        margin-left: -15px;
        -webkit-transition: margin-left 0.3s;
        transition: margin-left 0.3s;
      }
    }
  }
}

@media (min-width: 992px) {
  .goods-list .goods-item {
    width: calc(20% - 8px);
  }
}
</style>