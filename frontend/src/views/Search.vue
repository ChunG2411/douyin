<script setup>
import { Store } from '../assets/store'
import AuthenComponent from '../components/authen.vue'
import CommentComponent from '../components/comment_list.vue'

import { ref, reactive, watch } from 'vue'
import { useRoute } from 'vue-router'
import { vOnClickOutside } from '@vueuse/components'
import axios from 'axios'


const route = useRoute()
const store = Store()

watch(() => route.params.text, (currentvalue, oldvalue) => {
    search_video()
})

const active_bar = ref('video')
const my_user = localStorage.getItem('username')
const search_result = reactive({
    video: [],
    user: []
})
const show_login_popup = ref(false)
const show_comment = ref(false)
const page_search_video = ref(0)
const page_search_user = ref(0)


const close_popup = [() => {
    show_login_popup.value = false
}]


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

const like_video = (id) => {
    if (store.is_login) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        axios.get(`${store.domain}/api/video/${id}/like`, header)
            .then(response => {
                if (response.data.data == "Liked.") {
                    for (let i = 0; i < search_result.video.length; i++) {
                        if (search_result.video[i].id == id) {
                            search_result.video[i].liked = true
                            search_result.video[i].like_count += 1
                        }
                    }
                }
                else {
                    for (let i = 0; i < search_result.video.length; i++) {
                        if (search_result.video[i].id == id) {
                            search_result.video[i].liked = false
                            search_result.video[i].like_count -= 1
                        }
                    }
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
    else {
        show_login_popup.value = true
    }
}

const save_video = (id) => {
    if (store.is_login) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        axios.get(`${store.domain}/api/video/${id}/save`, header)
            .then(response => {
                if (response.data.data == "Saved.") {
                    for (let i = 0; i < search_result.video.length; i++) {
                        if (search_result.video[i].id == id) {
                            search_result.video[i].saved = true
                            search_result.video[i].save_count += 1
                        }
                    }
                }
                else {
                    for (let i = 0; i < search_result.video.length; i++) {
                        if (search_result.video[i].id == id) {
                            search_result.video[i].saved = false
                            search_result.video[i].save_count -= 1
                        }
                    }
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
    else {
        show_login_popup.value = true
    }
}

const loadMoreSearch_user = (e) => {
    const { scrollTop, offsetHeight, scrollHeight } = e.target
    if ((scrollTop + offsetHeight) >= scrollHeight) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        page_search_user.value += 1
        axios.get(`${store.domain}/api/search/user?text=${route.params.text}&page=${page_search_user.value}`, header)
            .then(response => {
                if (response.data.data.length == 0) {
                    page_search_user.value -= 1
                }
                else {
                    for (let i = 0; i < response.data.data.length; i++) {
                        search_result.value.push(response.data.data[i])
                    }
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
}

const loadMoreSearch_video = (e) => {
    const { scrollTop, offsetHeight, scrollHeight } = e.target
    if ((scrollTop + offsetHeight) >= scrollHeight) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        page_search_video.value += 1
        axios.get(`${store.domain}/api/search/video?text=${route.params.text}&page=${page_search_video.value}`, header)
            .then(response => {
                if (response.data.data.length == 0) {
                    page_search_video.value -= 1
                }
                else {
                    for (let i = 0; i < response.data.data.length; i++) {
                        search_result.value.push(response.data.data[i])
                    }
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
}

window.addEventListener('scroll', loadMoreSearch_user);
window.addEventListener('scroll', loadMoreSearch_video);

</script>

<template>
    <div class="search">
        <div class="search_bar">
            <button @click="search_video">video</button>
            <button @click="search_user">user</button>
        </div>

        <div class="search_board">
            <div class="search_board_user" v-if="active_bar == 'user'">
                <div class="list_user_search" v-if="search_result.user.length > 0" v-on:scroll="loadMoreSearch_user">
                    <div v-for="user in search_result.user">
                        <img class="profile_avatar_search" :src="store.domain + user.avatar">
                        <p>{{ user.full_name }}</p>
                        <router-link :to="{ name: 'guest_profile', params: { username: user.username } }">View</router-link>
                    </div>
                </div>
                <div v-else>
                    <p>No result</p>
                </div>
            </div>

            <div class="search_board_video" v-else-if="active_bar == 'video'">
                <div class="list_video_search" v-if="search_result.video.length > 0" v-on:scroll="loadMoreSearch_video">
                    <div v-for="video in search_result.video" :key="video.id">
                        <div>
                            <router-link :to="{ name: 'guest_profile', params: { username: video.user_infor.username } }" v-if="my_user!=video.user_infor.username">
                                <img class="profile_avatar_icon" :src="store.domain + video.user_infor.avatar">
                                <p>{{ video.user_infor.full_name }}</p>
                            </router-link>
                            <router-link to="/profile/self" v-else>
                                <img class="profile_avatar_icon" :src="store.domain + video.user_infor.avatar">
                                <p>{{ video.user_infor.full_name }}</p>
                            </router-link>
                        </div>
                        <div>
                            <p>{{ video.descrip }}</p>
                            <video class="video_search" :src="video.video" controls />
                        </div>
                        <div>
                            <button @click="like_video(video.id)" v-if="video.liked">liked: {{ video.like_count }}</button>
                            <button @click="like_video(video.id)" v-else>like: {{ video.like_count }}</button>

                            <button @click="show_comment = !show_comment">{{ video.comment_count }}</button>

                            <button @click="save_video(video.id)" v-if="video.saved">saved: {{ video.save_count }}</button>
                            <button @click="save_video(video.id)" v-else>save: {{ video.save_count }}</button>
                        </div>
                        <div class="comment_board" v-if="show_comment">
                            <CommentComponent :video_id="video.id" />
                            <button @click="show_comment = false">close</button>
                        </div>
                    </div>
                </div>
                <div v-else>
                    <p>No result</p>
                </div>

            </div>
        </div>
    </div>

    <div class="popup" v-if="show_login_popup">
        <AuthenComponent v-on-click-outside="close_popup" />
    </div>
</template>

<style>
.list_user_search{
    overflow-y: scroll;
    min-height: max-content;
    max-height: 500px;
}
.list_video_search{
    overflow-y: scroll;
    min-height: max-content;
    max-height: 500px;
}
</style>