<script setup>
import config from '../assets/config.js'

import { ref, reactive, inject, defineProps, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
    action: String,
    username: String
})

watch(props, (oldvalue, currentvalue) => {
    api_get_video_list(currentvalue.action)
})

const user_localstore = inject("user_localstore")

let queryTimeout = null
const video_list = ref(null)
const msg_error = ref(null)

const api_get_video_list = (value) => {
    clearTimeout(queryTimeout)
    queryTimeout = setTimeout(async () => {
        try {
            const header = {
                headers: { Authorization: `Bearer ${user_localstore.user["token"]}` }
            }
            const result = await axios.get(`${config.domain}/user/${props.username}/${value}`, header)
            video_list.value = result.data.data
            return
        } catch (error) {
            console.log(error)
            msg_error.value = error.response
        }
    }, 100)
}

api_get_video_list('video')

</script>

<template>
    <div class="video_list">
        <div class="video_card" v-if="video_list" v-for="video in video_list">
            <p>{{ video.descrip }}</p>
            <p>{{ video.like_count }}</p>
            <p>{{ video.comment_count }}</p>
            <p>{{ video.save_count }}</p>
        </div>
    </div>
</template>