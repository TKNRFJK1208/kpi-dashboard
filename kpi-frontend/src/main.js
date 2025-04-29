import { createApp } from 'vue'
import './style.css'
import './assets/main.css'
import App from './App.vue'
import { createPinia } from 'pinia'

const app = createApp(App)

app.use(createPinia()) // ← Piniaを登録！
app.mount('#app')