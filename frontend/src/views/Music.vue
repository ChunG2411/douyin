<script setup>
import { Store } from '../assets/store'
import VideoListComponent from '../components/video_list.vue'

import { useRoute } from 'vue-router'
import { ref } from 'vue'
import axios from 'axios'


const store = Store()
const route = useRoute()

const my_user = localStorage.getItem('username')
const music = ref(null)
const videos = ref(null)

const api_get_music = () => {
    let header = null
    if (store.is_login) {
        header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
    }
    axios.get(`${store.domain}/api/music/${route.params.id}`, header)
        .then(response => {
            music.value = response.data.data
        })
        .catch(error => {
            try {
                store.msg_error = error.response.data.msg
            }
            catch {
                store.msg_error = error
            }
        })
}
api_get_music()

const api_get_video_of_music = () => {
    let header = null
    if (store.is_login) {
        header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
    }
    axios.get(`${store.domain}/api/music/${route.params.id}/video`, header)
        .then(response => {
            videos.value = response.data.data
        })
        .catch(error => {
            try {
                store.msg_error = error.response.data.msg
            }
            catch {
                store.msg_error = error
            }
        })
}
api_get_video_of_music()

</script>

<template>
    <div class="music">
        <div v-if="music">
            <div>
                <img class="profile_avatar_music" :src="store.domain + music.user_infor.avatar" />
            </div>
            <div>
                <b>music created by {{ music.user_infor.full_name }}</b>
                <router-link :to="{ name: 'guest_profile', params: { username: music.user_infor.username } }"
                    v-if="my_user != music.user_infor.username">
                    <p>{{ music.user_infor.full_name }}</p>
                </router-link>
                <router-link to="/profile/self" v-else>
                    <p>{{ music.user_infor.full_name }}</p>
                </router-link>
                <p>{{ music.video_count }} used</p>
            </div>
        </div>

        <div v-if="videos">
            <div v-for="video in videos">
                <router-link :to="{ name: 'video', params: { id: video.id } }">
                    <video class="video_card" :src="store.domain + video.video" />
                    <p>like: {{ video.like_count }}</p>
                </router-link>
            </div>
        </div>
    </div>
</template>