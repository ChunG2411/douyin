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

</script>

<template>
    <div class="comment_item" v-if="show_this_comment">
        <div>
            <router-link :to="{ name: 'guest_profile', params: { username: props.data.user_infor.username } }"
                v-if="my_user != props.data.user_infor.username">
                <img class="profile_avatar_icon" :src="store.domain + props.data.user_infor.avatar">
            </router-link>
            <router-link to="/profile/self" v-else>
                <img class="profile_avatar_icon" :src="store.domain + props.data.user_infor.avatar">
            </router-link>
        </div>
        <div>
            <div>
                <router-link :to="{ name: 'guest_profile', params: { username: props.data.user_infor.username } }"
                    v-if="my_user != props.data.user_infor.username">
                    <p>{{ props.data.user_infor.full_name }}</p>
                </router-link>
                <router-link to="/profile/self" v-else>
                    <p>{{ props.data.user_infor.full_name }}</p>
                </router-link>

                <p>{{ props.data.context }}</p>
                <small>{{ props.data.create_time }}</small>
            </div>
            <div>
                <button @click="like_comment" v-if="props.data.liked">liked: {{ props.data.like_count }}</button>
                <button @click="like_comment" v-else>like: {{ props.data.like_count }}</button>

                <button @click="add_parent">comment</button>
                <button @click="get_child_comment" v-if="props.data.child_count > 0">
                    show more({{ props.data.child_count }})
                </button>

                <button @click="delete_comment" v-if="my_user == props.data.user_infor.username">delete</button>
            </div>
        </div>
        <div>
            <div v-for="child in child_comment" :key="child.id">
                <CommentItemRecursive :data="child" />
            </div>
        </div>
    </div>
</template>