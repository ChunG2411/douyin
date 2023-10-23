<script setup>
import { Store } from '../assets/store'
import AuthenComponent from '../components/authen.vue'
import CommentComponent from '../components/comment_list.vue'
import ProfileComponent from '../components/profile_short.vue'
import { socket_noti } from '../function/socket.js'

import { ref, reactive } from 'vue'
import axios from 'axios'
import { vOnClickOutside } from '@vueuse/components'

const store = Store()

const my_user = localStorage.getItem('username')
const list_video = ref([])
const page = ref(0)

const show_login_popup = ref(false)
const show_component = reactive({
    comment: false,
    profile: false
})


const close_popup = [() => {
    show_login_popup.value = false
}]

const get_list_video = () => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }

    axios.get(`${store.domain}/api/home/followed`, header)
        .then(response => {
            list_video.value = response.data.data
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
get_list_video()

const like_video = (id) => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.get(`${store.domain}/api/video/${id}/like`, header)
        .then(response => {
            for (let i = 0; i < list_video.value.length; i++) {
                if (list_video.value[i].id == id) {
                    if (response.data.data == "Liked.") {
                        list_video.value[i].liked = true
                        list_video.value[i].like_count += 1

                        //socket noti: like
                        socket_noti.send(JSON.stringify({
                            "user": localStorage.getItem('username'),
                            "video": list_video.value[i].id,
                            "type": "1"
                        }))
                    }
                    else {
                        list_video.value[i].liked = false
                        list_video.value[i].like_count -= 1
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

const save_video = (id) => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.get(`${store.domain}/api/video/${id}/save`, header)
        .then(response => {
            for (let i = 0; i < list_video.value.length; i++) {
                if (list_video.value[i].id == id) {
                    if (response.data.data == "Saved.") {
                        list_video.value[i].saved = true
                        list_video.value[i].save_count += 1
                    }
                    else {
                        list_video.value[i].saved = false
                        list_video.value[i].save_count -= 1
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


const handle_show_component = (target) => {
    if (target == "comment") {
        show_component.comment = true
        show_component.profile = false
    }
    else {
        show_component.comment = false
        show_component.profile = true
    }
}


const loadMore = (e) => {
    const { scrollTop, offsetHeight, scrollHeight } = e.target
    if ((scrollTop + offsetHeight) >= scrollHeight) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        page.value += 1
        axios.get(`${store.domain}/api/home/followed?page=${page.value}`, header)
            .then(response => {
                if (response.data.data.length == 0) {
                    page.value -= 1
                }
                else {
                    for (let i = 0; i < response.data.data.length; i++) {
                        list_video.value.push(response.data.data[i])
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
window.addEventListener('scroll', loadMore);

</script>

<template>
    <div class="home" v-on:scroll="loadMore">
        <div v-for="video in list_video" :key="video.id">
            <div>
                <div>
                    <video class="video_view" :src="video.video" loop controls />
                </div>
                <div>
                    <div>
                        <img class="profile_avatar_video" :src="store.domain + video.user_infor.avatar"
                            @click="handle_show_component('profile')">

                        <button @click="like_video(video.id)" v-if="video.liked">liked: {{ video.like_count }}</button>
                        <button @click="like_video(video.id)" v-else>like: {{ video.like_count }}</button>

                        <button @click="handle_show_component('comment')">{{ video.comment_count }}</button>

                        <button @click="save_video(video.id)" v-if="video.saved">saved: {{ video.save_count }}</button>
                        <button @click="save_video(video.id)" v-else>save: {{ video.save_count }}</button>
                    </div>
                    <div>
                        <router-link :to="{ name: 'music', params: { id: video.music } }" v-if="video.music">
                            <img class="profile_avatar_video" :src="store.domain + video.user_infor.avatar">
                        </router-link>
                        <img class="profile_avatar_video" :src="store.domain + video.user_infor.avatar" v-else>
                    </div>
                </div>
                <div>
                    <router-link :to="{ name: 'guest_profile', params: { username: video.user_infor.username } }"
                        v-if="my_user != video.user_infor.username">
                        <p>{{ video.user_infor.full_name }}</p>
                    </router-link>
                    <router-link to="/profile/self" v-else>
                        <p>{{ video.user_infor.full_name }}</p>
                    </router-link>

                    <p>{{ video.descrip }}</p>
                </div>
            </div>

            <div v-if="show_component.comment || show_component.profile">
                <div v-if="show_component.comment">
                    <CommentComponent :video_id="video.id" />
                    <button @click="show_component.comment = false">close</button>
                </div>
                <div v-if="show_component.profile">
                    <ProfileComponent :username="video.user_infor.username" />
                    <button @click="show_component.profile = false">close</button>
                </div>
            </div>
        </div>
    </div>

    <div class="popup" v-if="show_login_popup">
        <AuthenComponent v-on-click-outside="close_popup" />
    </div>
</template>

<style>
.home {
    overflow-y: scroll;
    height: 800px;
    width: 600px;
}
</style>