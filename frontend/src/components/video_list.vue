<script setup>
import { Store } from '../assets/store'

import { ref, defineProps, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
    active: String,
    username: String
})

const top_page = ref(null)

watch(props, (oldvalue, currentvalue) => {
    api_get_video_list(currentvalue.active)
    scrollToElement(top_page.value)
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
window.addEventListener('scroll', loadMoreVideo)

const scrollToElement = (element) => {
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
}

</script>

<template>
    <div class="video_list" v-on:scroll="loadMoreVideo">
        <div ref="top_page" style="display: none;"></div>
        <div class="video_card" v-if="video_list" v-for="video in video_list" :key="video.id">
            <router-link class="normal_text normal_color no_decor" :to="{ name: 'video', params: { id: video.id } }">
                <video class="profile_video_card" :src="store.domain + video.video" />
                <div class="card_content">
                    <div>
                        <p class="normal_text normal_color fs_13">{{ video.descrip.slice(0,15) }}...</p>
                    </div>
                    <div class="card_content_action">
                        <div>
                            <font-awesome-icon :icon="['fas', 'heart']" class="icon white" />
                            <p class="normal_text normal_color fs_13">{{ video.like_count }}</p>
                        </div>
                        <div>
                            <font-awesome-icon :icon="['fas', 'comment']" class="icon white" />
                            <p class="normal_text normal_color fs_13">{{ video.comment_count }}</p>
                        </div>
                        <div>
                            <font-awesome-icon :icon="['fas', 'star']" class="icon white" />
                            <p class="normal_text normal_color fs_13">{{ video.save_count }}</p>
                        </div>
                    </div>
                </div>
            </router-link>
        </div>
    </div>
</template>

<style>
.video_list {
    overflow-y: scroll;
    margin-top: 10px;
    height: 90%;
    width: 100%;
    max-width: 850px;
    display: grid;
    grid-template-columns: repeat(auto-fit, 150px);
    padding: 5px 0 0 5px;
    gap: 10px;
}

.video_list::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}

.video_list::-webkit-scrollbar-track {
    background: transparent !important;
}

.video_list::-webkit-scrollbar-thumb {
    background: var(--scroll_color);
    border-radius: 5px;
}

.video_card {
    width: 150px;
    height: 280px;
    border-radius: 10px;
    background: var(--hover_color);
    position: relative;
}

.card_content {
    position: absolute;
    bottom: 0;
    height: max-content;
    width: 88%;
    padding: 5px 10px;
}
.card_content_action{
    display: flex;
    justify-content: space-between;
}
.card_content_action div{
    display: flex;
    gap: 2px;
    align-items: center;
}
</style>