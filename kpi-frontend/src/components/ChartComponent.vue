<template>
  <div class="h-[500px] flex flex-col items-center">
    <h2 class="text-2xl font-bold mb-4">{{ chartTitle }}</h2>
    <div class="select-container">
      <!-- SNS選択 -->
      <select v-model="selectedSNS" @change="updateChart" class="border p-2 rounded mb-4" :disabled="isLoading">
        <option value="tiktok">TikTok</option>
        <option value="instagram">Instagram</option>
        <option value="x">X</option>
      </select>

      <!-- フィルター切り替え -->
      <select v-model="filterMode" class="border p-2 rounded mb-4" :disabled="isLoading">
        <option value="all">全期間表示</option>
        <option value="last7">直近7日間のみ</option>
      </select>
    </div>

    <!-- ローディング表示 -->
    <div v-if="isLoading" class="flex flex-col items-center justify-center h-64">
      <div class="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-500 border-l-transparent"></div>
      <p class="mt-4 text-gray-700">データ読み込み中...</p>
    </div>

    <!-- グラフ -->
    <Line v-else-if="chartData.labels.length" :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import axios from 'axios'
import { Line } from 'vue-chartjs'
import { useAuthStore } from '../stores/auth'
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  LineElement, PointElement,
  CategoryScale, LinearScale
} from 'chart.js'

ChartJS.register(
  Title, Tooltip, Legend,
  LineElement, PointElement,
  CategoryScale, LinearScale
)

// 状態管理
const selectedSNS = ref('tiktok')
const filterMode = ref('all')
const allMetrics = ref([])
const chartData = ref({ labels: [], datasets: [] })
const isLoading = ref(false)
const authStore = useAuthStore()

const chartTitle = computed(() => `${selectedSNS.value.toUpperCase()} フォロワー推移`)

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'top' },
    title: { display: true, text: chartTitle }
  }
}

function sortByDate(data) {
  return data.sort((a, b) => new Date(a.date) - new Date(b.date))
}

function filterLast7Days(data) {
  const today = new Date()
  const sevenDaysAgo = new Date()
  sevenDaysAgo.setDate(today.getDate() - 6)

  return data.filter(item => {
    const itemDate = new Date(item.date)
    return itemDate >= sevenDaysAgo && itemDate <= today
  })
}

async function fetchAllMetrics() {
  try {
    isLoading.value = true
    const token = localStorage.getItem('access_token')
    if (!token) throw new Error('アクセストークンが存在しません')

    let endpoint = ''
    if (selectedSNS.value === 'tiktok') {
      endpoint = '/tiktok_metrics'
    } else if (selectedSNS.value === 'instagram') {
      endpoint = '/ig_metrics'
    } else if (selectedSNS.value === 'x') {
      endpoint = '/x_metrics'
    }

    const res = await axios.get(`${import.meta.env.VITE_API_URL}${endpoint}`, {
      headers: { Authorization: `Bearer ${token}` }
    })

    allMetrics.value = sortByDate(res.data)
  } catch (error) {
    if (error.response && error.response.status === 401) {
      alert('認証エラー：再ログインしてください。')
      authStore.logout()
    } else {
      alert('API通信エラーが発生しました。')
    }
    console.error('❌ APIエラー:', error)
  } finally {
    isLoading.value = false
  }
}

function updateChart() {
  let filtered = [...allMetrics.value]

  if (filterMode.value === 'last7') {
    filtered = filterLast7Days(filtered)
  }

  chartData.value = {
    labels: filtered.map(item => item.date),
    datasets: [
      {
        label: selectedSNS.value.toUpperCase(),
        data: filtered.map(item => item.followers),
        borderColor: 'rgb(75, 192, 192)',
        fill: false
      },
    ]
  }
}

// 初回ロード
onMounted(async () => {
  await fetchAllMetrics()
  updateChart()
})

// SNS切り替え時は再フェッチ、それ以外はupdateのみ
watch(selectedSNS, async () => {
  await fetchAllMetrics()
  updateChart()
})

watch(filterMode, () => {
  updateChart()
})
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
}
.chart {
  width: 100%;
  height: 100%;
}
.loading-spinner {
  border: 4px solid #f3f3f3; /* Light grey */
  border-top: 4px solid #3498db; /* Blue */
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 2s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.loading-text {
  margin-top: 10px;
  color: #555;
}
.error-message {
  color: red;
  font-weight: bold;
}
.select-container {
  display: flex;
  justify-content: center;
  gap: 10px;
}
.select-container select {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 150px;
}
.select-container select:disabled {
  background-color: #f0f0f0;
  cursor: not-allowed;
}
.select-container select:focus {
  outline: none;
  border-color: #007bff;
}
.select-container select:hover {
  border-color: #007bff;
}
.select-container select:active {
  border-color: #007bff;
}
.select-container select:focus-visible {
  outline: 2px solid #007bff;
}
</style>