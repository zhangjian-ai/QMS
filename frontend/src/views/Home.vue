<template>
  <a-layout id="home-layout">
    <!-- 侧边栏 -->
    <a-layout-sider v-model="collapsed" :trigger="null" collapsible :collapsedWidth="0">
      <div class="logo"></div>
      <a-menu theme="dark" mode="inline" @click="changeView">
        <a-sub-menu key="service">
          <span slot="title">
            <a-icon type="cloud-server" />
            <span>服务管理</span>
          </span>
          <a-menu-item key="serviceList">服务列表</a-menu-item>
          <a-menu-item key="moduleList">模块列表</a-menu-item>
          <a-menu-item key="apiList">接口列表</a-menu-item>
        </a-sub-menu>
      </a-menu>
    </a-layout-sider>
    <!-- 主要区域 -->
    <a-layout>
      <!-- 导航栏 -->
      <a-layout-header id="layout-header">
        <a-row id="header-row">
          <a-col :span="4">
            <a-icon
              class="trigger"
              :type="collapsed ? 'menu-unfold' : 'menu-fold'"
              @click="() => (collapsed = !collapsed)"
            />
          </a-col>
          <a-col
            :xs="{ span: 13, offset: 7}"
            :md="{ span: 9, offset: 11}"
            :lg="{ span: 7, offset: 13}"
            :xl="{ span: 5, offset:15}"
            :xxl="{ span: 3, offset: 17}"
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
export default {
  data() {
    return {
      collapsed: false
    };
  },
  methods: {
    changeView(item) {
      this.$router.push({ name: item.key });
    }
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