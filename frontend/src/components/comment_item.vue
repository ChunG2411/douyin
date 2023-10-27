<script setup>
import { Store } from '../assets/store'
import CommentItemRecursive from './comment_item_Recursive.vue'

import { ref, defineProps } from 'vue'
import axios from 'axios'
import { socket_noti } from '../function/socket.js'


const props = defineProps({
    data: Object
})

const store = Store()
const my_user = localStorage.getItem('username')

const show_this_comment = ref(true)
const child_comment = ref([])
const show_child_comment = ref(false)
const page_comment_child = ref(0)


const api_get_child_comment = () => {
    let header = null
    if (store.is_login) {
        header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
    }
    axios.get(`${store.domain}/api/video/${props.data.video}/comment-list?parent=${props.data.id}`, header)
        .then(response => {
            child_comment.value = response.data.data
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

const like_comment = () => {
    if (store.is_login) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        axios.get(`${store.domain}/api/comment/${props.data.id}/like`, header)
            .then(response => {
                if (response.data.data == "Liked.") {
                    props.data.liked = true
                    props.data.like_count += 1

                    //socket noti: like comment
                    socket_noti.send(JSON.stringify({
                        "user": localStorage.getItem('username'),
                        "video": props.data.video,
                        "comment": props.data.id,
                        "type": "3"
                    }))
                }
                else {
                    props.data.liked = false
                    props.data.like_count -= 1
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

const add_parent = () => {
    if (store.is_login) {
        store.comment_tag.comment_id = props.data.id
        store.comment_tag.video_id = props.data.video
        store.comment_tag.full_name = props.data.user_infor.full_name
    }
}

const get_child_comment = () => {
    show_child_comment.value = !show_child_comment.value
    if (show_child_comment.value) {
        api_get_child_comment()
    }
    else {
        child_comment.value = []
    }
}

const delete_comment = () => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.delete(`${store.domain}/api/comment/${props.data.id}`, header)
        .then(response => {
            show_this_comment.value = false
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

const loadMoreComment_child = (e) => {
    const { scrollTop, offsetHeight, scrollHeight } = e.target
    if ((scrollTop + offsetHeight) >= scrollHeight) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        page_comment_child.value += 1
        axios.get(`${store.domain}/api/video/${props.data.video}/comment-list?parent=${props.data.id}&page=${page_comment_child.value}`, header)
            .then(response => {
                if (response.data.data.length == 0) {
                    page_comment_child.value -= 1
                }
                else {
                    for (let i = 0; i < response.data.data.length; i++) {
                        child_comment.value.push(response.data.data[i])
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
window.addEventListener('scroll', loadMoreComment_child);

</script>

<template>
    <div class="comment_item" v-if="show_this_comment">
        <div>
            <router-link :to="{ name: 'guest_profile', params: { username: props.data.user_infor.username } }"
                v-if="my_user != props.data.user_infor.username">
                <img class="profile_avatar_video" :src="store.domain + props.data.user_infor.avatar">
            </router-link>
            <router-link to="/profile/self" v-else>
                <img class="profile_avatar_video" :src="store.domain + props.data.user_infor.avatar">
            </router-link>
        </div>

        <div class="comment_content">
            <div>
                <router-link :to="{ name: 'guest_profile', params: { username: props.data.user_infor.username } }"
                    v-if="my_user != props.data.user_infor.username" class="text normal_color fs_15">
                    {{ props.data.user_infor.full_name }}
                </router-link>
                <router-link to="/profile/self" v-else class="text normal_color fs_15">
                    {{ props.data.user_infor.full_name }}
                </router-link>
                <p class="normal_text gray fs_15">{{ props.data.context }}</p>
                <p class="normal_text gray fs_11">{{ props.data.create_time }}</p>
            </div>

            <div class="display_flex justify_space align_center mg_t_5">
                <div @click="like_comment" class="display_flex align_center gap5 poiter">
                    <font-awesome-icon :icon="['fas', 'heart']" class="icon15 red" v-if="props.data.liked" />
                    <font-awesome-icon :icon="['fas', 'heart']" class="icon gray" v-else />
                    <p class="normal_text gray fs_13">{{ props.data.like_count }}</p>
                </div>

                <div @click="add_parent">
                    <font-awesome-icon :icon="['fas', 'message']" class="icon_11 gray" />
                </div>

                <div @click="get_child_comment" v-if="props.data.child_count > 0"
                    class="display_flex align_center gap5 poiter">
                    <font-awesome-icon :icon="['fas', 'caret-down']" class="icon15 gray" />
                    <p class="normal_text gray fs_13">{{ props.data.child_count }}</p>
                </div>

                <font-awesome-icon :icon="['fas', 'trash']" @click="delete_comment"
                    v-if="my_user == props.data.user_infor.username" class="icon_11 gray" />
            </div>

            <div class="comment_list_child">
                <div v-for="(child, index) in child_comment" :key="child.id" class="mg_t_5">
                    <CommentItemRecursive :data="child" />
                    <p class="normal_text normal_color fs_11 poiter" v-if="index == child_comment.length-1 && child.have_more=='True'" @click="loadMoreComment_child">Load more</p>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
.comment_item {
    display: flex;
    width: 100%;
    min-width: 200px;
    gap: 10px;
    margin-bottom: 10px;
}
</style>