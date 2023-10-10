<script setup>
import { Store } from '../assets/store'

import { ref, reactive, watch } from 'vue'
import axios from 'axios'

const store = Store()

const noti_list = ref([])

const api_get_notification = () => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.get(`${store.domain}/api/notification`, header)
        .then(response => {
            noti_list.value = response.data.data
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
api_get_notification()


const delete_noti = (id) => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.delete(`${store.domain}/api/notification/${id}`, header)
        .then(response => {
            for (let i = 0; i < noti_list.value.length; i++) {
                if (noti_list.value[i].id == id) {
                    noti_list.value.splice(i, 1)
                }
            }
            store.msg_success = "Delete successful."
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
    <div class="notification">
        <div v-for="noti in noti_list" :key="noti.id" v-if="noti_list.length > 0">
            <div>
                <p v-if="noti.user_interact.split(',').length - 1 > 0">
                    {{ noti.context }} and {{ noti.user_interact.split(',').length - 1 }} other people
                </p>
                <p v-else>{{ noti.context }}</p>

                <p v-if="noti.type == 'like_video'">liked your video</p>
                <p v-else-if="noti.type == 'comment_video'">commented your video</p>
                <p v-else-if="noti.type == 'like_comment'">liked your comment</p>
                <p v-else-if="noti.type == 'comment_comment'">commented your comment</p>
                <p v-else-if="noti.type == 'follow'">followed you</p>
            </div>
            <div>
                <router-link :to="{ name: 'video', params: { id: noti.video } }" v-if="noti.video">
                    <video class="video_manager" :src="store.domain + noti.video_link" />
                </router-link>
                <router-link :to="{ name: 'guest_profile', params: { username: noti.user_send_infor.username } }" v-else>
                    <img :src="store.domain + noti.user_send_infor.avatar" />
                </router-link>

            </div>
            <div>
                <button @click="delete_noti(noti.id)">Delete</button>
            </div>
        </div>

        <div v-else>
            <p>No notification</p>
        </div>
    </div>
</template>

<style>
.notification{
    height: 500px;
    overflow: scroll;
}
</style>