<template>
<Layout class="layout">
  <nav-bar title="添加收货地址" />
  <Content class="content">
    <transition mode="out-in">
      <div>
        <div class="add-container">
          <div class="add-title hidden-xs hidden-sm">
            <h1>添加收货地址</h1>
          </div>
          <div class="add-box">
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
                <Radio-group v-model="formData.defaultAddress" >
                    <Radio label="true">是</Radio>
                    <Radio label="false">否</Radio>
                </Radio-group>
              </FormItem>
            </Form>
          </div>
          <div class="add-submit">
            <Button type="primary" @click="handleSubmit('formInline')">添加地址</Button>
          </div>
        </div>
      </div>
    </transition>
  </Content>
  <Footer class="layout-footer-center">2018 &copy; Gavin</Footer>
</Layout>

</template>

<script>
import Distpicker from 'v-distpicker';
import store from '@/vuex/store';
import navBar from '@/components/navBar'
import { mapActions } from 'vuex';
export default {
  name: 'AddAddress',
  data () {
    return {
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
  methods: {
    ...mapActions(['addAddress']),
    getProvince (data) {
      this.formData.province = data.value;
    },
    getCity (data) {
      this.formData.city = data.value;
    },
    getArea (data) {
      this.formData.area = data.value;
    },
    handleSubmit (name) {
      console.log('this.formData-=-=-=-');
      //this.$router.back();
      this.$refs[name].validate((valid) => {
        if (valid) {
          const info = JSON.parse(localStorage.getItem('info'));
          this.formData.loginUser = info.data.username
          this.addAddress(this.formData).then(data => {
            if (data) {
              this.$Message.success('添加成功');
              this.$router.push('/home/myAddress');
            } else {
              this.$Message.error('添加失败，请重新尝试');
            }
          });
        } else {
          this.$Message.error('请填写正确的地址信息');
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

<style lang="less" scoped>
.layout{
  // padding-top: 44px;
}
.add-container {
  margin: 15px auto;
  width: 60%;
  min-width: 600px;
}
.add-title {
  margin-bottom: 15px;
  text-align: center;
}
.add-submit {
  display: flex;
  justify-content: center;
}
.content {
  // margin: 15px;
  background-color: #fff;
  padding: 15px;
}
.layout-footer-center {
  padding: 0px 15px;
  padding-bottom: 15px;
  text-align: center;
}

@media (max-width: 992px) {
  /deep/.add-container{
    width: auto !important;
    min-width: auto !important;
  }
  /deep/.ivu-input-wrapper{
    width: auto !important;
  }
}
</style>
