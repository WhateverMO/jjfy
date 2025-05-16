<script setup>
import HelloWorld from './components/HelloWorld.vue'
import TheWelcome from './components/TheWelcome.vue'
import { ref } from 'vue'

const count = ref(0)

const increment = () => {
  count.value++
}

const api1Result = ref(null)

const fetchApi1 = async () => {
  try {
    const response = await fetch('/api/api1');
    const data = await response.json()
    console.log('API Response:', data) // 打印 API 返回的数据
    api1Result.value = data
  } catch (error) {
    console.error('Error fetching API:', error)
  }
}
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="You did it!" />
    </div>
  </header>

  <main>
    <!-- <TheWelcome /> -->
    <div>
      <button @click="fetchApi1">api1</button>
      <div v-if="api1Result">{{ api1Result }}</div>
    </div>

    <!-- 新增的按钮和计数显示 -->
    <div>
      <button @click="increment">点击计数</button>
      <p>计数值：{{ count }}</p>
    </div>
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
