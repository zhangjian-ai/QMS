<template>
  <a-layout id="home-layout">
    <!-- 侧边栏 -->
    <a-layout-sider v-model="collapsed" :trigger="null" collapsible :collapsedWidth="0">
      <div class="logo"></div>
      <a-menu theme="dark" mode="inline" @click="changeView">
        <a-sub-menu v-for="sub_menu in menu" :key="sub_menu.key">
          <span slot="title">
            <a-icon :type="sub_menu.icon" />
            <span>{{ sub_menu.content }}</span>
          </span>
          <a-menu-item  v-for="item in sub_menu.items" :key="item.key">{{ item.content }}</a-menu-item>
        </a-sub-menu>
      </a-menu>
    </a-layout-sider>
    <!-- 主要区域 -->
    <a-layout>
      <!-- 导航栏 -->
      <a-layout-header id="layout-header">
        <a-row id="header-row">
          <a-col :span="1">
            <a-icon
              class="trigger"
              :type="collapsed ? 'menu-unfold' : 'menu-fold'"
              @click="() => (collapsed = !collapsed)"
            />
          </a-col>
          <a-col
            :xs="{ span: 13, offset: 10}"
            :md="{ span: 9, offset: 14}"
            :lg="{ span: 7, offset: 16}"
            :xl="{ span: 5, offset:18}"
            :xxl="{ span: 3, offset: 20}"
          >
            <span>
              您好:
              <span style="color: #CC6600">{{ $store.state.nickname }}</span>
            </span>
            <a-divider type="vertical" />
            <span>工作台</span>
            <a-divider type="vertical" />
            <span>退出</span>
          </a-col>
        </a-row>
      </a-layout-header>
      <!-- 主体 -->
      <a-layout-content>
        <router-view />
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>
<script>
import { getMenu } from "@/api";

export default {
  data() {
    return {
      // 是否隐藏侧边栏
      collapsed: false,

      // 菜单配置
      menu: []
    };
  },
  methods: {
    changeView(item) {
      this.$router.push({ name: item.key });
    }
  },
  mounted() {
    getMenu().then(res => {
      this.menu = res.data;
    });
  }
};
</script>
<style>
#home-layout {
  height: 100%;
}
#layout-header {
  background-color: lightblue;
  line-height: 5%;
  height: 5%;
  padding: 0;
  display: flex;
  align-items: center;
  text-align: center;
}
#layout-header .trigger {
  font-size: 1.5em;
  margin: 0 1em;
  cursor: pointer;
  transition: color 0.3s;
}

#home-layout .trigger:hover {
  color: #1890ff;
}

#home-layout .logo {
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  margin: 16px;
}
#header-row {
  width: 100%;
  display: flex;
  align-items: center;
}
.ant-divider {
  background-color: black;
}
.ant-layout-content {
  background: #fff;
}
</style>