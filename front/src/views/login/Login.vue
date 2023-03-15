<template>
  <!-- 登陆页面 -->
  <div class="page-login">
    <nav-bar title="登录" left-arrow></nav-bar>
    <div class="login-wrap">
      <Row>
        <i-col span="13" offset="2" class="login-img-box">
          <img src="static/img/sale.jpg" alt="" />
        </i-col>
        <i-col span="7" class="login-box">
          <div class="login-container">
            <div class="login-header">
              <p>欢迎登录 · 马士兵咚宝商城</p>
            </div>
            <div class="form-box">
              <div id="captcha" v-show="state.showSlider"></div>
              <Form ref="formInline" :model="formDate" :rules="ruleInline">
                <FormItem prop="username">
                  <i-input
                    type="text"
                    v-model="formDate.username"
                    clearable
                    size="large"
                    placeholder="用户名"
                  >
                    <Icon type="person" slot="prepend"></Icon>
                  </i-input>
                </FormItem>
                <FormItem prop="password">
                  <i-input
                    type="password"
                    v-model="formDate.password"
                    clearable
                    size="large"
                    placeholder="密码"
                  >
                    <Icon type="ios-locked-outline" slot="prepend"> </Icon>
                  </i-input>
                </FormItem>
                <!-- <FormItem prop="rand">
                  <Row>
                    <Col span="16">
                      <i-input
                        v-model="formDate.rand"
                        clearable
                        size="large"
                        placeholder="验证码"
                      >
                        <Icon type="ios-locked-outline" slot="prepend"> </Icon>
                      </i-input>
                    </Col>
                    <Col span="3">
                      <img
                        id="codevalidate_login"
                        :src="this.picBase64"
                        width="80"
                        height="32"
                        style="margin-left: 10px"
                        @click="changeUrl()"
                      />
                    </Col>
                  </Row>
                </FormItem> -->
                <FormItem>
                  <Button
                    type="error"
                    size="large"
                    @click="handleSubmit('formInline')"
                    long
                  >登录</Button
                  >
                  <Button
                    type="error"
                    size="large"
                    @click="skipToRegister"
                    class="register"
                    long
                  >去注册</Button
                  >
                </FormItem>
              </Form>
            </div>
          </div>
        </i-col>
      </Row>
    </div>
    <Footer />
  </div>
</template>

