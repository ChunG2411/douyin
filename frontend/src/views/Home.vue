<script setup>
import { Store } from '../assets/store'
import AuthenComponent from '../components/authen.vue'
import CommentComponent from '../components/comment_list.vue'
import ProfileComponent from '../components/profile_short.vue'
import { socket_noti } from '../function/socket.js'

import { ref, watch } from 'vue'
import axios from 'axios'
import { vOnClickOutside } from '@vueuse/components'

const store = Store()

const my_user = localStorage.getItem('username')
const list_video = ref([])
const page = ref(0)

const show_login_popup = ref(false)

const close_popup = [() => {
    show_login_popup.value = false
}]

// video handle
// const distance = ref([])

const player = ref(null)
const btnPlayPause = ref(null)
const btnMute = ref(null)
const progressBar = ref(null)
const volumeBar = ref(null)

const video_mute = ref(false)
const video_volumn = ref(1)


function handleVolumn() {
    for (let i = 0; i < player.value.length; i++) {
        player.value[i].volume = video_volumn.value
        volumeBar.value[i].value = video_volumn.value
    }
}

function setMute() {
    video_mute.value = !video_mute.value
    handleMute()
}
function handleMute() {
    for (let i = 0; i < player.value.length; i++) {
        player.value[i].muted = video_mute.value
    }
}

function playPauseVideo(i) {
    if (player.value[i].paused || player.value[i].ended) {
        player.value[i].play()
        list_video.value[i].play = !list_video.value[i].play
    }
    else {
        player.value[i].pause()
        list_video.value[i].play = !list_video.value[i].play
    }
}

// function replayVideo(i) {
//     player.value[i].play()
//     list_video.value[i].play = true
// }

function updatetime(i) {
    var percentage = Math.floor((100 / player.value[i].duration) * player.value[i].currentTime);
    progressBar.value[i].value = percentage;
    progressBar.value[i].innerHTML = percentage + '% played';

    var curmin = Math.floor(player.value[i].currentTime / 60)
    var cursec = Math.floor(player.value[i].currentTime - curmin * 60);
    var durmin = Math.floor(player.value[i].duration / 60)
    var dursec = Math.floor(player.value[i].duration - durmin * 60);

    if (curmin < 10) {
        curmin = '0' + curmin
    }
    if (cursec < 10) {
        cursec = '0' + cursec
    }
    if (durmin < 10) {
        durmin = '0' + durmin
    }
    if (dursec < 10) {
        dursec = '0' + dursec
    }
    list_video.value[i].time = curmin + ':' + cursec + ' / ' + durmin + ':' + dursec
}

watch(() => list_video.value.length, (currentvalue, oldvalue) => {
    setTimeout(() => {
        player.value = document.querySelectorAll('#video-element')
        btnPlayPause.value = document.querySelectorAll('#btnPlayPause')
        btnMute.value = document.querySelectorAll('#btnMute')
        progressBar.value = document.querySelectorAll('#progress-bar')
        volumeBar.value = document.querySelectorAll('#volume-bar')

        handleVolumn()
        handleMute()

        // distance.value = []
        // for (let i = 0; i < player.value.length; i++) {
        //     distance.value.push(player.value[i].scrollHeight * i)
        // }
    }, 100)
})


