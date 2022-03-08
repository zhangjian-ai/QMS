<template>
  <div id="whole-area">
    <div id="operate-scope">
      <!-- 横幅 -->
      <div id="banner">
        <h1 id="banner-title">{{ name }}</h1>
        <h3 id="banner-desc">{{ culture }}</h3>
      </div>
      <div>
        <!-- 账号密码登录表单 -->
        <account v-if="type == 1" @login="login"></account>
        <!-- 验证码登录表单 -->
        <mobile v-if="type == 2" @login="login"></mobile>
        <!-- 注册表单 -->
        <logon v-if="type == 3" @logon="logon"></logon>
      </div>
      <div>
        <a-row>
          <a-col :span="6" :offset="2" style="text-align: left;">
            <a-button
              type="link"
              @click="type =  type == 1 ? 2 : 1"
              :disabled="type == 3"
            >{{ link1Text }}</a-button>
          </a-col>
          <a-col :span="6" :offset="8" style="text-align: right;">
            <a-button type="link" @click="type =  type != 3 ? 3 : 1">{{ link2Text }}</a-button>
          </a-col>
        </a-row>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import { sysInfo, userLogin, userLogon } from "@/api";
import account from "@/components/login/account.vue";
import mobile from "@/components/login/mobile.vue";
import logon from "@/components/login/logon.vue";

export default {
  data() {
    return {
      // 系统信息
      name: "",
      culture: "",

      // 表单类型。1:账号登陆，2:手机号登陆，3:注册
      type: 1,

      // 按钮文本
      link1Text: "验证码登录",
      link2Text: "注册账号"
    };
  },
  methods: {
    // 用户登录
    login(form) {
      userLogin(form).then(res => {
        console.log(res.data);
      });
    },

    // 用户注册
    logon(form) {
      userLogon(form).then(res => {
        if (res.status == 201) {
          this.$message.success("恭喜！注册成功");
          this.type = 1;
        }
      });
    }
  },
  components: {
    account,
    mobile,
    logon
  },
  watch: {
    type(val) {
      if (val == 1 || val == 2) {
        if (val == 1) {
          this.link1Text = "验证码登录";
        } else {
          this.link1Text = "账号密码登录";
        }
        this.link2Text = "注册账号";
      } else {
        this.link2Text = "立即登录";
      }
    }
  },
  mounted() {
    sysInfo().then(res => {
      this.name = res.data.name;
      this.culture = res.data.culture;
    });
  }
};
</script>
<style scoped>
#whole-area {
  margin: 0px;
  padding: 0px;
  width: 100%;
  height: 100%;
}
#operate-scope {
  width: 28em;
  position: relative;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #f5f5f5;
  border-radius: 0.5em;
  padding: 1em 0;
}
#banner {
  text-align: center;
}
#banner-title {
  color: cornflowerblue;
  margin-bottom: 0;
}
#banner-desc {
  color: grey;
  margin-bottom: 1.5em;
}
</style>
