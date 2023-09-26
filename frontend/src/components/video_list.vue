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

const video_list = ref(null)
const msg_error = ref(null)

const api_get_video_list = (value) => {

    if (user_localstore.is_authen) {
        const header = {
            headers: { Authorization: `Bearer ${user_localstore.user["token"]}` }
        }
        axios.get(`${config.domain}/user/${props.username}/${value}`, header)
            .then(response => {
                video_list.value = response.data.data
            })
            .catch(e => {
                msg_error.value = e
            })
    }
    else {
        axios.get(`${config.domain}/user/${props.username}/${value}`)
            .then(response => {
                video_list.value = response.data.data
            })
            .catch(e => {
                msg_error.value = e
            })
    }

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