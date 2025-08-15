<template>
  <el-menu default-active="1-4-1" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose"
    :collapse="isCollapse">
    <el-menu-item index="2">
        <i class="el-icon-menu"></i>
        <span slot="title">导航一</span>
    </el-menu-item>
    <el-submenu index="1">
        <template slot="title">
            <Location />
            <span slot="title">导航二</span>
        </template>
        <el-menu-item-group>
            <span slot="title">分组一</span>
            <el-menu-item index="1-1">选项1</el-menu-item>
            <el-menu-item index="1-2">选项2</el-menu-item>
        </el-menu-item-group>
    </el-submenu>
</el-menu>
</template>

<script setup lang="ts">
import { Location } from '@element-plus/icons-vue';
</script>

<style>

</style>
