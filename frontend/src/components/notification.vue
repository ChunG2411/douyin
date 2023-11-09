<script setup>
import { Store } from '../assets/store'

import { ref } from 'vue'
import axios from 'axios'

const store = Store()

const noti_list = ref([])
const page_noti = ref(0)

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
            store.msg_success = store.translate("msg","delete")
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

const loadMoreNoti = (e) => {
    const { scrollTop, offsetHeight, scrollHeight } = e.target
    if ((scrollTop + offsetHeight + 5) >= scrollHeight) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        page_noti.value += 1
        axios.get(`${store.domain}/api/notification?page=${page_noti.value}`, header)
            .then(response => {
                if (response.data.data.length == 0) {
                    page_noti.value -= 1
                }
                else {
                    for (let i = 0; i < response.data.data.length; i++) {
                        noti_list.value.push(response.data.data[i])
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
window.addEventListener('scroll', loadMoreNoti);

</script>

<template>
    <div class="notification">
        <p class="text normal_color fs_17">{{ store.translate("noti", "noti") }}</p>
        <div class="noti_list_item mg_t_5" v-if="noti_list.length > 0" v-on:scroll="loadMoreNoti">
            <div class="noti_item" v-for="noti in noti_list" :key="noti.id">
                <div class="noti_item_left">
                    <div>
                        <router-link :to="{ name: 'video', params: { id: noti.video } }" v-if="noti.video">
                            <video class="noti_image" :src="store.domain + noti.video_link" />
                        </router-link>
                        <router-link :to="{ name: 'guest_profile', params: { username: noti.user_send_infor.username } }"
                            v-else>
                            <img class="noti_image" :src="store.domain + noti.user_send_infor.avatar" />
                        </router-link>
                    </div>
                    <div class="noti_content">
                        <p class="text normal_color fs_15" v-if="noti.user_interact.split(',').length - 1 > 0">
                            {{ noti.context }} {{ store.translate("noti", "and") }} {{ noti.user_interact.split(',').length - 1 }} {{ store.translate("noti", "other") }}
                        </p>
                        <p class="text normal_color fs_15" v-else>{{ noti.context }}</p>

                        <p class="normal_text normal_color fs_15" v-if="noti.type == 'like_video'">{{ store.translate("noti", "like_video") }}</p>
                        <p class="normal_text normal_color fs_15" v-else-if="noti.type == 'comment_video'">{{ store.translate("noti", "cmt_video") }}</p>
                        <p class="normal_text normal_color fs_15" v-else-if="noti.type == 'like_comment'">{{ store.translate("noti", "like_cmt") }}</p>
                        <p class="normal_text normal_color fs_15" v-else-if="noti.type == 'comment_comment'">{{ store.translate("noti", "cmt_cmt") }}</p>
                        <p class="normal_text normal_color fs_15" v-else-if="noti.type == 'follow'">{{ store.translate("noti", "follow") }}</p>

                        <p class="normal_text normal_color fs_11">-{{ noti.create_time }} {{ store.translate("creator",
                                    "duration") }}-</p>
                    </div>
                </div>
                <div class="noti_item_right">
                    <button @click="delete_noti(noti.id)" class="fs_13">{{ store.translate("noti", "delete") }}</button>
                </div>
            </div>
        </div>
        <div v-else>
            <p class="normal_text normal_color fs_13 mg_l_10">{{ store.translate("noti", "no") }}</p>
        </div>
    </div>
</template>

<style>
.notification {
    height: 100%;
}

.noti_list_item {
    overflow-y: scroll;
    min-height: max-content;
    height: 470px;
}

.noti_list_item::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}

.noti_list_item::-webkit-scrollbar-track {
    background: transparent !important;
}

.noti_list_item::-webkit-scrollbar-thumb {
    background: var(--scroll_color);
    border-radius: 5px;
}

.noti_item {
    display: flex;
    width: 95%;
    justify-content: space-between;
    padding: 5px 10px;
    align-items: center;
    border-radius: 5px;
}
.noti_item:hover{
    background: var(--hover_color);
    cursor: pointer;
}
.noti_item_left{
    display: flex;
}
.noti_content{
    margin-left: 15px;
    margin-top: 10px;
}

</style>