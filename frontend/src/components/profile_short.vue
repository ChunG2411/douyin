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
            <router-link :to="{ name: 'guest_profile', params: { username: profile.username } }"
                v-if="my_user != profile.username" class="text normal_color no_decor fs_17">@{{ profile.full_name }}
            </router-link>
            <router-link to="/profile/self" v-else class="text normal_color no_decor fs_17">
                @{{ profile.full_name }}
            </router-link>
            <p class="normal_text normal_color fs_13">Follower: {{ profile.follower_count }}</p>
        </div>
        <VideoListComponent :active="'video'" :username="props.username" />
    </div>
</template>

<style>
.profile_short{
    height: 100%;
}
</style>