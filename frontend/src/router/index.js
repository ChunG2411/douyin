import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import GuestProfile from '../views/GuestProfile.vue'
import MyProfile from '../views/MyProfile.vue'
import Search from '../views/Search.vue'
import Video from '../views/Video.vue'
import Music from '../views/Music.vue'
import Creator from '../views/Creator.vue'
import Chat from '../views/Chat.vue'


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
        path: "/profile/self",
        component: MyProfile
    },
    {
        name: "search",
        path: "/search/:text",
        component: Search
    },
    {
        name: "video",
        path: "/video/:id",
        component: Video
    },
    {
        name: "music",
        path: "/music/:id",
        component: Music
    },
    {
        name: "creator",
        path: "/creator",
        component: Creator
    },
    {
        name: "chat",
        path: "/chat",
        component: Chat
    }
]
const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router