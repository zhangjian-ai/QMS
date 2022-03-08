<template>
  <a-form-model
    ref="smsForm"
    :model="smsForm"
    :rules="smsRules"
    :wrapperCol="{span: 18, offset: 3}"
  >
    <a-form-model-item prop="mobile">
      <a-input v-model="smsForm.mobile" placeholder="手机号" autocomplete="off" size="large">
        <a-icon slot="prefix" type="mobile" style="color:rgba(0,0,0,.25)" />
      </a-input>
    </a-form-model-item>
    <a-form-model-item prop="code">
      <a-row>
        <a-col :span="14">
          <a-input v-model="smsForm.code" placeholder="验证码" autocomplete="off" size="large">
            <a-icon slot="prefix" type="mail" style="color:rgba(0,0,0,.25)" />
          </a-input>
        </a-col>
        <a-col :span="9" :offset="1">
          <a-button
            @click="sendCode()"
            size="large"
            type="primary"
            :disabled="smsFlag"
            block
          >{{ smsText }}</a-button>
        </a-col>
      </a-row>
    </a-form-model-item>
    <a-form-model-item :wrapper-col="{ span: 18, offset: 3 }">
      <a-button
        type="danger"
        @click="submitForm()"
        block
        size="large"
        style="margin-top: 1em;"
      >登录</a-button>
    </a-form-model-item>
  </a-form-model>
</template>
<script>
import { smsCode } from "@/api";

export default {
  data() {
    return {
      // 验证码登录表单及校验规则
      smsForm: {
          method: 2
      },
      smsRules: {
        mobile: [
          {
            required: true,
            pattern: /^1[3-9]{1}\d{9}$/,
            trigger: "blur",
            message: "非法手机号"
          }
        ],
        code: [
          {
            required: true,
            pattern: /^\d{6}/,
            trigger: "blur",
            message: "验证码错误"
          }
        ]
      },
      smsText: "发送验证码",
      smsFlag: false
    };
  },
  methods: {
    submitForm() {
      this.$refs.smsForm.validate(valid => {
        if (valid) {
          this.$emit("login", this.smsForm);
        }
      });
    },
    // 发送验证码
    sendCode() {
      let pat = /^1[3-9]{1}\d{9}$/;
      if (pat.test(this.smsForm.mobile)) {
        smsCode(this.smsForm.mobile).then(() => {
          this.smsFlag = true;
          let n = 60;
          let timer = setInterval(
            () => {
              if (n == 0) {
                clearInterval(timer);
                this.smsText = "发送验证码";
                this.smsFlag = false;
              } else {
                n -= 1;
                this.smsText = `${n} s`;
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
  }
};
</script>