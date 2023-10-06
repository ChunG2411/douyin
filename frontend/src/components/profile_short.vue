<script setup>
import { Store } from '../assets/store'
import VideoListComponent from '../components/video_list.vue'

import { ref, defineProps, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
    username: String
})

const store = Store()
const my_user = localStorage.getItem('username')
const profile = ref(null)

const api_get_user_infor = (username) => {
    axios.get(`${store.domain}/api/user/${username}`)
        .then(response => {
            profile.value = response.data.data
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
api_get_user_infor(props.username)

</script>

<template>
    <div class="profile_short" v-if="profile">
        <div>
            <router-link :to="{ name: 'guest_profile', params: { username: profile.username } }" v-if="my_user!=profile.username">
                <b>{{ profile.full_name }}</b>
            </router-link>
            <router-link to="/profile/self" v-else>
                <b>{{ profile.full_name }}</b>
            </router-link>
            <small>follower: {{ profile.follower_count }}</small>
        </div>
        <div>
            <VideoListComponent :active="'video'" :username="props.username" />
        </div>
    </div>
</template>