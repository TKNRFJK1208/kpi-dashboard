<template>
  <div id="app">
    <div v-if="isAuthenticated">
      <div style="position: absolute; top: 10px; right: 10px;">
        <button 
          @click="logout" 
          class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded"
        >ログアウト</button>
      </div>
      <div style="position: absolute; top: 10px; left: 10px;">
        <button
          class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded mb-4"
          @click="triggerScraping"
        >
          データを手動で更新
        </button>
      </div>
      <h1>Instagram / TikTok / X 推移</h1>
      <p>このダッシュボードは、Instagram、TikTok、Xのデータを表示します。</p>
      <ChartComponent />
    </div>
    <div v-else>
      <h1>Instagram / TikTok / X ダッシュボード</h1>
      <Login @login-success="handleLoginSuccess" />
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import ChartComponent from './components/ChartComponent.vue'
import Login from './components/Login.vue'
import { useAuthStore } from './stores/auth'

const isAuthenticated = ref(!!localStorage.getItem('access_token'))
const auth = useAuthStore()

const triggerScraping = async () => {
  const token = localStorage.getItem('access_token')
  try {
    await axios.post(`${import.meta.env.VITE_API_URL}/scrape-all`, {}, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    alert("✅ データ更新完了しました")
  } catch (error) {
    alert("❌ 更新エラー: " + error.message)
  }
}

function handleLoginSuccess() {
  isAuthenticated.value = true
}

function logout() {
  auth.logout()
  localStorage.removeItem('access_token')
  isAuthenticated.value = false
  location.reload()  // ←追加
}
</script>
