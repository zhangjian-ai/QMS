<template>
  <a-form-model
    ref="loginForm"
    :model="loginForm"
    :rules="loginRules"
    :wrapperCol="{span: 18, offset: 3}"
  >
    <a-form-model-item prop="username">
      <a-input v-model="loginForm.username" placeholder="用户名" autocomplete="off" size="large">
        <a-icon slot="prefix" type="user" style="color:rgba(0,0,0,.25)" />
      </a-input>
    </a-form-model-item>
    <a-form-model-item prop="password">
      <a-input
        v-model="loginForm.password"
        placeholder="密码"
        type="password"
        autocomplete="off"
        size="large"
      >
        <a-icon slot="prefix" type="lock" style="color:rgba(0,0,0,.25)" />
      </a-input>
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
export default {
  data() {
    return {
      // 账号登录表单及校验规则
      loginForm: {
          method: 1
      },
      loginRules: {
        username: [
          { required: true, trigger: "submit", message: "请输入用户名" }
        ],
        password: [{ required: true, trigger: "submit", message: "请输入密码" }]
      }
    };
  },
  methods: {
    submitForm() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.$emit("login", this.loginForm);
        }
      });
    }
  }
};
</script>
