<template>
  <div class="nav-bar hidden-lg hidden-md">
    <div class="nav-bar-left" @click="$router.back()">
      <Icon type="chevron-left"></Icon>
    </div>
    <div class="nav-bar-title">{{title}}</div>
    <div class="nav-bar-menu">
      <slot name="menu" />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: String
  }
}
</script>

<style lang="less" scoped>
.nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 20;
  display: flex;
  align-items: center;
  height: 44px;
  text-align: center;
  background: #fff;
  border-bottom: 1px solid #e5e5e5;
  .nav-bar-title {
    flex-grow: 1;
    font-size: 16px;
    color: #333;
    font-weight: 500;
  }
  .nav-bar-left,
  .nav-bar-menu {
    font-size: 18px;
    width: 44px;
  }
}
</style>