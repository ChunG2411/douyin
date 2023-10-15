import { createApp } from 'vue'
import { createPinia } from 'pinia'
import infiniteScroll from 'vue-infinite-scroll'

import App from './App.vue'
import router from './router/index.js'
import './assets/style.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(infiniteScroll)
app.use(router)

app.mount('#app')
