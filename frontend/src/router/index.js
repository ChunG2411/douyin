import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import Profile from '../views/Profile.vue'

const routes = [
    {
        name: "home",
        path: "/",
        component: Home
    },
    {
        name: "profile",
        path: "/profile/:username",
        component: Profile
    }

]
const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router