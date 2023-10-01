<script setup>
import { Store } from '../assets/store'

import { ref, defineProps, watch } from 'vue'
import axios from 'axios'


const props = defineProps({
    video_id: String
})
watch(props, (oldvalue, currentvalue) => {
    api_get_comment_list(currentvalue.video_id)
})

const store = Store()
const my_user = localStorage.getItem('username')
const comment_list = ref(null)

const api_get_comment_list = (id) => {
    let header = null
    if (store.is_login) {
        header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
    }
    axios.get(`${store.domain}/api/video/${id}/comment-list`, header)
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
api_get_comment_list(props.video_id)

const like_comment = () => {
    console.log("like");
}

const comment_comment = () => {
    console.log("comment");
}

</script>

<template>
    <div class="comment_list">
        <div v-for="comment in comment_list">
            <div>
                <router-link :to="{ name: 'guest_profile', params: { username: comment.user_infor.username } }"
                    v-if="my_user != comment.user_infor.username">
                    <img class="profile_avatar_icon" :src="store.domain + comment.user_infor.avatar">
                </router-link>
                <router-link to="/profile/self" v-else>
                    <img class="profile_avatar_icon" :src="store.domain + comment.user_infor.avatar">
                </router-link>

            </div>
            <div>
                <div>
                    <router-link :to="{ name: 'guest_profile', params: { username: comment.user_infor.username } }"
                        v-if="my_user != comment.user_infor.username">
                        <p>{{ comment.user_infor.full_name }}</p>
                    </router-link>
                    <router-link to="/profile/self" v-else>
                        <p>{{ comment.user_infor.full_name }}</p>
                    </router-link>

                    <p>{{ comment.context }}</p>
                    <small>{{ comment.create_time }}</small>
                </div>
                <div>
                    <button @click="like_comment">like</button>
                    <button @click="comment_comment">comment</button>
                </div>
            </div>
        </div>
    </div>
</template>