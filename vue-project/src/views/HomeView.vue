<template>
  <div class="p-4 flex flex-col gap-6">
    <!-- 数据源选择 -->
    <div class="flex flex-col gap-2">
      <div class="text-gray-600 font-medium">数据源选择：</div>
      <el-select
        v-model="selectedSource"
        placeholder="请选择数据源"
        @change="fetchTables"
        style="width: 240px"
      >
        <el-option
          v-for="table in dataSources"
          :key="table"
          :label="table"
          :value="table"
        />
      </el-select>
    </div>

    <!-- 表选择 -->
    <div class="flex flex-col gap-2">
      <div class="text-gray-600 font-medium">数据表选择：</div>
      <el-select
        v-model="selectedTable"
        placeholder="请选择数据表"
        style="width: 240px"
        :disabled="tables.length === 0"
      >
        <el-option
          v-for="table in tables"
          :key="table"
          :label="table"
          :value="table"
        />
      </el-select>
    </div>

    <!-- 血缘图操作区域 -->
    <div class="flex flex-col gap-2">
      <div class="text-gray-600 font-medium">血缘图操作：</div>
      <el-button
        type="primary"
        :disabled="!selectedSource || !selectedTable"
        @click="fetchLineageImage"
        style="width: 240px"
      >
        获取血缘图
      </el-button>
    </div>

    <!-- 图像展示 -->
    <div v-if="lineageImageUrl" class="mt-4 border rounded p-2">
      <div class="image-preview" @click="openLightbox">
        <img :src="lineageImageUrl" alt="数据血缘图" class="preview-image" />
        <div class="preview-overlay">
          <el-icon class="preview-icon"><FullScreen /></el-icon>
          <div class="preview-text">点击查看大图</div>
        </div>
      </div>
      
      <!-- 使用vue-easy-lightbox组件 -->
      <vue-easy-lightbox
        :visible="lightboxVisible"
        :imgs="[lineageImageUrl]"
        :index="0"
        @hide="lightboxVisible = false"
        :moveDisabled="false"
        :enableZoom="true"
        :zoomScale="2"
      >
        <template v-slot:toolbar="{ toolbarMethods }">
          <div class="custom-toolbar">
            <el-button-group>
              <el-button @click="toolbarMethods.zoomIn" size="small" :icon="ZoomIn">放大</el-button>
              <el-button @click="toolbarMethods.zoomOut" size="small" :icon="ZoomOut">缩小</el-button>
              <el-button @click="toolbarMethods.reset" size="small" :icon="Refresh">重置</el-button>
              <el-button @click="lightboxVisible = false" size="small">关闭</el-button>
            </el-button-group>
          </div>
        </template>
      </vue-easy-lightbox>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Minus, Refresh, ZoomIn, ZoomOut, FullScreen } from '@element-plus/icons-vue'
import axios from 'axios'
import VueEasyLightbox from 'vue-easy-lightbox'

// 数据源固定为 dev 和 main，设置初始测试数据
const dataSources = ref(['dev', 'main', 'test'])
const tables = ref(['table1', 'table2', 'table3'])
const selectedSource = ref('')
const selectedTable = ref('')
const lineageImageUrl = ref('')

// Lightbox相关变量
const lightboxVisible = ref(false)


// 获取所有数据源（页面初始化）
const fetchDataSources = async () => {
    // 暂时使用测试数据，后续连接后端API时再修改
  dataSources.value = ['table1', 'table2', 'table3']
  selectedSource.value = ''
  ElMessage.success('获取数据表成功')
}
// 获取所选数据源的所有表
const fetchTables = async() => {
  try {
    const response = await axios.get('/api/get_table_names')
    console.log('获取数据源:', response.data)
    dataSources.value = response.data.table_names
    ElMessage.success('获取数据源成功')
  } catch (error) {
    console.log('获取数据源失败:', error)
    ElMessage.error('获取数据源失败')
  }
}

// 获取数据血缘图（本地测试用）
const fetchLineageImage = () => {
  try {
    // 使用本地图片进行测试
    const testImage = new URL('../assets/images/test-lineage.jpg', import.meta.url).href
    lineageImageUrl.value = testImage
    ElMessage.success('获取血缘图成功')
  } catch (error) {
    ElMessage.error('获取血缘图失败')
  }
}

// 页面初始化加载数据源
onMounted(() => {
  fetchDataSources()
})

// 打开图像查看器
const openLightbox = () => {
  lightboxVisible.value = true
}
</script>

<style scoped>
.image-preview {
  position: relative;
  width: 100%;
  height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  overflow: hidden;
  border: 1px solid #eaeaea;
  border-radius: 4px;
}

.preview-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.preview-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.image-preview:hover .preview-overlay {
  opacity: 1;
}

.preview-icon {
  font-size: 32px;
  color: white;
  margin-bottom: 8px;
}

.preview-text {
  color: white;
  font-size: 16px;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
}

.custom-toolbar {
  margin-top: 12px;
  display: flex;
  justify-content: center;
}
</style>