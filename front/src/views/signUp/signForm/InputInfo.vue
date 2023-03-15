<template>
  <div class="info-form">
    <div id="captcha" v-show="state.showSlider"></div>
    <Form
      ref="formValidate"
      :model="formValidate"
      :rules="ruleValidate"
      :label-width="80"
    >
      <FormItem label="用户名" prop="name">
        <i-input
          v-model="formValidate.name"
          clearable
          size="large"
          placeholder="请输入你的姓名"
        ></i-input>
      </FormItem>
      <FormItem label="邮箱" prop="mail">
        <i-input
          v-model="formValidate.mail"
          clearable
          size="large"
          placeholder="请输入你的邮箱"
        ></i-input>
      </FormItem>
      <FormItem label="密码" prop="password">
        <i-input
          type="password"
          v-model="formValidate.password"
          clearable
          size="large"
          placeholder="请输入你的密码"
        ></i-input>
      </FormItem>
      <FormItem label="确认密码" prop="repassword">
        <i-input
          type="password"
          v-model="formValidate.repassword"
          clearable
          size="large"
          placeholder="请再次输入你的密码"
        ></i-input>
      </FormItem>
      <!-- <FormItem label="验证码" prop="rand">
        <i-input
          v-model="formValidate.rand"
          style="width: 40%"
          clearable
          size="large"
          placeholder="验证码"
        ></i-input>
        <img
          id="codevalidate"
          :src="this.picBase64"
          width="100"
          height="30"
          style="margin-left: 10px"
          @click="changeUrl()"
        />
      </FormItem> -->
      <Button
        type="error"
        size="large"
        long
        @click="handleSubmit('formValidate')"
        >注册</Button
      >
    </Form>
  </div>
</template>

<script>
import store from "@/vuex/store";
import { mapMutations, mapActions, mapState } from "vuex";
// import '@/utils/longbow.slidercaptcha.js'
import '@/utils/longbow.slidercaptcha.js'
export default {
  name: "InputInfo",
  data() {
    const validatePassCheck = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.formValidate.password) {
        callback(new Error("两次输入的密码不一样"));
      } else {
        callback();
      }
    };
    return {
      state: {
        showSlider: false
      },
      formValidate: {
        name: "",
        mail: "",
        password: "",
        repassword: "",
        tracks: null
      },
      ruleValidate: {
        name: [
          { required: true, message: "用户名不能为空", trigger: "blur" },
          {
            min: 6,
            max: 12,
            message: "用户名最小长度6,最大长度12",
            trigger: "blur"
          }
        ],
        mail: [
          { required: true, message: "邮箱不能为空", trigger: "blur" },
          { type: "email", message: "邮箱格式错误", trigger: "blur" }
        ],
        password: [
          { required: true, message: "密码不能为空", trigger: "blur" },
          {
            type: "string",
            min: 6,
            message: "密码长度不能小于6",
            trigger: "blur"
          }
        ],
        repassword: [{ validator: validatePassCheck, trigger: "blur" }]
      }
    };
  },
  created() {
    // this.getPicBase64();
  },
  computed: {
    ...mapState(["picBase64"])
  },
  mounted() {
    // 初始化验证滑块控件
    let width = $('.info-form').outerWidth()
    let height = $('.info-form').outerHeight()
    let self = this
    $('#captcha').sliderCaptcha({
      width: parseInt(width*1.1),
      height: parseInt(height*1.1),
      sliderL: 42,
      sliderR: 14,
      offset: 10,
      loadingText: '正在加载中...',
      failedText: '再试一次',
      barText: '向右滑动填充拼图',
      repeatIcon: 'fa fa-redo',
      verify(arr, url) {
        self.formValidate.tracks = arr
      },
      remoteUrl: 'www.baidu.com',
      onSuccess: () => {  //成功事件
        var handler = setTimeout(function () {
            window.clearTimeout(handler)
            $('#captcha').sliderCaptcha('reset')
        }, 500);
        self.tracksLogin()
      }
    })
  },
  methods: {
    ...mapMutations(["SET_SIGN_UP_SETP"]),
    ...mapActions(["signUp", "getPicBase64"]),
    handleSubmit(name) {
      const father = this;
      this.$refs[name].validate(valid => {
        if (valid) {
          this.state.showSlider = true
        //   const data = {
        //     username: this.formValidate.name,
        //     phone: this.$route.query.phone,
        //     password: this.formValidate.password,
        //     email: this.formValidate.mail,
        //     status: 0
        //   };
        //   this.signUp(data).then(data => {
        //     if (data) {
        //       father.$Message.success("注册成功");
        //       father.SET_SIGN_UP_SETP(2);
        //       father.$router.push({ path: "/SignUp/signUpDone" });
        //     } else {
        //       this.$Message.error("注册失败, 请重新注册");
        //     }
        //   });
        } else {
          this.$Message.error("注册失败, 请先填写完正确信息");
        }
      });
    },
    tracksLogin() {
      const father = this;
      const data = {
        username: this.formValidate.name,
        phone: this.$route.query.phone,
        password: this.formValidate.password,
        email: this.formValidate.mail,
        status: 0,
        tracks: this.formValidate.tracks
      }
      this.signUp(data).then(data => {
        if (data) {
          father.$Message.success("注册成功");
          father.SET_SIGN_UP_SETP(2);
          father.$router.push({ path: "/SignUp/signUpDone" });
        } else {
          this.$Message.error("注册失败, 请重新注册");
        }
      })
      this.state.showSlider = false
    },
    changeUrl() {
      this.getPicBase64();
    }
  },
  store
};
</script>

<style scoped>
.info-form {
  width: 90% !important;
  /* height: 20px !important; */
}
.info-form #captcha{
  width: 100%;
  position: absolute !important;
  border: 12px solid rgb(244, 244, 248);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -45%);
  z-index: 10000;
  background: rgb(234, 234, 234);
  box-shadow: 0px 2px 19px 0px rgba(79, 79, 79, 0.5);
  border-radius: 5px;
}
</style>
<style>
@import "../../../../src/styles/slidercaptcha.css";
.sliderContainer_active {
  /* overflow: hidden; */
  height: 40px;
}
.sliderContainer_fail {
  height: 40px;
}
</style>
