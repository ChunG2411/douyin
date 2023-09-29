import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import GuestProfile from '../views/GuestProfile.vue'
import MyProfile from '../views/MyProfile.vue'
import Search from '../views/Search.vue';

const routes = [
    {
        name: "home",
        path: "/",
        component: Home
    },
    {
        name: "guest_profile",
        path: "/profile/:username",
        component: GuestProfile
    },
    {
        name: "my_profile",
        path:"/profile/self",
        component: MyProfile
    },
    {
        name: "search",
        path:"/search/:text",
        component: Search
    }
]
const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router