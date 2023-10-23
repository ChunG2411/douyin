import { createApp } from 'vue'
import { createPinia } from 'pinia'
import infiniteScroll from 'vue-infinite-scroll'

import App from './App.vue'
import router from './router/index.js'
import './assets/style.css'

import '@fortawesome/fontawesome-free/css/all.css'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'

library.add(fas)

const app = createApp(App)
const pinia = createPinia()

app.component('font-awesome-icon', FontAwesomeIcon)
app.use(pinia)
app.use(infiniteScroll)
app.use(router)

app.mount('#app')