// main js
const get_list_video = () => {
    let header = null
    if (store.is_login) {
        header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
    }
    axios.get(`${store.domain}/api/home`, header)
        .then(response => {
            list_video.value = response.data.data.map(item => { return { ...item, showComment: false, showProfile: false, play: false, time: '00:00/00:00' } })
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
get_list_video()

const like_video = (id) => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.get(`${store.domain}/api/video/${id}/like`, header)
        .then(response => {
            for (let i = 0; i < list_video.value.length; i++) {
                if (list_video.value[i].id == id) {
                    if (response.data.data == "Liked.") {
                        list_video.value[i].liked = true
                        list_video.value[i].like_count += 1

                        //socket noti: like
                        socket_noti.send(JSON.stringify({
                            "user": localStorage.getItem('username'),
                            "video": list_video.value[i].id,
                            "type": "1"
                        }))
                    }
                    else {
                        list_video.value[i].liked = false
                        list_video.value[i].like_count -= 1
                    }
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

const save_video = (id) => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.get(`${store.domain}/api/video/${id}/save`, header)
        .then(response => {
            for (let i = 0; i < list_video.value.length; i++) {
                if (list_video.value[i].id == id) {
                    if (response.data.data == "Saved.") {
                        list_video.value[i].saved = true
                        list_video.value[i].save_count += 1
                    }
                    else {
                        list_video.value[i].saved = false
                        list_video.value[i].save_count -= 1
                    }
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


const loadMore = (e) => {
    const { scrollTop, offsetHeight, scrollHeight } = e.target

    // for (let i = 0; i < distance.value.length; i++) {
    //     if (scrollTop >= distance.value[i] - 50 && scrollTop < distance.value[i] + distance.value[1] - 50) {
    //         if (player.value[i].paused == true) {
    //             player.value[i].play()
    //             list_video.value[i].play=!list_video.value[i].play
    //             // playPauseVideo(i)
    //         }
    //     }
    //     else {
    //         if (player.value[i].paused == false) {
    //             player.value[i].pause()
    //             list_video.value[i].play=!list_video.value[i].play
    //             // playPauseVideo(i)
    //         }
    //     }
    // }

    if ((scrollTop + offsetHeight) >= scrollHeight) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        page.value += 1
        axios.get(`${store.domain}/api/home?page=${page.value}`, header)
            .then(response => {
                if (response.data.data.length == 0) {
                    page.value -= 1
                }
                else {
                    for (let i = 0; i < response.data.data.length; i++) {
                        list_video.value.push(response.data.data[i])
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
window.addEventListener('scroll', loadMore)

const increaseView = (id) => {
    axios.get(`${store.domain}/api/video/${id}/increase`)
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
    <div class="home" v-on:scroll="loadMore">
        <div class="home_video" v-for="(video, index) in list_video" :key="video.id">
            <div class="home_video_left">
                <div class="home_video_left_video">
                    <video class="video" id="video-element" :src="video.video" @click="playPauseVideo(index)"
                        @timeupdate="updatetime(index)" @ended="video.play = false; increaseView(video.id)"
                        @playing="handleMute()"></video>
                    <div class="controls">
                        <progress class="controls_bar mg_b_5" id='progress-bar' min='0' max='100' value='0'>0%
                            played</progress>
                        <div class="controls_button">
                            <div class="display_flex gap10 align_center">
                                <font-awesome-icon :icon="['fas', 'pause']" class="icon_15 white" id="btnPlayPause"
                                    v-if="video.play" @click="playPauseVideo(index)" />
                                <font-awesome-icon :icon="['fas', 'play']" class="icon_15 white" id="btnPlayPause"
                                    v-else @click="playPauseVideo(index)" />
                                <p class="video_text_2 fs_15 shadow">{{ video.time }}</p>
                            </div>
                            <div class="display_flex gap10 align_center">
                                <input type="range" id="volume-bar" min="0" max="1" step="0.1" v-model="video_volumn"
                                    @change="handleVolumn">
                                <font-awesome-icon :icon="['fas', 'volume-xmark']" class="icon_15 white" id="btnMute"
                                    @click='setMute' v-if="video_mute" />
                                <font-awesome-icon :icon="['fas', 'volume-high']" class="icon_15 white" id="btnMute"
                                    @click='setMute' v-else />
                            </div>
                        </div>
                    </div>
                </div>

                <div class="home_video_left_action">
                    <img class="profile_avatar_video" :src="store.domain + video.user_infor.avatar"
                        @click="video.showProfile = !video.showProfile; video.showComment = false">

                    <div @click="like_video(video.id)" class="display_flex_column align_center poiter">
                        <font-awesome-icon :icon="['fas', 'heart']" class="icon_25 red" v-if="video.liked" />
                        <font-awesome-icon :icon="['fas', 'heart']" class="icon_25 white" v-else />
                        <p class="video_text_2 fs_15 shadow">{{ video.like_count }}</p>
                    </div>

                    <div @click="video.showComment = !video.showComment; video.showProfile = false"
                        class="display_flex_column align_center poiter">
                        <font-awesome-icon :icon="['fas', 'message']" class="icon_20 white" />
                        <p class="video_text_2 fs_15 shadow">{{ video.comment_count }}</p>
                    </div>

                    <div @click="save_video(video.id)" class="display_flex_column align_center poiter">
                        <font-awesome-icon :icon="['fas', 'star']" class="icon_20 yellow" v-if="video.saved" />
                        <font-awesome-icon :icon="['fas', 'star']" class="icon_20 white" v-else />
                        <p class="video_text_2 fs_15 shadow">{{ video.save_count }}</p>
                    </div>
                </div>

                <div class="home_video_left_infor">
                    <div>
                        <div class="display_flex align_center gap10">
                            <router-link :to="{ name: 'guest_profile', params: { username: video.user_infor.username } }"
                                v-if="my_user != video.user_infor.username" class="video_text_1 fs_17 no_decor shadow">
                                {{ video.user_infor.full_name }}
                            </router-link>
                            <router-link to="/profile/self" v-else class="video_text_1 fs_17 no_decor shadow">
                                {{ video.user_infor.full_name }}
                            </router-link>
                            <p class="video_text_2 fs_10 shadow">-{{ video.create_time }} {{
                                store.translate("creator",
                                    "duration") }}-</p>
                        </div>
                        <p class="video_text_2 fs_15 shadow">{{ video.descrip }}</p>
                    </div>

                    <router-link :to="{ name: 'music', params: { id: video.music } }" v-if="video.music">
                        <img class="avatar_music_icon" :src="store.domain + video.music_avatar">
                    </router-link>
                    <img class="avatar_music_icon" :src="store.domain + video.user_infor.avatar" v-else>
                </div>
            </div>

            <div class="home_video_right" v-if="video.showComment || video.showProfile">
                <div class="home_video_right_board" v-if="video.showComment">
                    <p class="text normal_color fs_17 pd_b_10">{{ store.translate("comment", "comment") }}</p>
                    <CommentComponent :video_id="video.id" />
                </div>
                <div class="home_video_right_board" v-if="video.showProfile">
                    <ProfileComponent :username="video.user_infor.username" />
                </div>
            </div>
        </div>
    </div>

    <div class="popup" v-if="show_login_popup">
        <div class="popup_board" v-if="show_login_popup">
            <AuthenComponent v-on-click-outside="close_popup" />
        </div>
    </div>
</template>

<style>
.home {
    width: 98%;
    height: 99%;
    display: flex;
    flex-direction: column;
    gap: 20px;
    overflow-y: auto;
    padding-right: 10px;
}

.home::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}

.home::-webkit-scrollbar-track {
    background: transparent !important;
}

.home::-webkit-scrollbar-thumb {
    background: var(--scroll_color);
    border-radius: 5px;
}

.home_video {
    width: 100%;
    height: 100%;
    min-height: 100%;
    background: var(--background_video);
    border-radius: 10px;
    display: flex;
    box-shadow: 0 0 1px var(--boder_color);
    justify-content: center;
}

.home_video_left {
    width: auto;
    height: 100%;
    display: flex;
    align-items: center;
    position: relative;
}

.home_video_left_video {
    height: 100%;
    width: 100%;
    position: relative;
}

.home_video_left_action {
    position: absolute;
    display: flex;
    right: 10px;
    bottom: 200px;
    flex-direction: column;
    gap: 20px;
    align-items: center;
}

.home_video_left_infor {
    position: absolute;
    display: flex;
    left: 10px;
    bottom: 50px;
    align-items: center;
    justify-content: space-between;
    width: 97%;
}

.home_video_right {
    width: 40%;
}

.home_video_right_board {
    width: 90%;
    height: 97%;
    overflow: hidden;
    padding: 10px;
}

/* --------------------------------------video player------------------------------- */
.video {
    width: 100%;
    height: 100%;
}

.controls {
    position: absolute;
    display: flex;
    flex-direction: column;
    bottom: 5px;
    width: 99%;
    padding: 5px;
}

.controls_bar {
    width: 100%;
    height: 5px;
}

.controls_button {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 95%;
    padding: 0 20px 0 20px;
}

#volume-bar {
    width: 100px;
    height: 5px;
    cursor: pointer;
    overflow: hidden;
    border-radius: 5px;
    background: var(--text_color);
}
</style>