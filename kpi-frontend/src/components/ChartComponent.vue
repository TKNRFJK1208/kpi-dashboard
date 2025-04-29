<template>
  <div style="height: 500px;">
    <h2>SNS KPIダッシュボード</h2>

    <!-- SNS切り替えセレクトボックス -->
    <select v-model="selectedSNS" @change="fetchMetrics">
      <option value="tiktok">TikTok</option>
      <option value="instagram">Instagram</option>
      <option value="x">X</option>
    </select>

    <Line v-if="chartData.labels.length" :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  LineElement, PointElement,
  CategoryScale, LinearScale
} from 'chart.js'

// Chart.js登録
ChartJS.register(
  Title, Tooltip, Legend,
  LineElement, PointElement,
  CategoryScale, LinearScale
)

// 状態管理
const selectedSNS = ref('tiktok') // 初期値はTikTok
const chartData = ref({
  labels: [],
  datasets: []
})
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'top' },
    title: { display: true, text: 'SNSフォロワー推移' }
  }
}

// データ取得関数
const fetchMetrics = async () => {
  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      throw new Error('アクセストークンが存在しません。ログインしてください。')
    }

    let endpoint = ''
    if (selectedSNS.value === 'tiktok') {
      endpoint = '/tiktok_metrics'
    } else if (selectedSNS.value === 'instagram') {
      endpoint = '/ig_metrics'
    } else if (selectedSNS.value === 'x') {
      endpoint = '/x_metrics'
    }

    const res = await axios.get(`${import.meta.env.VITE_API_URL}${endpoint}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    const metrics = res.data
    console.log('✅ 取得したmetrics:', metrics)

    chartData.value = {
      labels: metrics.map(item => item.date),
      datasets: [
        {
          label: selectedSNS.value.toUpperCase(),
          data: metrics.map(item => item.followers),
          borderColor: 'rgb(75, 192, 192)',
          fill: false
        }
      ]
    }

  } catch (error) {
    console.error('❌ APIエラー:', error.message || error)
    alert('トークンエラーまたはAPIエラーが発生しました。ログインし直してください。')
  }
}

// 初回実行
onMounted(() => {
  fetchMetrics()
})
</script>
