import { createRouter, createWebHistory } from 'vue-router'

import Authen from '../views/Authen.vue'

const routes = [
    {
        name: "authen",
        path: "/",
        component: Authen
    },

]
const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router