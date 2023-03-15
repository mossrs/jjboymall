<template>
  <Layout class="layout">
    <nav-bar title="我的收货地址" />
    <Content class="content">
      <transition mode="out-in">
        <div>
          <div class="address-box" v-for="(item, index) in getAddress" :key="index">
            <div class="address-header">
              <span>{{item.recipient}}</span>
              <div class="address-action">
                <span @click="edit(index)"><Icon type="edit"></Icon> 修改</span>
                <span @click="del(index)"><Icon type="trash-a"></Icon> 删除</span>
              </div>
            </div>
            <div class="address-content">
              <p><span class="address-content-title"> 收 货 人 :</span> {{item.recipient}}</p>
              <p><span class="address-content-title">收货地区:</span> {{item.province}} {{item.city}} {{item.area}}
              </p>
              <p><span class="address-content-title">手机号码:</span> {{item.telephone}}</p>
              <p><span class="address-content-title">收货地址:</span> {{item.address}}</p>
              <span v-if="item.default_address" style="color: #c81623;font-size: smaller">默认收货地址</span>
            </div>
          </div>
          <Modal v-model="modal" width="530">
              <p slot="header">
                <Icon type="edit"></Icon>
                <span>修改地址</span>
              </p>
              <div>
                <Form ref="formInline" :model="formData" label-position="left" :label-width="100" :rules="ruleInline">
                  <FormItem label="收件人" prop="recipient">
                    <i-input v-model="formData.recipient" size="large"></i-input>
                  </FormItem>
                  <FormItem label="收件地区" prop="address">
                    <Distpicker :province="formData.province" :city="formData.city" :area="formData.area" @province="getProvince" @city="getCity" @area="getArea"></Distpicker>
                  </FormItem>
                  <FormItem label="收件地址" prop="address">
                    <i-input v-model="formData.address" size="large"></i-input>
                  </FormItem>
                  <FormItem label="手机号码" prop="telephone">
                    <i-input v-model="formData.telephone" size="large"></i-input>
                  </FormItem>
                  <FormItem label="默认收货地址">
                    <Radio-group v-model="formData.defaultAddress">
                      <Radio label="true">是</Radio>
                      <Radio label="false">否</Radio>
                    </Radio-group>
                  </FormItem>
                </Form>
              </div>
              <div slot="footer">
                  <Button type="primary" size="large" long @click="editAction()">修改</Button>
              </div>
          </Modal>
        </div>
      </transition>
    </Content>
    <Footer class="layout-footer-center">2018 &copy; Gavin</Footer>
  </Layout>
</template>

<script>
import store from '@/vuex/store';
import { mapActions, mapGetters } from 'vuex';
import Distpicker from 'v-distpicker';
import navBar from '@/components/navBar'
export default {
  name: 'MyAddress',
  data () {
    return {
      modal: false,
      formData: {
        loginUser: '',
        recipient: '',
        telephone: '',
        defaultAddress: '',
        province: '广东省',
        city: '广州市',
        area: '天河区',
        address: ''
      },
      ruleInline: {
        recipient: [
          { required: true, message: '请输入姓名', trigger: 'blur' }
        ],
        telephone: [
          { required: true, message: '手机号不能为空', trigger: 'blur' },
          { type: 'string', pattern: /^1[3|4|5|7|8][0-9]{9}$/, message: '手机号格式出错', trigger: 'blur' }
        ],
        defaultAddress: [
          { required: true, message: '请选择是否设置为默认地址', trigger: 'change' }
        ],
        address: [
          { required: true, message: '请输入地址', trigger: 'blur' }
        ]
      }
    };
  },
  created () {
    const info = JSON.parse(localStorage.getItem('info'));
    const username = info.data.username;
    console.log(username);
    this.loadAddress(username);
  },
  computed: {
    ...mapGetters(['getAddress'])
  },
  methods: {
    ...mapActions(['loadAddress', 'delAddress', 'editAddress']),
    getProvince (data) {
      this.formData.province = data.value;
    },
    getCity (data) {
      this.formData.city = data.value;
    },
    getArea (data) {
      this.formData.area = data.value;
    },
    edit (index) {
      this.modal = true;
      this.formData.id = this.getAddress[index].id
      this.formData.recipient = this.getAddress[index].recipient;
      this.formData.province = this.getAddress[index].province;
      this.formData.city = this.getAddress[index].city;
      this.formData.area = this.getAddress[index].area;
      this.formData.address = this.getAddress[index].address;
      this.formData.telephone = this.getAddress[index].telephone;
      this.formData.defaultAddress = this.getAddress[index].defaultAddress;
      console.log(this.formData);
    },
    editAction () {
      const info = JSON.parse(localStorage.getItem('info'));
      const username = info.data.username;
      this.formData.loginUser=username;
      this.editAddress(this.formData).then(result => {
        if (result) {
          this.$Message.success(`修改成功`);
          this.loadAddress(username);
        } else {
          this.$Message.error('修改失败');
        }
        this.modal = false;
      });
    },
    del (index) {
      this.$Modal.confirm({
        title: '信息提醒',
        content: '你确定删除这个收货地址',
        onOk: () => {
          console.log(this.getAddress[index].id);
          this.delAddress(this.getAddress[index].id).then(result => {
            if (result) {
              this.$Message.success(`删除成功`);
              const info = JSON.parse(localStorage.getItem('info'));
              const username = info.data.username;
              this.loadAddress(username);
            } else {
              this.$Message.error('删除失败');
            }
          });
        },
        onCancel: () => {
          this.$Message.info('取消删除');
        }
      });
    }
  },
  components: {
    Distpicker,
    navBar
  },
  store
};
</script>

<style scoped>
.layout{
  /* padding-top: 44px; */
}
.address-box {
  padding: 15px;
  margin: 15px;
  border-radius: 5px;
  box-shadow: 0px 0px 5px #ccc;
}
.address-header {
  height: 35px;
  display: flex;
  justify-content: space-between;
  color: #232323;
  font-size: 18px;
}
.address-content {
  font-size: 14px;
}
.address-content-title {
  color: #999;
}
.address-action span{
  margin-left: 15px;
  font-size: 14px;
  color: #2d8cf0;
  cursor: pointer;
}
.content {
  /* margin: 15px; */
  background-color: #fff;
  padding: 15px;
}
.layout-footer-center {
  padding: 0px 15px;
  padding-bottom: 15px;
  text-align: center;
}
</style>
