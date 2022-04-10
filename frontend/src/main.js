import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import Ant from 'ant-design-vue';
import { notification, message } from 'ant-design-vue'
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


// http request 拦截
axios.interceptors.request.use(
  config => {
      // 添加token
      if (store.state.token) {
          // 判断是否存在token，如果存在的话，则每个http header都加上token。本项目使用JWT
          config.headers.Authorization = `JWT ${store.state.token}`;
      }
      return config;
  },
  err => {
      return Promise.reject(err);
  });

// http response 拦截
axios.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    let res = error.response
    if (res) {
      switch (res.status) {
        case 401:
          notification.error(
            {
              message: '系统提示',
              description:
                '登录信息已过期，请重新登录。',
              duration: 3,
            }
          );
          setTimeout(() => {
            router.replace('/login');
          }, 1500)

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
    // 驳回响应对象，不再继续向后走
    return Promise.reject(res)

  });

//  路由权限判断
router.beforeEach((to, from, next) => {
  if (to.meta.auth) {  // 判断该路由是否需要登录权限
      if (store.state.token) {  // 通过vuex state获取当前的token是否存在
          next();
      }
      else {
          next({
              name: 'Login',
              //   query: { redirect: to.fullPath }  // 将跳转的路由path作为参数，登录成功后跳转到该路由
          })
      }
  }
  else {
      next();
  }
})

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
