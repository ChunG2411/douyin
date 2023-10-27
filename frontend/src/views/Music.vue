<script setup>
import { Store } from '../assets/store'
import VideoListComponent from '../components/video_list.vue'

import { useRoute } from 'vue-router'
import { ref } from 'vue'
import axios from 'axios'


const store = Store()
const route = useRoute()

const my_user = localStorage.getItem('username')
const music = ref(null)
const videos = ref(null)
const page_video_of_music = ref(0)

const api_get_music = () => {
    let header = null
    if (store.is_login) {
        header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
    }
    axios.get(`${store.domain}/api/music/${route.params.id}`, header)
        .then(response => {
            music.value = response.data.data
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
api_get_music()

const api_get_video_of_music = () => {
    let header = null
    if (store.is_login) {
        header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
    }
    axios.get(`${store.domain}/api/music/${route.params.id}/video`, header)
        .then(response => {
            videos.value = response.data.data
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
api_get_video_of_music()

const loadMoreVideo_of_music = (e) => {
    const { scrollTop, offsetHeight, scrollHeight } = e.target
    if ((scrollTop + offsetHeight) >= scrollHeight) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        page_video_of_music.value += 1
        axios.get(`${store.domain}/api/music/${route.params.id}/video?page=${page_video_of_music.value}`, header)
            .then(response => {
                if (response.data.data.length == 0) {
                    page_video_of_music.value -= 1
                }
                else {
                    for (let i = 0; i < response.data.data.length; i++) {
                        videos.value.push(response.data.data[i])
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
window.addEventListener('scroll', loadMoreVideo_of_music);

</script>

<template>
    <div class="music">
        <div class="music_infor" v-if="music">
            <div>
                <img class="avatar_music" :src="store.domain + music.user_infor.avatar" />
            </div>
            <div>
                <p class="text normal_color fs_20">Music created by {{ music.user_infor.full_name }}</p>
                <router-link :to="{ name: 'guest_profile', params: { username: music.user_infor.username } }"
                    v-if="my_user != music.user_infor.username" class="normal_text normal_color no_decor fs_15">{{
                        music.user_infor.full_name }}
                </router-link>
                <router-link to="/profile/self" v-else class="normal_text normal_color no_decor fs_15">
                    {{ music.user_infor.full_name }}
                </router-link>
                <p class="normal_text normal_color fs_13">{{ music.video_count }} used</p>
            </div>
        </div>

        <div class="music_video" v-if="videos">
            <div class="music_video_list" v-on:scroll="loadMoreVideo_of_music">
                <div class="video_card" v-for="video in videos">
                    <router-link class="normal_text normal_color no_decor"
                        :to="{ name: 'video', params: { id: video.id } }">
                        <video class="profile_video_card" :src="store.domain + video.video" />
                        <div class="card_content">
                            <div class="card_content_action">
                                <div>
                                    <font-awesome-icon :icon="['fas', 'heart']" class="icon white" />
                                    <p class="normal_text normal_color fs_13">{{ video.like_count }}</p>
                                </div>
                            </div>
                        </div>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
.music {
    width: 87%;
    height: 90%;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.music_infor {
    height: 25%;
    width: 95%;
    padding: 10px 20px 0 20px;
    display: flex;
    gap: 20px;
}

.music_video {
    width: 95%;
    height: 70%;
    padding: 0 20px;
}

.music_video_list {
    overflow-y: scroll;
    height: 100%;
    width: 100%;
    max-width: 850px;
    display: grid;
    grid-template-columns: repeat(auto-fit, 150px);
    gap: 10px;
}

.music_video_list::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}

.music_video_list::-webkit-scrollbar-track {
    background: transparent !important;
}

.music_video_list::-webkit-scrollbar-thumb {
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