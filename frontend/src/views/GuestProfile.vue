<script setup>
import VideoListComponent from '../components/video_list.vue'
import { Store } from '../assets/store.js'
import { socket_noti } from '../function/socket.js'

import { reactive, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { vOnClickOutside } from '@vueuse/components'


const store = Store()
const route = useRoute()

watch(() => route.params.username, (currentvalue, oldvalue) => {
    api_get_user_infor(currentvalue)
    check_follow(currentvalue)
})

const profile = reactive({
    infor: null,
    followed: null,
    follower: null,
    follow_status: null,
    active_tab: "video"
})

const show_followed_popup = ref(false)
const show_follower_popup = ref(false)
const show_avatar_popup = ref(false)


const close_popup = [() => {
    show_followed_popup.value = false
    show_follower_popup.value = false
    show_avatar_popup.value = false
}]

const api_get_user_infor = (username) => {
    axios.get(`${store.domain}/api/user/${username}`)
        .then(response => {
            profile.infor = response.data.data
            profile.active_tab = "video"
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
api_get_user_infor(route.params.username)


const api_get_followed = () => {
    axios.get(`${store.domain}/api/user/${profile.infor.username}/followed-list`)
        .then(response => {
            profile.followed = response.data.data
        })
        .catch(e => {
            try {
                store.msg_error = error.response.data.msg
            }
            catch {
                store.msg_error = error
            }
        })
}
const api_get_follower = () => {
    axios.get(`${store.domain}/api/user/${profile.infor.username}/follower-list`)
        .then(response => {
            profile.follower = response.data.data
        })
        .catch(e => {
            try {
                store.msg_error = error.response.data.msg
            }
            catch {
                store.msg_error = error
            }
        })
}

const show_followed = () => {
    show_followed_popup.value = true
    api_get_followed()
}

const show_follower = () => {
    show_follower_popup.value = true
    api_get_follower()
}


const check_follow = (username) => {
    if (store.is_login) {
        axios.get(`${store.domain}/api/user/${localStorage.getItem('username')}/followed-list`)
            .then(response => {
                for (let i = 0; i < response.data.data.length; i++) {
                    if (response.data.data[i].username == username) {
                        profile.follow_status = true
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
check_follow(route.params.username)


const follow = () => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.get(`${store.domain}/api/user/${profile.infor.username}/follow`, header)
        .then(response => {
            profile.follow_status = true

            //socket noti: like
            socket_noti.send(JSON.stringify({
                "user": localStorage.getItem('username'),
                "video": '',
                "user_receive": profile.infor.username,
                "type": "5"
            }))
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

const unfollow = () => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.get(`${store.domain}/api/user/${profile.infor.username}/follow`, header)
        .then(response => {
            profile.follow_status = false
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
    <div class="profile">
        <div class="profile_infor" v-if="profile.infor">
            <div class="profile_infor_left">
                <div class="profile_infor_avatar">
                    <img class="profile_avatar" :src="store.domain + profile.infor.avatar"
                        @click="show_avatar_popup = true">
                </div>
                <div class="profile_infor_content">
                    <div>
                        <p class="fullname fs_20">{{ profile.infor.full_name }}</p>
                        <p class="username gray fs_13">@{{ profile.infor.username }}</p>
                    </div>
                    <div class="profile_follow_infor">
                        <button @click="show_followed" class="fs_13">{{store.translate("profile", "followed")}}: {{ profile.infor.followed_count }}</button>
                        <button @click="show_follower" class="fs_13">{{store.translate("profile", "follower")}}: {{ profile.infor.follower_count }}</button>
                    </div>
                    <div class="display_flex_column gap5">
                        <div class="display_flex gap10">
                            <div class="display_flex gap5 align_center">
                                <font-awesome-icon :icon="['fas', 'transgender']" class="icon gray" />
                                <p class="normal_text gray fs_13" v-if="profile.infor.gender">{{ profile.infor.gender }}</p>
                            </div>
                            <div class="display_flex gap5 align_center">
                                <font-awesome-icon :icon="['fas', 'cake-candles']" class="icon gray" />
                                <p class="normal_text gray fs_13" v-if="profile.infor.birth">{{ profile.infor.birth }}</p>
                            </div>
                        </div>
                        <p class="normal_text gray fs_13" v-if="profile.infor.address">{{ profile.infor.address }}</p>
                        <p class="normal_text gray fs_15" v-if="profile.infor.introduce">{{ profile.infor.introduce }}</p>
                    </div>
                </div>
            </div>
            <div class="profile_infor_right" v-if="store.is_login">
                <button @click="unfollow" v-if="profile.follow_status" class="fs_15">{{store.translate("profile", "unfollow")}}</button>
                <button @click="follow" v-else class="fs_15">{{store.translate("profile", "follow")}}</button>
            </div>
        </div>

        <div class="profile_video">
            <div class="profile_video_tag">
                <div class="tag_item active_tag" id="created" @click="profile.active_tab = 'video'">
                    <p class="text normal_color fs_15">{{store.translate("profile", "create")}}</p>
                </div>
            </div>
            <VideoListComponent :active="profile.active_tab" :username="route.params.username" />
        </div>

        <div class="popup" v-if="show_followed_popup || show_follower_popup || show_avatar_popup">
            <div class="popup_board" id="followed_popup" v-if="show_followed_popup" v-on-click-outside="close_popup">
                <p class="text normal_color fs_17">{{store.translate("profile", "followed")}}</p>
                <div class="follow_board">
                    <div class="follow_board_item poiter" v-for="user in profile.followed">
                        <div class="follow_context">
                            <img class="profile_avatar_folllow" :src="store.domain + user.avatar">
                            <p class="text normal_color fs_15">{{ user.full_name }}</p>
                        </div>
                        <button>
                            <router-link class="text normal_color fs_15"
                                :to="{ name: 'guest_profile', params: { username: user.username } }">{{store.translate("search", "view")}}</router-link>
                        </button>
                    </div>
                </div>
            </div>
            <div class="popup_board" id="follower_popup" v-if="show_follower_popup" v-on-click-outside="close_popup">
                <p class="text normal_color fs_17">{{store.translate("profile", "follower")}}</p>
                <div class="follow_board">
                    <div class="follow_board_item poiter" v-for="user in profile.follower">
                        <div class="follow_context">
                            <img class="profile_avatar_folllow" :src="store.domain + user.avatar">
                            <p class="text normal_color fs_15">{{ user.full_name }}</p>
                        </div>
                        <button>
                            <router-link class="text normal_color fs_15"
                                :to="{ name: 'guest_profile', params: { username: user.username } }">{{store.translate("search", "view")}}</router-link>
                        </button>
                    </div>
                </div>
            </div>

            <div class="popup_board" id="avatar_popup" v-if="show_avatar_popup" v-on-click-outside="close_popup">
                <img class="show_profile_avatar" :src="store.domain + profile.infor.avatar" />
            </div>
        </div>
    </div>
</template>

<style>
.profile {
    width: 98%;
    height: 100%;
}

.profile_infor {
    width: 97%;
    height: 30%;
    padding: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.profile_infor_left {
    display: flex;
}

.profile_infor_avatar {
    padding: 10px 20px;
}

.fullname {
    font-size: 20px;
    font-weight: 500;
    color: var(--text_color);
    margin-bottom: 0;
}

.username {
    font-size: 13px;
    font-weight: 350;
    color: var(--text_color);
    margin: 0;
}

.profile_follow_infor {
    margin: 5px 0 5px 0;
    display: flex;
    gap: 5px;
}

.profile_video {
    width: 97%;
    height: 65%;
    padding: 10px;
}

.profile_video_tag {
    display: flex;
    width: 100%;
    padding: 5px;
    height: 20px;
    margin-bottom: 10px;
    align-items: center;
}

.tag_item {
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
}

.active_tag {
    background: var(--hover_color);
}

.follow_board {
    height: 93%;
    overflow-y: scroll;
    display: flex;
    flex-direction: column;
    margin-top: 10px;
}

.follow_board::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}

.follow_board::-webkit-scrollbar-track {
    background: transparent !important;
}

.follow_board::-webkit-scrollbar-thumb {
    background: var(--scroll_color);
    border-radius: 5px;
}

.follow_board_item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
    align-items: center;
    padding: 10px;
    border-radius: 10px;
}

.follow_board_item:hover {
    background: var(--hover_color);
}

.follow_context {
    display: flex;
    gap: 10px;
    align-items: center;
}
</style>