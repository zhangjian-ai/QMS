import Vue from 'vue'
import VueRouter from 'vue-router'

// 解决当前子路由跳转报错,本质上就是捕获这个异常不上报
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/Login.vue'),
    meta: {
      title: "用户"
    }
  },
  {
    path: "/",
    name: "Home",
    component: () => import('../views/Home.vue'),
    children: [
      {
        path: "service/serviceList",
        name: "serviceList",
        component: () => import('../components/home/service/serviceList.vue'),
        meta: {
          title: "服务",
          auth: true
        }
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
