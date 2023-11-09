<script setup>
import { Store } from '../assets/store'
import AuthenComponent from '../components/authen.vue'
import CommentComponent from '../components/comment_list.vue'

import { ref, reactive, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { vOnClickOutside } from '@vueuse/components'
import axios from 'axios'


const route = useRoute()
const store = Store()

watch(() => route.params.text, (currentvalue, oldvalue) => {
    search_video()
    resetActive_search()
})

const active_bar = ref('video')
const my_user = localStorage.getItem('username')
const search_result = reactive({
    video: [],
    user: []
})
const show_login_popup = ref(false)
const page_search_video = ref(0)
const page_search_user = ref(0)


const close_popup = [() => {
    show_login_popup.value = false
    for (let i = 0; i < search_result.video.length; i++) {
        search_result.video[i].showComment = false
    }
}]


const api_search_video = () => {
    let header = null
    if (store.is_login) {
        header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
    }
    if (route.params.text) {
        axios.get(`${store.domain}/api/search/video?text=${route.params.text}`, header)
            .then(response => {
                if (response.data.data.length > 0) {
                    search_result.video = response.data.data.map(item => { return { ...item, showComment: false } })
                }
                else {
                    search_result.video = []
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

const api_search_user = () => {
    let header = null
    if (store.is_login) {
        header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
    }
    axios.get(`${store.domain}/api/search/user?text=${route.params.text}`, header)
        .then(response => {
            if (response.data.data.length > 0) {
                search_result.user = response.data.data
            }
            else {
                search_result.user = []
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

const search_video = () => {
    active_bar.value = 'video'
    api_search_video()
}
search_video()

const search_user = () => {
    active_bar.value = 'user'
    api_search_user()
}

const like_video = (id) => {
    if (store.is_login) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        axios.get(`${store.domain}/api/video/${id}/like`, header)
            .then(response => {
                if (response.data.data == "Liked.") {
                    for (let i = 0; i < search_result.video.length; i++) {
                        if (search_result.video[i].id == id) {
                            search_result.video[i].liked = true
                            search_result.video[i].like_count += 1
                        }
                    }
                }
                else {
                    for (let i = 0; i < search_result.video.length; i++) {
                        if (search_result.video[i].id == id) {
                            search_result.video[i].liked = false
                            search_result.video[i].like_count -= 1
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
    else {
        show_login_popup.value = true
    }
}

const save_video = (id) => {
    if (store.is_login) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        axios.get(`${store.domain}/api/video/${id}/save`, header)
            .then(response => {
                if (response.data.data == "Saved.") {
                    for (let i = 0; i < search_result.video.length; i++) {
                        if (search_result.video[i].id == id) {
                            search_result.video[i].saved = true
                            search_result.video[i].save_count += 1
                        }
                    }
                }
                else {
                    for (let i = 0; i < search_result.video.length; i++) {
                        if (search_result.video[i].id == id) {
                            search_result.video[i].saved = false
                            search_result.video[i].save_count -= 1
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
    else {
        show_login_popup.value = true
    }
}

const loadMoreSearch_user = (e) => {
    const { scrollTop, offsetHeight, scrollHeight } = e.target
    if ((scrollTop + offsetHeight) >= scrollHeight) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        page_search_user.value += 1
        axios.get(`${store.domain}/api/search/user?text=${route.params.text}&page=${page_search_user.value}`, header)
            .then(response => {
                if (response.data.data.length == 0) {
                    page_search_user.value -= 1
                }
                else {
                    for (let i = 0; i < response.data.data.length; i++) {
                        search_result.user.push(response.data.data[i])
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

const loadMoreSearch_video = (e) => {
    const { scrollTop, offsetHeight, scrollHeight } = e.target
    if ((scrollTop + offsetHeight) >= scrollHeight) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        page_search_video.value += 1
        axios.get(`${store.domain}/api/search/video?text=${route.params.text}&page=${page_search_video.value}`, header)
            .then(response => {
                if (response.data.data.length == 0) {
                    page_search_video.value -= 1
                }
                else {
                    for (let i = 0; i < response.data.data.length; i++) {
                        search_result.video.push(response.data.data[i])
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

window.addEventListener('scroll', loadMoreSearch_user);
window.addEventListener('scroll', loadMoreSearch_video);

// active tag
const search_tag = ref(null)

const removeActive_search = () => {
    search_tag.value.forEach(item => {
        item.classList.remove('active_search_tag')
    })
}
const resetActive_search = () => {
    search_tag.value.forEach(item => {
        if (item.id == 'video') {
            item.classList.add('active_search_tag')
        }
        else {
            item.classList.remove('active_search_tag')
        }
    })
}

onMounted(() => {
    search_tag.value = document.querySelectorAll('.search_tag')
    search_tag.value.forEach(item => {
        item.addEventListener('click', () => {
            removeActive_search()
            item.classList.add('active_search_tag')
        })
    })
})

</script>

<template>
    <div class="search_view">
        <div class="search_view_bar">
            <button class="search_tag active_search_tag" id="video" @click="search_video">{{store.translate("search", "video")}}</button>
            <button class="search_tag" id="user" @click="search_user">{{store.translate("search", "user")}}</button>
        </div>

        <div class="search_board">
            <div class="search_board_user" v-if="active_bar == 'user'" v-on:scroll="loadMoreSearch_user">
                <div class="item_user_search" v-if="search_result.user.length > 0" v-for="user in search_result.user"
                    :key="user.id">
                    <div class="display_flex gap20 align_center">
                        <img class="profile_user_search" :src="store.domain + user.avatar">
                        <p class="text normal_color fs_15">{{ user.full_name }}</p>
                    </div>
                    <router-link class="button no_decor"
                        :to="{ name: 'guest_profile', params: { username: user.username } }">{{store.translate("search", "view")}}</router-link>
                </div>
                <div v-else>
                    <p class="normal_text normal_color fs_15">{{store.translate("search", "no")}}</p>
                </div>
            </div>

            <div class="search_board_video" v-else-if="active_bar == 'video'" v-on:scroll="loadMoreSearch_video">
                <div class="item_video_search" v-if="search_result.video.length > 0" v-for="video in search_result.video"
                    :key="video.id">

                    <div class="item_video_search_left">
                        <router-link :to="{ name: 'guest_profile', params: { username: video.user_infor.username } }"
                            v-if="my_user != video.user_infor.username" class="display_flex gap15 align_center no_decor">
                            <img class="profile_video_search" :src="store.domain + video.user_infor.avatar">
                            <p class="text normal_color fs_17">{{ video.user_infor.full_name }}</p>
                        </router-link>
                        <router-link to="/profile/self" v-else class="display_flex gap15 align_center no_decor">
                            <img class="profile_video_search" :src="store.domain + video.user_infor.avatar">
                            <p class="text normal_color fs_17">{{ video.user_infor.full_name }}</p>
                        </router-link>

                        <div class="display_flex_column gap10 mg_t_10 mg_b_10">
                            <p class="normal_text normal_color fs_15">{{ video.descrip }}</p>
                            <video class="video_search" :src="video.video" controls />
                        </div>

                        <div class="item_video_search_action">
                            <div @click="like_video(video.id)" class="search_action_item">
                                <font-awesome-icon :icon="['fas', 'heart']" class="icon_20 red" v-if="video.liked" />
                                <font-awesome-icon :icon="['fas', 'heart']" class="icon_20 white" v-else />
                                <p class="normal_text normal_color fs_15">{{ video.like_count }}</p>
                            </div>
                            <div @click="video.showComment = !video.showComment" class="search_action_item">
                                <font-awesome-icon :icon="['fas', 'message']" class="icon_20 white" />
                                <p class="normal_text normal_color fs_15">{{ video.comment_count }}</p>
                            </div>
                            <div @click="save_video(video.id)" class="search_action_item">
                                <font-awesome-icon :icon="['fas', 'star']" class="icon_20 yellow" v-if="video.saved" />
                                <font-awesome-icon :icon="['fas', 'star']" class="icon_20 white" v-else />
                                <p class="normal_text normal_color fs_15">{{ video.save_count }}</p>
                            </div>
                        </div>
                    </div>

                    <div class="item_video_search_right" v-if="video.showComment">
                        <div class="item_video_search_right_board">
                            <p class="text normal_color fs_17 pd_b_10">{{store.translate("comment", "comment")}}</p>
                            <CommentComponent :video_id="video.id" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="popup" v-if="show_login_popup">
        <div class="popup_board">
            <AuthenComponent v-on-click-outside="close_popup" />
        </div>
    </div>
</template>

<style>
.search_view {
    width: 98%;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 5px;
    padding: 10px;
}

.search_view_bar {
    display: flex;
    gap: 10px;
    width: 100%;
    height: max-content;
}

.active_search_tag {
    background: var(--hover_color);
}

.search_board {
    width: 100%;
    height: 92%;
    padding: 10px;
}

.search_board_user {
    display: flex;
    flex-direction: column;
    gap: 20px;
    overflow-y: scroll;
    width: 100%;
    height: 100%;
}

.search_board_user::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}

.search_board_user::-webkit-scrollbar-track {
    background: transparent !important;
}

.search_board_user::-webkit-scrollbar-thumb {
    background: var(--scroll_color);
    border-radius: 5px;
}

.item_user_search {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    border-radius: 10px;
    margin-right: 10px;
}

.item_user_search:hover {
    background: var(--hover_color);
}

.search_board_video {
    display: flex;
    flex-direction: column;
    gap: 20px;
    overflow-y: scroll;
    width: 100%;
    height: 100%;
}

.search_board_video::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}

.search_board_video::-webkit-scrollbar-track {
    background: transparent !important;
}

.search_board_video::-webkit-scrollbar-thumb {
    background: var(--scroll_color);
    border-radius: 5px;
}

.item_video_search {
    display: flex;
    height: max-content;
    gap: 20px;
    border-radius: 10px;
    background: var(--background_video);
    margin-right: 10px;
    padding: 10px 20px;
}

.item_video_search_left{
    width: auto;
    display: flex;
    flex-direction: column;
}

.item_video_search_action {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 30px;
}

.search_action_item {
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
    padding: 10px 30px;
    border-radius: 10px;
}

.search_action_item:hover {
    background: var(--hover_color);
}

.item_video_search_right{
    width: 30%;
    height: 670px;
}

.item_video_search_right_board{
    width: 90%;
    height: 100%;
    overflow: hidden;
}
</style>