import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)


export default new Vuex.Store({
  state: {
    // 登录token、nickname
    token: localStorage.token,
    nickname: localStorage.nickname,

  },
  mutations: {
    // 保存token
    storeToken(state, payload) {
      if (payload) {
        state.token = localStorage.token = payload.token
        state.nickname = localStorage.nickname = payload.nickname
      } else {
        state.token = ""
        state.nickname = ""
        localStorage.clear()
      }
    }
  },
  actions: {
  },
  modules: {
  }
})
