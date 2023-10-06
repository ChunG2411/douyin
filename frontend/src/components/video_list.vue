<script setup>
import { Store } from '../assets/store'

import { ref, defineProps, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
    active: String,
    username: String
})

watch(props, (oldvalue, currentvalue) => {
    api_get_video_list(currentvalue.active)
})

const store = Store()
const video_list = ref(null)


const api_get_video_list = (value) => {
    let header = null
    if (store.is_login) {
        header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
    }
    axios.get(`${store.domain}/api/user/${props.username}/${value}`, header)
        .then(response => {
            video_list.value = response.data.data
        })
        .catch(error => {
            try {
                store.error = error.response.data.msg
            }
            catch {
                store.error = error
            }
        })
}
api_get_video_list('video')

</script>

<template>
    <div class="video_list">
        <div class="video_card" v-if="video_list" v-for="video in video_list" :key="video.id">
            <router-link :to="{ name: 'video', params: { id: video.id } }">
                <video class="video_card" :src="store.domain + video.video" />
                <p>{{ video.descrip }}</p>
                <p>{{ video.like_count }}</p>
                <p>{{ video.comment_count }}</p>
                <p>{{ video.save_count }}</p>
            </router-link>
        </div>
    </div>
</template>