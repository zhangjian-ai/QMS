<template>
  <a-form-model
    ref="logonForm"
    :model="logonForm"
    :rules="logonRules"
    :wrapperCol="{span: 18, offset: 3}"
  >
    <a-form-model-item prop="username">
      <a-input v-model="logonForm.username" placeholder="登录账号">
        <a-icon slot="prefix" type="user" style="color:rgba(0,0,0,.25)" />
      </a-input>
    </a-form-model-item>
    <a-form-model-item prop="nickname">
      <a-input v-model="logonForm.nickname" placeholder="用户昵称">
        <a-icon slot="prefix" type="meh" style="color:rgba(0,0,0,.25)" />
      </a-input>
    </a-form-model-item>
    <a-form-model-item prop="password">
      <a-input v-model="logonForm.password" placeholder="设置密码" type="password" autocomplete="off">
        <a-icon slot="prefix" type="lock" style="color:rgba(0,0,0,.25)" />
      </a-input>
    </a-form-model-item>
    <a-form-model-item prop="confirm_password">
      <a-input
        v-model="logonForm.confirm_password"
        type="password"
        placeholder="确认密码"
        autocomplete="off"
      >
        <a-icon slot="prefix" type="check-square" style="color:rgba(0,0,0,.25)" />
      </a-input>
    </a-form-model-item>
    <a-form-model-item prop="role">
      <a-select placeholder="选择职位" v-model="logonForm.role">
        <a-select-option v-for="item in roles" :value="item[0]" :key="item[0]">{{ item[1] }}</a-select-option>
      </a-select>
    </a-form-model-item>
    <a-form-model-item prop="rank">
      <a-select placeholder="选择职级" v-model="logonForm.rank">
        <a-select-option v-for="item in ranks" :value="item[0]" :key="item[0]">{{ item[1] }}</a-select-option>
      </a-select>
    </a-form-model-item>
    <a-form-model-item prop="mobile">
      <a-input v-model="logonForm.mobile" placeholder="手机号" autocomplete="off">
        <a-icon slot="prefix" type="mobile" style="color:rgba(0,0,0,.25)" />
      </a-input>
    </a-form-model-item>
    <a-form-model-item prop="sms_code">
      <a-row>
        <a-col :span="14">
          <a-input v-model="logonForm.sms_code" placeholder="验证码" autocomplete="off">
            <a-icon slot="prefix" type="mail" style="color:rgba(0,0,0,.25)" />
          </a-input>
        </a-col>
        <a-col :span="9" :offset="1">
          <a-button @click="sendCode()" type="primary" :disabled="logonFlag" block>{{ logonText }}</a-button>
        </a-col>
      </a-row>
    </a-form-model-item>
    <a-form-model-item :wrapper-col="{ span: 18, offset: 3 }">
      <a-button type="danger" @click="submitForm()" block style="margin-top: 1em;">注册</a-button>
    </a-form-model-item>
  </a-form-model>
</template>
<script>
import { smsCode, getStaff } from "@/api";

export default {
  data() {
    let checkPassword = (rule, val, callback) => {
      if (!val) {
        callback(new Error("请设置用户密码"));
      }
      if (val.length < 8 || val.length > 24) {
        callback(new Error("密码需满足8～24个字符长度"));
      }
      callback()
    };
    let checkConfirmPassword = (rule, val, callback) => {
      if (!val) {
        callback(new Error("请输入确认密码"));
      }
      if (val !== this.logonForm.password) {
        callback(new Error("两次密码输入不一致"));
      }
      callback()
    };
    return {
      // 验证码登录表单及校验规则
      logonForm: {},
      logonRules: {
        username: [
          {
            required: true,
            trigger: "blur",
            message: "登录账号必填"
          }
        ],
        nickname: [
          {
            required: true,
            trigger: "blur",
            message: "用户昵称必填"
          }
        ],
        password: [
          {
            validator: checkPassword,
            trigger: "blur"
          }
        ],
        confirm_password: [
          {
            validator: checkConfirmPassword,
            trigger: "blur"
          }
        ],
        role: [
          {
            required: true,
            trigger: "blur",
            message: "必填项"
          }
        ],
        rank: [
          {
            required: true,
            trigger: "blur",
            message: "必填项"
          }
        ],
        mobile: [
          {
            required: true,
            pattern: /^1[3-9]{1}\d{9}$/,
            trigger: "blur",
            message: "非法手机号"
          }
        ],
        sms_code: [
          {
            required: true,
            pattern: /^\d{6}/,
            trigger: "blur",
            message: "验证码错误"
          }
        ]
      },
      logonText: "发送验证码",
      logonFlag: false,

      // 职位和职级信息
      roles: [],
      ranks: []
    };
  },
  methods: {
    submitForm() {
      this.$refs.logonForm.validate(valid => {
        if (valid) {
          this.$emit("logon", this.logonForm);
        }
      });
    },

    // 发送验证码
    sendCode() {
      let pat = /^1[3-9]{1}\d{9}$/;
      if (pat.test(this.logonForm.mobile)) {
        smsCode(this.logonForm.mobile).then(() => {
          this.logonFlag = true;
          let n = 60;
          let timer = setInterval(
            () => {
              if (n == 0) {
                clearInterval(timer);
                this.logonText = "发送验证码";
                this.logonFlag = false;
              } else {
                n -= 1;
                this.logonText = `${n} s`;
              }
            },
            1000,
            60
          );
        });
      } else {
        this.$message.error("手机号非法");
      }
    }
  },
  mounted() {
    getStaff().then(res => {
      this.roles = res.data.role;
      this.ranks = res.data.rank;
    });
  }
};
</script>
