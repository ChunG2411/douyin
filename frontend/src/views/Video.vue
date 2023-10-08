<script setup>
import { Store } from '../assets/store'
import AuthenComponent from '../components/authen.vue'
import CommentComponent from '../components/comment_list.vue'
import ProfileComponent from '../components/profile_short.vue'
import { socket_noti } from '../function/socket.js'

import { ref, reactive, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { vOnClickOutside } from '@vueuse/components'

const store = Store()
const route = useRoute()


watch(() => route.params.id, (currentvalue, oldvalue) => {
    api_get_video(currentvalue)
})

const my_user = localStorage.getItem('username')
const video = ref(null)

const show_login_popup = ref(false)

const show_component = reactive({
    comment: false,
    profile: false
})


const close_popup = [() => {
    show_login_popup.value = false
}]


const api_get_video = (id) => {
    let header = null
    if (store.is_login) {
        header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
    }
    axios.get(`${store.domain}/api/video/${id}`, header)
        .then(response => {
            video.value = response.data.data
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
api_get_video(route.params.id)

const like_video = () => {
    if (store.is_login) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        axios.get(`${store.domain}/api/video/${route.params.id}/like`, header)
            .then(response => {
                if (response.data.data == "Liked.") {
                    video.value.liked = true
                    video.value.like_count += 1

                    //socket noti: like
                    socket_noti.send(JSON.stringify({
                        "user": localStorage.getItem('username'),
                        "video": video.value.id,
                        "type": "1"
                    }))
                }
                else {
                    video.value.liked = false
                    video.value.like_count -= 1
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

const save_video = () => {
    if (store.is_login) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        axios.get(`${store.domain}/api/video/${route.params.id}/save`, header)
            .then(response => {
                if (response.data.data == "Saved.") {
                    video.value.saved = true
                    video.value.save_count += 1
                }
                else {
                    video.value.saved = false
                    video.value.save_count -= 1
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


</script>

<template>
    <div class="video_view" v-if="video">
        <div>
            <div>
                <video class="video_view" :src="video.video" autoplay loop controls />
            </div>
            <div>
                <div>
                    <img class="profile_avatar_icon" :src="store.domain + video.user_infor.avatar"
                        @click="handle_show_component('profile')">

                    <button @click="like_video" v-if="video.liked">liked: {{ video.like_count }}</button>
                    <button @click="like_video" v-else>like: {{ video.like_count }}</button>

                    <button @click="handle_show_component('comment')">{{ video.comment_count }}</button>

                    <button @click="save_video" v-if="video.saved">saved: {{ video.save_count }}</button>
                    <button @click="save_video" v-else>save: {{ video.save_count }}</button>
                </div>
                <div>
                    <router-link :to="{ name: 'music', params: { id: video.music } }" v-if="video.music">
                        <img class="profile_avatar_icon" :src="store.domain + video.user_infor.avatar">
                    </router-link>
                    <img class="profile_avatar_icon" :src="store.domain + video.user_infor.avatar" v-else>
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

    <div class="popup" v-if="show_login_popup">
        <AuthenComponent v-on-click-outside="close_popup" />
    </div>
</template>