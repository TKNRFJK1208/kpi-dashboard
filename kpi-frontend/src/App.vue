<template>
  <div id="app">
    <h1>Instagram / TikTok / X 推移</h1>
    <p>このダッシュボードは、Instagram、TikTok、Xのデータを表示します。</p>

    <div v-if="isAuthenticated">
      <button 
        @click="logout" 
        class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded mb-4"
      >ログアウト</button>
      <ChartComponent />
    </div>
    <div v-else>
      <Login @login-success="handleLoginSuccess" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ChartComponent from './components/ChartComponent.vue'
import Login from './components/Login.vue'

const isAuthenticated = ref(!!localStorage.getItem('access_token'))

function handleLoginSuccess() {
  isAuthenticated.value = true
}

function logout() {
  localStorage.removeItem('access_token')
  isAuthenticated.value = false
  location.reload()  // ←追加
}
</script>
