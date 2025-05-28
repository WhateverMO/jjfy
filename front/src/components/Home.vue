<script setup>
import HelloWorld from './HelloWorld.vue'
import TheWelcome from './TheWelcome.vue'
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
    console.log('API Response:', data)
    api1Result.value = data
  } catch (error) {
    console.error('Error fetching API:', error)
  }
}
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="../assets/logo.svg" width="125" height="125" />
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
    <div>
      <button @click="increment">点击计数</button>
      <p>计数值：{{ count }}</p>
    </div>
  </main>
</template>

<style scoped>
.logo {
  display: block;
  margin: 0 auto 2rem;
}
.wrapper {
  display: flex;
  justify-content: center;
}
</style>
