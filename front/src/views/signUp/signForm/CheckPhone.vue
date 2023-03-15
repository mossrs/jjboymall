<template>
  <div class="info-form">
    <Form ref="formValidate" :model="formValidate" :label-width="80" :rules="ruleValidate">
      <FormItem label="手机号" prop="phone">
          <i-input v-model="formValidate.phone" clearable size="large"  placeholder="请输入手机号"></i-input>
      </FormItem>
      <FormItem label="验证码" prop="checkNum">
          <i-input v-model="formValidate.checkNum" size="large"  placeholder="请输入验证码">
            <Button slot="append" @click="getcheckNum">获取验证码</Button>
          </i-input>
      </FormItem>
      <Button type="error" size="large" long @click="handleSubmit('formValidate')">验证手机号</Button>
    </Form>
  </div>
</template>

<script>
import store from '@/vuex/store';
import { mapMutations, mapActions } from 'vuex';
export default {
  name: 'CheckPhone',
  data () {
    return {
      formValidate: {
        phone: '',
        checkNum: ''
      },
      flag: false,
      ruleValidate: {
        phone: [
          { required: true, message: '手机号不能为空', trigger: 'blur' },
          { type: 'string', pattern: /^1[3|4|5|7|8][0-9]{9}$/, message: '手机号格式出错', trigger: 'blur' }
        ],
        checkNum: [
          { required: true, message: '必须填写验证码', trigger: 'blur' },
          { type: 'string', min: 4, max: 4, message: '验证码长度错误', trigger: 'blur' }
        ]
      }
    };
  },
  methods: {
    ...mapMutations(['SET_SIGN_UP_SETP']),
    // 导入 校验 验证码 发送验证码 判断手机号是否已存在
    ...mapActions(['checkSmsCode','sendSmsCode','isExist']),
    getcheckNum () {
      const father = this;
      if (this.formValidate.phone.length === 11) {
        this.isExist(this.formValidate.phone).then(data => {
          //  手机号未注册 调用发送验证码的接口
             this.sendSmsCode(this.formValidate.phone).then(data => {
                father.$Message.success('验证码发送成功');
                father.flag = true;
             })
        });
      } else {
        this.$Message.error({
          content: '请输入正确的手机号',
          duration: 6,
          closable: true
        });
      }
    },
    handleSubmit (name) { // 提交验证
      this.$refs[name].validate((valid) => {
        if (!this.flag) {
          this.$Message.error({
            content: '请先验证手机号',
            duration: 6,
            closable: true
          });
          return;
        }
        if (valid) {
          const data = {
            phone: this.formValidate.phone,
            code: this.formValidate.checkNum,
          }
          // 调用 校验注册码的接口
          this.checkSmsCode(data).then(data => {
            if(data){
                console.log('短信验证码结果为:', data.msg)
                // 路由到 注册下面的 输入注册信息页面 携带手机号为参数
                this.$router.push({ path: '/SignUp/inputInfo', query: { phone: this.formValidate.phone } });
                this.SET_SIGN_UP_SETP(1);
            }else{
                this.$Message.error("验证码出错或已失效");
            }
            
          })
        } else {
          this.$Message.error({
            content: '请填写正确的信息',
            duration: 6,
            closable: true
          });
        }
      });
    }
  },
  store
};
</script>

<style scoped>
.info-form {
  width: 90% !important;
}
</style>
