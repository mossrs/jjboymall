<template>
  <div class="item-class-show">
    <Dropdown
      trigger="click"
      class="item-class-group hidden-md hidden-lg"
      v-for="(items, index) in searchConditionData"
      @on-click="dropDownSelect($event, index)"
      :key="'dropdown' + index"
    >
      <p class="item-class-name">
        {{ items.specName }}
        {{ selectedItemList[index] ? ":" + selectedItemList[index] : "" }}
      </p>
      <DropdownMenu slot="list">
        <DropdownItem
          v-for="(item, subIndex) in items.optionList"
          :key="subIndex"
          :name="subIndex"
          >{{ item.name }}
        </DropdownItem>
      </DropdownMenu>
    </Dropdown>
    <Row
      class="item-class-group hidden-xs hidden-sm"
      v-for="(items, index) in searchConditionData"
      :key="'row' + index"
    >
      <i-col class="item-class-name" span="2"
        ><p>{{ items.specName }} <span class="hidden-xs hidden-sm">:</span></p>
      </i-col>
      <i-col
        :class="[
          'item-class-select',
          { 'item-class-select-active': selectActiveIndex === index }
        ]"
        span="22"
      >
        <span
          v-for="(item, subIndex) in items.optionList"
          :key="subIndex"
          :id="item.id"
          :class="spanClass"
          @click="selectItem(item, items)"
          >{{ item.name }}</span
        >
      </i-col>
    </Row>
  </div>
</template>

<script>
import store from "@/vuex/store";
import { mapState, mapGetters, mapMutations } from "vuex";
export default {
  name: "GoodsClassNav",
  // 通过props获取父组件传递过来的值
  props: ["searchConditionData"],
  data() {
    return {
      spanClass: "span-unselect-class",
      selectedItemList: [],
      selectActiveIndex: -1
    };
  },
  computed: {
    ...mapState(["selectedCondtions"]),
    ...mapGetters(["getterSelectedCondtions"])
  },
  created() {
    this.SET_SELECTED_CONDTIONS([]);
  },
  methods: {
    ...mapMutations(["SET_SELECTED_CONDTIONS"]),
    /**
     * @param optionItem 规格项值对象
     * @param sepcItem 规格项对象
     */
    selectItem: function(optionItem, sepcItem) {
      var selectedData = this.getterSelectedCondtions;
      var sel = {};
      sel.specId = sepcItem.specId;
      sel.specName = sepcItem.specName;
      sel.optionId = optionItem.id;
      sel.optionName = optionItem.name;
      /*
          specId: 1,
          specName: '颜色',
          optionId: 1,
          optionName: '红色'
       */
      for (var i = 0; i < selectedData.length; i++) {
        if (selectedData[i].specId === sepcItem.specId) {
          selectedData.remove(selectedData[i]);
        }
      }
      selectedData.push(sel);
      this.SET_SELECTED_CONDTIONS(selectedData);
      this.$parent.sreach();
    },
    dropDownSelect(subIndex, index) {
      const data = this.searchConditionData[index];
      this.selectItem(data.optionList[subIndex], data);
      this.$set(this.selectedItemList, index, data.optionList[subIndex].name);
    }
  },
  store
};

Array.prototype.indexOf = function(val) {
  for (var i = 0; i < this.length; i++) {
    if (this[i] === val) return i;
  }
  return -1;
};

Array.prototype.remove = function(val) {
  var index = this.indexOf(val);
  if (index > -1) {
    this.splice(index, 1);
  }
};
</script>

<style scoped>
.item-class-show {
  margin: 15px auto;
  width: 100%;
}
.item-class-group {
  margin-top: 1px;
  height: 45px;
  border-bottom: 1px solid #ccc;
}
.item-class-group:first-child {
  border-top: 1px solid #ccc;
}
.item-class-name {
  padding-left: 15px;
  line-height: 44px;
  color: #666;
  font-weight: bold;
  background-color: #f3f3f3;
}
.item-class-name:first-child {
  line-height: 43px;
}
.span-unselect-class {
  margin-left: 15px;
  width: 160px;
  color: #005aa0;
  line-height: 45px;
  cursor: pointer;
}

.span-select-class {
  margin-left: 15px;
  width: 160px;
  color: #005aa0;
  line-height: 45px;
  cursor: pointer;
}
</style>

<style lang="less" scoped>
@media (max-width: 992px) {
  .item-class-show {
    margin: 0;
    padding: 10px 5px 10px 15px;
    border-bottom: 1px solid #e5e5e5;
    position: relative;
    .item-class-group {
      display: inline-block;
      padding-right: 6px;
      border: none;
      height: auto;
      .item-class-name {
        width: auto;
        padding: 0 5px;
        height: 25px;
        line-height: 25px;
        color: #666;
        background-color: #f2f2f7;
        border-radius: 2px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
      .item-class-select {
        width: auto;
        display: none;
      }
    }
  }
}
</style>
