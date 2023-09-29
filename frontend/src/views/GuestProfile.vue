<script setup>
import VideoListComponent from '../components/video_list.vue'
import { Store } from '../assets/store.js'

import { reactive, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { vOnClickOutside } from '@vueuse/components'

const store = Store()
const route = useRoute()

watch(() => route.params.username, (currentvalue, oldvalue) => {
    api_get_user_infor(currentvalue)
    check_follow(currentvalue)
})

const profile = reactive({
    infor: null,
    followed: null,
    follower: null,
    follow_status: null,
    active_tab: "video"
})

const show_followed_popup = ref(false)
const show_follower_popup = ref(false)
const show_avatar_popup = ref(false)


const close_popup = [() => {
    show_followed_popup.value = false
    show_follower_popup.value = false
    show_avatar_popup.value = false
}]

const api_get_user_infor = (username) => {
    axios.get(`${store.domain}/api/user/${username}`)
        .then(response => {
            profile.infor = response.data.data
            profile.active_tab = "video"
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
api_get_user_infor(route.params.username)


const api_get_followed = () => {
    axios.get(`${store.domain}/api/user/${profile.infor.username}/followed-list`)
        .then(response => {
            profile.followed = response.data.data
        })
        .catch(e => {
            try {
                store.msg_error = error.response.data.msg
            }
            catch {
                store.msg_error = error
            }
        })
}
const api_get_follower = () => {
    axios.get(`${store.domain}/api/user/${profile.infor.username}/follower-list`)
        .then(response => {
            profile.follower = response.data.data
        })
        .catch(e => {
            try {
                store.msg_error = error.response.data.msg
            }
            catch {
                store.msg_error = error
            }
        })
}

const show_followed = () => {
    show_followed_popup.value = true
    api_get_followed()
}

const show_follower = () => {
    show_follower_popup.value = true
    api_get_follower()
}


const check_follow = (username) => {
    if (store.is_login) {
        axios.get(`${store.domain}/api/user/${localStorage.getItem('username')}/followed-list`)
            .then(response => {
                for (let i = 0; i < response.data.data.length; i++) {
                    if (response.data.data[i].username == username) {
                        profile.follow_status = true
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
check_follow(route.params.username)


const follow = () => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.get(`${store.domain}/api/user/${profile.infor.username}/follow`, header)
        .then(response => {
            profile.follow_status = true
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

const unfollow = () => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.get(`${store.domain}/api/user/${profile.infor.username}/follow`, header)
        .then(response => {
            profile.follow_status = false
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

</script>

<template>
    <div class="profile">
        <div class="profile-infor" v-if="profile.infor">
            <div>
                <div>
                    <img class="profile_avatar" :src="store.domain + profile.infor.avatar"
                        @click="show_avatar_popup = true">
                    <button @click="show_followed">followed: {{ profile.infor.followed_count }}</button>
                    <button @click="show_follower">follower: {{ profile.infor.follower_count }}</button>

                    <p>fullname: {{ profile.infor.full_name }}</p>
                    <p>username: {{ profile.infor.username }}</p>
                    <p v-if="profile.infor.gender">gender: {{ profile.infor.gender }}</p>
                    <p v-if="profile.infor.birth">birth: {{ profile.infor.birth }}</p>
                    <p v-if="profile.infor.address">address: {{ profile.infor.address }}</p>
                    <p v-if="profile.infor.introduce">introduce: {{ profile.infor.introduce }}</p>
                </div>

                <div v-if="store.is_login">
                    <button @click="unfollow" v-if="profile.follow_status">Unfollow</button>
                    <button @click="follow" v-else>Follow</button>
                </div>
            </div>

            <div>
                <p id="created" @click="profile.active_tab = 'video'">created ({{ profile.infor.video_count }})</p>
            </div>
        </div>

        <div class="profile-video">
            <VideoListComponent :active="profile.active_tab" :username="route.params.username" />
        </div>

        <div class="popup" v-if="store.msg_error || show_followed_popup || show_follower_popup || show_avatar_popup">
            <div id="error-popup" v-if="store.msg_error">
                <p>{{ store.msg_error }}</p>
            </div>

            <div id="followed-popup" v-if="show_followed_popup" v-on-click-outside="close_popup">
                <b>Followed</b>
                <p v-for="user in profile.followed">{{ user.username }}</p>
            </div>
            <div id="follower-popup" v-if="show_follower_popup" v-on-click-outside="close_popup">
                <b>Follower</b>
                <p v-for="user in profile.follower">{{ user.username }}</p>
            </div>

            <div id="avatar-popup" v-if="show_avatar_popup" v-on-click-outside="close_popup">
                <img class="show_profile_avatar" :src="store.domain + profile.infor.avatar" />
            </div>
        </div>
    </div>
</template>

<style>
.popup div {
    background: white;
}
</style>