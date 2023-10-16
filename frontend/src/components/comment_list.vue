<script setup>
import { Store } from '../assets/store'
import CommentItem from './comment_item.vue'

import { ref, defineProps, watch, reactive } from 'vue'
import axios from 'axios'
import { socket_noti } from '../function/socket.js'


const props = defineProps({
    video_id: String
})
watch(props, (oldvalue, currentvalue) => {
    api_get_comment_list(currentvalue.video_id)
})

const store = Store()

const comment_list = ref([])
const comment_form = ref('')
const page_comment = ref(0)

const api_get_comment_list = () => {
    let header = null
    if (store.is_login) {
        header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
    }

    axios.get(`${store.domain}/api/video/${props.video_id}/comment-list`, header)
        .then(response => {
            comment_list.value = response.data.data
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
api_get_comment_list()

const remove_parent = () => {
    store.comment_tag.comment_id = ''
    store.comment_tag.video_id = ''
    store.comment_tag.full_name = ''
}

const comment_video = () => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    const form = new FormData()
    form.append('parent', store.comment_tag.comment_id)
    form.append('context', comment_form.value)

    axios.post(`${store.domain}/api/video/${props.video_id}/comment`, form, header)
        .then(response => {
            comment_list.value.push(response.data.data)
            comment_form.value = null

            //socket noti: comment
            if (store.comment_tag.comment_id) {
                socket_noti.send(JSON.stringify({
                    "user": localStorage.getItem('username'),
                    "video": props.video_id,
                    "comment": store.comment_tag.comment_id,
                    "type": "4"
                }))
            }
            else {
                socket_noti.send(JSON.stringify({
                    "user": localStorage.getItem('username'),
                    "video": props.video_id,
                    "type": "2"
                }))
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

const loadMoreComment = (e) => {
    const { scrollTop, offsetHeight, scrollHeight } = e.target
    if ((scrollTop + offsetHeight) >= scrollHeight) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        page_comment.value += 1
        axios.get(`${store.domain}/api/video/${props.video_id}/comment-list?page=${page_comment.value}`, header)
            .then(response => {
                if (response.data.data.length == 0) {
                    page_comment.value -= 1
                }
                else {
                    for (let i = 0; i < response.data.data.length; i++) {
                        comment_list.value.push(response.data.data[i])
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
window.addEventListener('scroll', loadMoreComment);

</script>

<template>
    <div class="comment_list">
        <div class="comment_list_item" v-on:scroll="loadMoreComment">
            <div v-for="comment in comment_list" :key="comment.id">
                <CommentItem :data="comment" />
            </div>
        </div>


        <div>
            <form @submit.prevent="comment_video" v-if="store.is_login">
                <span v-if="store.comment_tag.video_id == props.video_id">
                    <small>to @{{ store.comment_tag.full_name }}</small>
                    <label @click="remove_parent">remove</label>
                </span>
                <input type="text" v-model="comment_form">
                <button type="submit">comment</button>
            </form>
        </div>
    </div>
</template>

<style>
.comment_list_item {
    overflow-y: scroll;
    min-height: max-content;
    max-height: 300px;
}
</style>