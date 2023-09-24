<script setup>
import HeaderComponent from '../components/header.vue'
import TaskbarComponent from '../components/taskbar.vue'
import VideoListComponent from '../components/video_list.vue'
import config from '../assets/config.js'

import { provide, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'


const profile = reactive({
    infor: ref(null),
    is_my_profile: ref(false)
})

const user_store = reactive({
    user: JSON.parse(localStorage.getItem('user')),
    is_authen: (localStorage.getItem('user') === null) ? false : true
})

provide("user_store", user_store)

const route = useRoute()
const params_user = route.params.username
let queryTimeout = null
const msg_error = ref(null)
const action = ref("video")


if (params_user === user_store.user["username"]) {
    profile.is_my_profile = true
}

const api_get_user_infor = () => {
    clearTimeout(queryTimeout)
    queryTimeout = setTimeout(async () => {
        try {
            const header = {
                headers: { Authorization: `Bearer ${user_store.user["token"]}` }
            }
            const result = await axios.get(`${config.domain}/user/${params_user}`, header)
            profile.infor = result.data.data
            return
        } catch (error) {
            console.log(error)
            msg_error.value = error.response.data.msg
        }
    }, 100)
}
api_get_user_infor()

</script>

<template>
    <HeaderComponent />
    <TaskbarComponent />

    <div class="profile">
        <div class="profile-infor" v-if="profile.infor">
            <div class="profile-infor-infor">
                <p>fullname: {{ profile.infor.full_name }}</p>
                <p>followed: {{ profile.infor.followed_count }}</p>
                <p>follower: {{ profile.infor.follower_count }}</p>
                <p>username: {{ profile.infor.username }}</p>
                <p v-if="profile.infor.gender">gender: {{ profile.infor.gender }}</p>
                <p v-if="profile.infor.birth">birth: {{ profile.infor.birth }}</p>
                <p v-if="profile.infor.introduce">introduce: {{ profile.infor.introduce }}</p>

            </div>
            <div class="profile-infor-tab">
                <p id="created" @click="action = 'video'">created ({{ profile.infor.video_count }})</p>
                <p id="like" @click="action = 'like'" v-if="profile.is_my_profile">like</p>
                <p id="save" @click="action = 'save'" v-if="profile.is_my_profile">save</p>
            </div>
        </div>

        <div class="profile-video">
            <VideoListComponent :action="action" :username="params_user" />
        </div>

        <div class="profile-popup" v-if="msg_error">
            <p>{{ msg_error }}</p>
        </div>
    </div>
</template>

