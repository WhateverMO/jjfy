<template>
  <el-container class="full-height">
    <el-aside width="220px" class="aside-fixed">
      <el-menu :default-openeds="['1']" router>
        <el-sub-menu index="1">
          <template #title>数据管理</template>
          <el-menu-item index="/data/table">数据表管理</el-menu-item>
          <el-menu-item index="/data/import">数据导入</el-menu-item>
          <el-menu-item index="/data/export">数据导出</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="2">
          <template #title>统计分析</template>
          <el-menu-item index="/data/stat">数据统计</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header-fixed">数据管理平台</el-header>
      <el-main class="main-full">
        <router-view v-slot="{ Component }">
          <component :is="Component" />
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import 'element-plus/dist/index.css'
import { ElContainer, ElAside, ElHeader, ElMain, ElMenu, ElSubMenu, ElMenuItem } from 'element-plus'
</script>

<style scoped>
.full-height {
  height: 100vh;
}
.aside-fixed {
  min-height: 100vh;
  border-right: 1px solid #ebeef5;
  padding: 0;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  z-index: 100;
  background: #f5f7fa;
}
.el-container {
  margin-left: 220px;
  height: 100vh;
}
.header-fixed {
  font-size: 20px;
  font-weight: bold;
  padding-left: 20px;
  background: #fff;
  border-bottom: 1px solid #ebeef5;
}
.main-full {
  height: calc(100vh - 60px);
  min-height: 200px;
  overflow: auto;
  background: #fff;
}
</style>
