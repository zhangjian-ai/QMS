import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // 登录token、nickname
    token: localStorage.token,
    nickname: localStorage.nickname
  },
  mutations: {
    // 保存token
    storeToken(state, payload) {
      state.token = payload.token
      state.nickname = payload.nickname
      localStorage.token = payload.token
      localStorage.nickname = payload.nickname
    }
  },
  actions: {
  },
  modules: {
  }
})
