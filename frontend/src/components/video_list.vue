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
    page_video.value = 0
    type.value = currentvalue.active
})

const store = Store()
const video_list = ref(null)
const type = ref('video')
const page_video = ref(0)


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
api_get_video_list(type.value)

const loadMoreVideo = (e) => {
    const { scrollTop, offsetHeight, scrollHeight } = e.target
    if ((scrollTop + offsetHeight) >= scrollHeight) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        page_video.value += 1
        axios.get(`${store.domain}/api/user/${props.username}/${type.value}?page=${page_video.value}`, header)
            .then(response => {
                if (response.data.data.length == 0) {
                    page_video.value -= 1
                }
                else {
                    for (let i = 0; i < response.data.data.length; i++) {
                        video_list.value.push(response.data.data[i])
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
window.addEventListener('scroll', loadMoreVideo);

</script>

<template>
    <div class="video_list" v-on:scroll="loadMoreVideo">
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

<style>
.video_list {
    overflow-y: scroll;
    min-height: max-content;
    max-height: 300px;
    width: 500px;
}
</style>