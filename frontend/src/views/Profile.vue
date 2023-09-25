<script setup>
import HeaderComponent from '../components/header.vue'
import TaskbarComponent from '../components/taskbar.vue'
import VideoListComponent from '../components/video_list.vue'
import config from '../assets/config.js'

import { reactive, ref, inject, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
const route = useRoute()

watch(() => route.params.username, (currentvalue, oldvalue) => {
    check_my_profile(currentvalue)
    api_get_user_infor(currentvalue)
})

const profile = reactive({
    infor: null,
    is_my_profile: false
})

const user_localstore = inject("user_localstore")

const params_user = ref(route.params.username)

let queryTimeout = null
const msg_error = ref(null)
const action = ref("video")
const follow_status = ref('')


const check_my_profile = (username) => {
    if (user_localstore.is_authen) {
        if (username === user_localstore.user["username"]) {
            profile.is_my_profile = true
        }
        else {
            profile.is_my_profile = false
        }
    }
}
check_my_profile(params_user.value)

const api_get_user_infor = (username) => {
    axios.get(`${config.domain}/user/${username}`)
        .then(response => {
            profile.infor = response.data.data
            params_user.value = username
            action.value = "video"
        })
        .catch(e => {
            console.log(e)
            msg_error.value = e
        })
}
api_get_user_infor(params_user.value);


const modify_infor = () => {

}

const follow = () => {

}

</script>

<template>
    <div class="profile">
        <div class="profile-infor" v-if="profile.infor">
            <div>
                <div>
                    <p>fullname: {{ profile.infor.full_name }}</p>
                    <p>followed: {{ profile.infor.followed_count }}</p>
                    <p>follower: {{ profile.infor.follower_count }}</p>
                    <p>username: {{ profile.infor.username }}</p>
                    <p v-if="profile.infor.gender">gender: {{ profile.infor.gender }}</p>
                    <p v-if="profile.infor.birth">birth: {{ profile.infor.birth }}</p>
                    <p v-if="profile.infor.introduce">introduce: {{ profile.infor.introduce }}</p>
                </div>
                <div v-if="profile.is_my_profile">
                    <button @click="modify_infor">Modify</button>
                </div>
                <div v-else>
                    <button @click="follow">{{ follow_status }}</button>
                </div>
            </div>
            <div>
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

