<template>
  <div id="app">
    <h1>Instagram / TikTok / X 推移</h1>
    <p>このダッシュボードは、Instagram、TikTok、Xのデータを表示します。</p>

    <div v-if="isAuthenticated">
      <button @click="logout" style="margin-bottom: 20px;">ログアウト</button>
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

// ログイン状態を管理する
const isAuthenticated = ref(!!localStorage.getItem('access_token'))

// ログイン成功時に呼び出す
function handleLoginSuccess() {
  isAuthenticated.value = true
}

// ログアウト処理
function logout() {
  localStorage.removeItem('access_token')
  isAuthenticated.value = false
}
</script>