<script>
  import Footer from "@/components/footer/Footer";
  import store from "@/vuex/store";
  import { mapMutations, mapActions, mapState } from "vuex";
  // import footerBar from '@/components/footerBar'
  import navBar from "@/components/navBar";
  import '@/utils/longbow.slidercaptcha.js'
  export default {
    name: "Login",
    data() {
      return {
        formDate: {
          username: "",
          password: "",
          tracks: null,
          remoteUrl: ''
          // rand: ""
        },
        state: {
          showSlider: false,
          verifyResult: false,
          verifyArr: null
        },
        ruleInline: {
          username: [
            { required: true, message: "请输入用户名", trigger: "blur" },
            {
              type: "string",
              min: 6,
              max: 14,
              message: "用户名出错",
              trigger: "blur"
            }
          ],
          password: [
            { required: true, message: "请输入密码", trigger: "blur" },
            {
              type: "string",
              min: 6,
              max: 14,
              message: "密码不能少于6位",
              trigger: "blur"
            }
          ],
          rand: [
            { required: true, message: "验证码不能为空", trigger: "blur" },
            { min: 1, max: 6, message: "验证码长度不正确", trigger: "blur" },
            {
              type: "string",
              pattern: /^[0-9]*$/,
              message: "验证码格式错误",
              trigger: "blur"
            }
          ]
        }
      };
    },
    created() {
      // this.getPicBase64();
    },
    mounted() {
      // 初始化验证滑块控件
      let width = $('.form-box').outerWidth()
      let height = $('.form-box').outerHeight()
      let self = this
      $('#captcha').sliderCaptcha({
        width: parseInt(width*1.1),
        height: parseInt(height),
        sliderL: 42,
        sliderR: 14,
        offset: 10,
        loadingText: '正在加载中...',
        failedText: '再试一次',
        barText: '向右滑动填充拼图',
        repeatIcon: 'fa fa-redo',
        verify(arr, url) {
          self.formDate.tracks = arr
          self.formDate.remoteUrl = url
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
    computed: {
      ...mapState(["picBase64"])
    },
    methods: {
      ...mapMutations(["SET_USER_LOGIN_INFO"]),
      ...mapActions(["login", "getPicBase64"]),
      handleSubmit(name) {
        const father = this;
        console.log(this.formDate.username);
        this.$refs[name].validate(valid => {
          if (valid) {
            // debugger
            if (!this.state.verifyResult) {
              this.state.showSlider = true
              return
            }
          } else {
            this.$Message.error("请填写正确的用户名或密码");
          }
        });
      },
      tracksLogin() {
        const data = {
          username: this.formDate.username,
          password: this.formDate.password,
          tracks: this.formDate.tracks
        };
        let self = this
        this.login(data).then(data => {
          if (data) {
            self.$Message.success("登陆成功")
            self.$router.push("/")
          }
        }).catch(() => {

        })
        self.state.showSlider = false
      },
      changeUrl() {
        this.getPicBase64();
      },
      skipToRegister() {
        // 跳转注册页面
        this.$router.push("/SignUp");
      }
    },
    components: {
      Footer,
      navBar
    },
    store
  };
</script>

<style>
  @import "../../../src/styles/slidercaptcha.css";
  .sliderContainer_active {
    /* overflow: hidden; */
    height: 40px;
  }
  .sliderContainer_fail {
    height: 40px;
  }
  .login-wrap{
    width: 100%;
    flex: 1;
  }
  .login-img-box {
    height: 485px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .login-img-box > img {
    width: 68%;
  }
  .login-box {
    height: 385px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .login-container {
    width: 100%;
    height: 320px;
    border: #ed3f14 solid 1px;
  }
  .login-header {
    height: 50px;
    font-size: 14px;
    text-align: center;
    line-height: 50px;
    letter-spacing: 5px;
    color: #fff;
    background-color: #ed3f14;
  }
  .form-box {
    width: 80%;
    margin: 30px auto;
    position: relative;
    /* overflow: hidden; */
  }
  .form-box #captcha{
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
<style lang="less" scoped>
  /deep/.sliderContainer{
    margin-top: 3px;
  }
  .page-login {
    background: #fff;
    height: 100vh;
    display: flex;
    flex-direction: column;
    padding-top: 50px;
  }
  @media (max-width: 992px) {
    .login-img-box {
      display: none;
    }
    .login-container{
      margin: 50px;
      margin-top: 150px;
    }
    .login-box {
      width: 100%;
    }
    /deep/.ivu-form-item-content {
      display: flex;
      flex-direction: row;
      .register {
        margin-left: 10px;
      }
    }
  }
  @media (min-width: 992px) {
    /deep/.ivu-form-item-content {
      .register {
        display: none;
      }
    }
    .page-login {
      height: calc(100vh - 35px);
      /deep/ .footer {
        // position: fixed;
        bottom: 0;
        margin: 0;
      }
    }
  }
  body {
    overflow-x: hidden;
  }

  .block {
    position: absolute;
    left: 0;
    top: 0;
  }

  .sliderContainer {
    position: relative;
    text-align: center;
    line-height: 40px;
    background: #f7f9fa;
    color: #45494c;
    border-radius: 2px;
  }

  .sliderbg {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    background-color: #f7f9fa;
    height: 40px;
    border-radius: 2px;
    border: 1px solid #e6e8eb;
  }

  .sliderContainer_active .slider {
    top: -1px;
    border: 1px solid #1991FA;
  }

  .sliderContainer_active .sliderMask {
    border-width: 1px 0 1px 1px;
  }

  .sliderContainer_success .slider {
    top: -1px;
    border: 1px solid #52CCBA;
    background-color: #52CCBA !important;
  }

  .sliderContainer_success .sliderMask {
    border: 1px solid #52CCBA;
    border-width: 1px 0 1px 1px;
    background-color: #D2F4EF;
  }

  .sliderContainer_success .sliderIcon:before {
    content: "\f00c";
  }

  .sliderContainer_fail .slider {
    top: -1px;
    border: 1px solid #f57a7a;
    background-color: #f57a7a !important;
  }

  .sliderContainer_fail .sliderMask {
    border: 1px solid #f57a7a;
    background-color: #fce1e1;
    border-width: 1px 0 1px 1px;
  }

  .sliderContainer_fail .sliderIcon:before {
    content: "\f00d";
  }
  .sliderContainer_active .sliderText, .sliderContainer_success .sliderText, .sliderContainer_fail .sliderText {
    display: none;
  }

  .sliderMask {
    position: absolute;
    left: 0;
    top: 0;
    height: 40px;
    border: 0 solid #1991FA;
    background: #D1E9FE;
    border-radius: 2px;
  }

  .slider {
    position: absolute;
    top: 0;
    left: 0;
    width: 40px;
    height: 40px;
    background: #fff;
    box-shadow: 0 0 3px rgba(0, 0, 0, 0.3);
    cursor: pointer;
    transition: background .2s linear;
    border-radius: 2px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .slider:hover {
    background: #1991FA;
  }

  .slider:hover .sliderIcon {
    background-position: 0 -13px;
  }

  .sliderText {
    position: relative;
  }

  .sliderIcon {

  }

  .refreshIcon {
    position: absolute;
    right: 0;
    top: 0;
    cursor: pointer;
    margin: 6px;
    color: rgba(0,0,0,.25);
    font-size: 1rem;
    z-index: 5;
    transition: color .3s linear;
  }

  .refreshIcon:hover {
    color: #6c757d;
  }

</style>
