<script setup>
import { Store } from '../assets/store'
import AuthenComponent from '../components/authen.vue'
import CommentComponent from '../components/comment_list.vue'
import ProfileComponent from '../components/profile_short.vue'
import VideoComponent from '../components/video_tag.vue'
import { socket_noti } from '../function/socket.js'

import { ref, reactive, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { vOnClickOutside } from '@vueuse/components'

const store = Store()
const route = useRoute()


watch(() => route.params.id, (currentvalue, oldvalue) => {
    api_get_video(currentvalue)
})

const my_user = localStorage.getItem('username')
const video = ref(null)

const show_login_popup = ref(false)

const show_component = reactive({
    comment: false,
    profile: false
})


const close_popup = [() => {
    show_login_popup.value = false
}]


const api_get_video = (id) => {
    let header = null
    if (store.is_login) {
        header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
    }
    axios.get(`${store.domain}/api/video/${id}`, header)
        .then(response => {
            video.value = response.data.data

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
api_get_video(route.params.id)

const like_video = () => {
    if (store.is_login) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        axios.get(`${store.domain}/api/video/${route.params.id}/like`, header)
            .then(response => {
                if (response.data.data == "Liked.") {
                    video.value.liked = true
                    video.value.like_count += 1

                    //socket noti: like
                    socket_noti.send(JSON.stringify({
                        "user": localStorage.getItem('username'),
                        "video": video.value.id,
                        "type": "1"
                    }))
                }
                else {
                    video.value.liked = false
                    video.value.like_count -= 1
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
    else {
        show_login_popup.value = true
    }
}

const save_video = () => {
    if (store.is_login) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        axios.get(`${store.domain}/api/video/${route.params.id}/save`, header)
            .then(response => {
                if (response.data.data == "Saved.") {
                    video.value.saved = true
                    video.value.save_count += 1
                }
                else {
                    video.value.saved = false
                    video.value.save_count -= 1
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
    else {
        show_login_popup.value = true
    }
}


const handle_show_component = (target) => {
    if (target == "comment") {
        show_component.comment = !show_component.comment
        show_component.profile = false
    }
    else {
        show_component.comment = false
        show_component.profile = !show_component.profile
    }
}

</script>

<template>
    <div class="video_view" v-if="video">
        <div class="video_view_left">
            <div class="video_view_video">
                <VideoComponent :src="video.video"/>
            </div>

            <div class="video_view_action">
                <img class="profile_avatar_video" :src="store.domain + video.user_infor.avatar"
                    @click="handle_show_component('profile')">

                <div @click="like_video" class="display_flex_column align_center poiter">
                    <font-awesome-icon :icon="['fas', 'heart']" class="icon_25 red" v-if="video.liked" />
                    <font-awesome-icon :icon="['fas', 'heart']" class="icon_25 white" v-else />
                    <p class="normal_text normal_color fs_15">{{ video.like_count }}</p>
                </div>

                <div @click="handle_show_component('comment')" class="display_flex_column align_center poiter">
                    <font-awesome-icon :icon="['fas', 'message']" class="icon_20 white" />
                    <p class="normal_text normal_color fs_15">{{ video.comment_count }}</p>
                </div>

                <div @click="save_video" class="display_flex_column align_center poiter">
                    <font-awesome-icon :icon="['fas', 'star']" class="icon_20 yellow" v-if="video.saved" />
                    <font-awesome-icon :icon="['fas', 'star']" class="icon_20 white" v-else />
                    <p class="normal_text normal_color fs_15">{{ video.save_count }}</p>
                </div>
            </div>

            <div class="video_view_infor">
                <div>
                    <router-link :to="{ name: 'guest_profile', params: { username: video.user_infor.username } }"
                        v-if="my_user != video.user_infor.username" class="text normal_color fs_17 no_decor shadow">
                        {{ video.user_infor.full_name }}
                    </router-link>
                    <router-link to="/profile/self" v-else class="text normal_color fs_17 no_decor shadow">
                        {{ video.user_infor.full_name }}
                    </router-link>
                    <p class="normal_text normal_color fs_15 shadow">{{ video.descrip }}</p>
                </div>

                <router-link :to="{ name: 'music', params: { id: video.music } }" v-if="video.music">
                    <img class="profile_avatar_video" :src="store.domain + video.user_infor.avatar">
                </router-link>
                <img class="profile_avatar_video" :src="store.domain + video.user_infor.avatar" v-else>
            </div>
        </div>

        <div class="video_view_right" v-if="show_component.comment || show_component.profile">
            <div class="right_board" v-if="show_component.comment">
                <p class="text normal_color fs_17 pd_b_10">Comment</p>
                <CommentComponent :video_id="video.id" />
            </div>
            <div class="right_board" v-if="show_component.profile">
                <ProfileComponent :username="video.user_infor.username" />
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
.video_view {
    width: 90%;
    height: 90%;
    margin-left: 10px;
    border-radius: 10px;
    display: flex;
    overflow: hidden;
    background: var(--background_video);
    box-shadow: 0 0 1px var(--boder_color);
    justify-content: center;
}

.video_view_left {
    width: auto;
    height: 100%;
    display: flex;
    align-items: center;
    position: relative;
}

.video_view_video{
    height: 100%;
    width: 100%;
}

.video_view_action {
    position: absolute;
    display: flex;
    right: 10px;
    bottom: 200px;
    flex-direction: column;
    gap: 20px;
    align-items: center;
}

.video_view_infor {
    position: absolute;
    display: flex;
    left: 10px;
    bottom: 50px;
    align-items: center;
    justify-content: space-between;
    width: 97%;
}

.video_view_right {
    width: 40%;
}

.right_board {
    width: 90%;
    height: 97%;
    overflow: hidden;
    padding: 10px;
}
</style>