<template>
  <div style="height: 400px;">
    <h2>SNS KPIダッシュボード</h2>
    <Line :data="chartData" :options="chartOptions" />
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

ChartJS.register(
  Title, Tooltip, Legend,
  LineElement, PointElement,
  CategoryScale, LinearScale
)

const chartData = ref({
  labels: [],
  datasets: []
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'top' },
    title: { display: true, text: 'Instagram / TikTok / X 推移' }
  }
}

onMounted(async () => {
  try {
    const token = localStorage.getItem('access_token')
    const res = await axios.get(`${import.meta.env.VITE_API_URL}/metrics`, {
      headers: {
        Authorization: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0YWthIiwiZXhwIjoxNzQ1NDQ2NTQxfQ.qDnMA2LqharbYUITQq8UkN_kJ-zo3VGB2M7OPxdpEEU`,
        // Authorization: `Bearer ${token}`
      }
    })

    const metrics = res.data
    console.log('✅ 取得したmetrics:', metrics)

    chartData.value = {
      labels: metrics.map(item => item.date),
      datasets: [
        {
          label: 'Instagram',
          data: metrics.map(item => item.instagram),
          borderColor: 'rgb(255, 99, 132)',
          fill: false
        },
        {
          label: 'TikTok',
          data: metrics.map(item => item.tiktok),
          borderColor: 'rgb(54, 162, 235)',
          fill: false
        },
        {
          label: 'X',
          data: metrics.map(item => item.x),
          borderColor: 'rgb(75, 192, 192)',
          fill: false
        }
      ]
    }

  } catch (error) {
    console.error('❌ APIエラー:', error)
  }
})
</script>
