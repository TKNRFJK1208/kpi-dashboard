<template>
  <div>
    <input v-model="username" placeholder="Username" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="login">ログイン</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

// 親コンポーネントに「login-success」イベントをemitできるようにする
const emit = defineEmits(['login-success'])

const username = ref('')
const password = ref('')
const auth = useAuthStore()

const login = async () => {
  try {
    const params = new URLSearchParams()
    params.append('username', username.value)
    params.append('password', password.value)

    const res = await axios.post(`${import.meta.env.VITE_API_URL}/token`, params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })

    const token = res.data.access_token
    auth.login(token)  // Piniaストアを使ってトークンを保存
    localStorage.setItem('access_token', token)
    console.log('✅ ログイン成功！トークン保存しました')

    // ここで親に「ログイン成功」を通知！
    emit('login-success')

  } catch (error) {
    console.error('❌ ログイン失敗:', error)
  }
}
</script>
