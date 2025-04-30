<template>
  <div class="flex flex-col items-center">
    <input v-model="username" placeholder="Username" class="input" />
    <input v-model="password" type="password" placeholder="Password" class="input" />

    <button @click="login" :disabled="isLoading" class="button">
      {{ isLoading ? "ログイン中..." : "ログイン" }}
    </button>

    <p v-if="errorMessage" class="text-red-600 mt-2">{{ errorMessage }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const emit = defineEmits(['login-success'])

const username = ref('')
const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')
const auth = useAuthStore()

const login = async () => {
  errorMessage.value = ''
  if (!username.value || !password.value) {
    errorMessage.value = 'ユーザー名とパスワードを入力してください'
    return
  }

  try {
    isLoading.value = true

    const params = new URLSearchParams()
    params.append('username', username.value)
    params.append('password', password.value)

    const res = await axios.post(`${import.meta.env.VITE_API_URL}/token`, params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })

    const token = res.data.access_token
    auth.login(token)
    localStorage.setItem('access_token', token)
    console.log('✅ ログイン成功！')

    emit('login-success')
  } catch (error) {
    if (error.response?.status === 401) {
      errorMessage.value = 'ユーザー名またはパスワードが間違っています'
    } else {
      errorMessage.value = 'ログイン中にエラーが発生しました'
    }
    console.error('❌ ログイン失敗:', error)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
  max-width: 300px;
  margin-bottom: 10px;
  transition: border-color 0.3s;
}
.button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}
</style>
