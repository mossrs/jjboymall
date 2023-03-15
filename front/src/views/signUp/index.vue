<template>
  <div class="wrap page-sign page-footer-bar page-nav-bar">
    <nav-bar title="注册" left-arrow></nav-bar>
    <Row class="container">
      <i-col span="12" class="signup-img-box">
        <img src="static/img/signup-sale.png" alt="" />
      </i-col>
      <i-col span="8" class="box">
        <div class="sign-up-title">
          <h1>欢迎注册账号</h1>
        </div>
        <div class="sing-up-step-box">
          <Steps :current="signUpStep">
            <Step title="验证手机号" icon="iphone"></Step>
            <Step title="填写账号信息" icon="person-add"></Step>
            <Step title="注册成功" icon="ios-checkmark-outline"></Step>
          </Steps>
          <div class="sign-up-box">
            <transition mode="out-in">
              <router-view></router-view>
            </transition>
          </div>
        </div>
      </i-col>
    </Row>
    <Footer />
  </div>
</template>

<script>
  import store from "@/vuex/store";
  import { mapState, mapMutations } from "vuex";
  import Footer from "@/components/footer/Footer";
  // import footerBar from '@/components/footerBar'
  import navBar from "@/components/navBar";
  export default {
    name: "SignUp",
    data() {
      return {
        index: 0
      };
    },
    computed: {
      ...mapState(["signUpStep"])
    },
    methods: {
      ...mapMutations(["SET_SIGN_UP_SETP"])
    },
    store,
    mounted() {
      this.SET_SIGN_UP_SETP(0);
    },
    components: {
      Footer,
      navBar
    }
  };
</script>

<style scoped>
  .wrap{
    display: flex;
    flex-direction: column;
  }
  .container {
    margin: 15px auto;
    /* height: 500px; */
    overflow: hidden;
    flex: 1;
    min-height: 420px;
  }
  .signup-img-box {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .signup-img-box > img {
    width: 80%;
  }
  .sign-up-title {
    width: 430px;
    margin: 15px auto;
    height: 40px;
  }
  .sing-up-step-box {
    margin: 0 auto;
    padding-left: 30px;
    padding-top: 30px;
    width: 430px;
    /* height: 390px; */
    border: 1px solid #d6d6d6;
  }
  .sign-up-box {
    margin: 30px 25px;
    width: 350px;
    display: flex;
    align-items: center;
  }
  .box{
    margin-top: 30px;
  }
</style>
<style lang="less" scoped>
  .page-sign {
    background: #fff;
    height: 100vh;
  }
  @media (max-width: 992px) {
    .container {
      width: 100%;
      .signup-img-box {
        display: none;
      }
      .box {
        width: 100%;
        .sing-up-step-box {
          width: 100%;
          padding-left: 5px;
          /deep/.ivu-steps {
            padding-left: calc(10%);
            display: flex;
            /deep/.ivu-steps-item {
              // display: flex;
            }
            /deep/.ivu-steps-head {
              display: none;
            }
          }
          // /deep/.ivu-steps {
          //   padding-left: 30px;
          // }
          .sign-up-box {
            width: 100%;
            margin-left: 10px;
          }
          .info-form {
            /deep/.ivu-form {
              width: 100%;
            }
          }
        }
      }
    }
  }
  @media (min-width: 992px) {
    .page-sign {
      // height: calc(100vh - 35px);
      /deep/ .footer {
        // position: fixed;
        bottom: 0;
        margin: 0;
      }
    }
    .container {
      min-height: 500px;
    }
  }
</style>
