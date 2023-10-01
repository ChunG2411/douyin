<script setup>
import { Store } from '../assets/store'

import { ref, reactive, watch } from 'vue'
import { useRoute } from 'vue-router'

import axios from 'axios'


const route = useRoute()
const store = Store()

watch(() => route.params.text, (currentvalue, oldvalue) => {
    search_video()
})

const active_bar = ref('video')
const search_result = reactive({
    video: [],
    user: []
})
const videoVisibilityMap = ref({})


const api_search_video = () => {
    let header = null
    if (store.is_login) {
        header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
    }
    axios.get(`${store.domain}/api/search/video?text=${route.params.text}`, header)
        .then(response => {
            if (response.data.data.length > 0) {
                search_result.video = response.data.data
            }
            else {
                search_result.video = []
            }
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

const api_search_user = () => {
    let header = null
    if (store.is_login) {
        header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
    }
    axios.get(`${store.domain}/api/search/user?text=${route.params.text}`, header)
        .then(response => {
            if (response.data.data.length > 0) {
                search_result.user = response.data.data
            }
            else {
                search_result.user = []
            }
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

const search_video = () => {
    active_bar.value = 'video'
    api_search_video()
}
search_video()

const search_user = () => {
    active_bar.value = 'user'
    api_search_user()
}

</script>

<template>
    <div class="search">
        <div class="search_bar">
            <button @click="search_video">video</button>
            <button @click="search_user">user</button>
        </div>

        <div class="search_board">
            <div class="search_board_user" v-if="active_bar == 'user'">
                <div v-if="search_result.user.length > 0">
                    <div v-for="user in search_result.user">
                        <img :src="store.domain + user.avatar">
                        <p>{{ user.full_name }}</p>
                        <router-link :to="{ name: 'guest_profile', params: { username: user.username } }">View</router-link>
                    </div>
                </div>
                <div v-else>
                    <p>No result</p>
                </div>
            </div>

            <div class="search_board_user" v-else-if="active_bar == 'video'">
                <div v-if="search_result.video.length > 0">
                    <div v-for="video in search_result.video">
                        <div>
                            <router-link :to="{ name: 'guest_profile', params: { username: video.user_infor.username } }">
                                <img :src="store.domain + video.user_infor.avatar">
                                <p>{{ video.user_infor.full_name }}</p>
                            </router-link>
                        </div>
                        <div>
                            <p>{{ video.descrip }}</p>
                            <video :src="store.domain + video.video" controls />
                        </div>
                        <div>
                            <button>{{ video.like_count }}</button>
                            <button>{{ video.comment_count }}</button>
                            <button>{{ video.save_count }}</button>
                        </div>
                    </div>
                </div>
                <div v-else>
                    <p>No result</p>
                </div>

            </div>
        </div>
    </div>
</template>