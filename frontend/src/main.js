import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import Ant from 'ant-design-vue';
import { Modal, message } from 'ant-design-vue'
import 'ant-design-vue/dist/antd.css';

import axios from 'axios'

Vue.use(Ant)


// axios环境的切换
if (process.env.NODE_ENV == 'development') {
  axios.defaults.baseURL = 'http://127.0.0.1:8000/api';
}
if (process.env.NODE_ENV == 'production') {
  axios.defaults.baseURL = 'http://101.43.61.175:8090/api';
}

// 默认携带cookie发起请求和保存cookie
axios.defaults.withCredentials = true

// 开发环境运行时，设置为false，控制台会打印详细的错误信息。
// 生产环境时，这些信息基本没啥用，因此发布时，需要将该值设置为 true
Vue.config.productionTip = false


// http response 拦截器
axios.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    let res = error.response
    if (res) {
      switch (res.status) {
        case 401:
          Modal.confirm(
            {
              content: '账户认证信息已失效，请重新登录。',
              title: '系统提示',
              onOk() {
                // 返回 401 清除token信息并跳转到登录页面
                store.commit('setStatus');
                router.replace('/');
              },
              onCancel() {
                store.commit('setStatus');
                router.go(0);  // 刷新一下当前页面
              }
            }
          )
          break;
        case 400:
          message.error(res.data.msg || '客户端错误')
          break;

        case 403:
          message.error(res.data.msg || '权限不足')
          break;

        case 404:
          message.error(res.data.msg || '资源不存在')
          break;

        case 500:
          message.error(res.data.msg || '服务器异常')
          break;

        case 501:
          message.error(res.data.msg || '服务器拒绝')
          break;

        default:
          message.error(res.data.msg || '服务器正在摸鱼')

      }
    }
    // 返回接口返回的错误信息
    // return Promise.reject(res)

  });

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
