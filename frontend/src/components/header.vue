<script setup>
import AuthenComponent from './authen.vue'
import Notification from './notification.vue'
import { Store } from '../assets/store'
import { socket_noti, connect_noti, connect_chat, socket_chat } from '../function/socket.js'

import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { vOnClickOutside } from '@vueuse/components'
import jwt_decode from "jwt-decode"


const store = Store()
const router = useRouter()

const search = reactive({
    context: null,
    suggest: null,
    recent: null
})

const show_search_popup = ref(false)
const show_login_popup = ref(false)
const show_noti_popup = ref(false)
const have_new_noti = ref(false)
const have_new_chat = ref(false)

const socket_noti_data = ref(null)

//socket
connect_noti()
connect_chat()

socket_noti.onmessage = function (e) {
    if (store.is_login) {
        var data = JSON.parse(e.data)
        const decoded = jwt_decode(localStorage.getItem('token'))

        // noti
        if (data.type == "noti" && data.data) {
            socket_noti_data.value = data.data
            if (decoded.user_id == socket_noti_data.value.user) {
                have_new_noti.value = true
            }
        }
    }
}

socket_chat.onmessage = function (e) {
    if (store.is_login) {
        var data = JSON.parse(e.data)

        // chat
        if (data.type == "chat" && data.data) {
            if (data.data.member.includes(localStorage.getItem('username')) && data.data.sender != localStorage.getItem('username')) {
                have_new_chat.value = true
                store.chat_socket = { ...data.data };

                console.log(store.chat_socket);
            }
        }
    }
}

//

const api_get_my_user = () => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.get(`${store.domain}/api/user/self`, header)
        .then(response => {
            store.my_profile.username = response.data.data.username
            store.my_profile.avatar = response.data.data.avatar
        })
        .catch(error => {
            console.log(error)
            try {
                store.msg_error.value = error.response.data.msg
            }
            catch {
                store.msg_error.value = error
            }
        })
}

const api_get_search_recent = () => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.get(`${store.domain}/api/search/recent`, header)
        .then(response => {
            search.recent = response.data.data
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

const api_get_search_suggest = () => {
    axios.get(`${store.domain}/api/search/suggest?text=${search.context}`)
        .then(response => {
            search.suggest = response.data.data
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

if (store.is_login) {
    api_get_my_user()
}

const get_search_suggest = () => {
    if (search.context) {
        api_get_search_suggest()
    }
    else {
        search.suggest = null
        search.recent = null
        if (store.is_login) {
            api_get_search_recent()
        }
    }
}

const click_input = () => {
    show_search_popup.value = true

    if (store.is_login) {
        api_get_search_recent()
    }
}

const click_outside = () => {
    show_search_popup.value = false
}

const clear_context = () => {
    search.context = null
    search.recent = null
    search.suggest = null
}

const logout = () => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.get(`${store.domain}/api/offline`, header)
        .then(response => {
            localStorage.removeItem('username')
            localStorage.removeItem('token')
            window.location.href = store.home
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

const close_popup = [() => {
    show_login_popup.value = false
    show_noti_popup.value = false
    have_new_noti.value = false
    have_new_chat.value = false
}]

const redirectSearch = () => {
    router.push({ name: 'search', params: { text: search.context } })
}

</script>

<template>
    <div class="header">
        <router-link to="/">home</router-link>

        <div class="search">
            <input type="text" id="search-bar" placeholder="What do you want to find?" v-model="search.context"
                @input="get_search_suggest" @click="click_input" v-on-click-outside="click_outside"
                v-on:keyup.enter="redirectSearch">
            <button @click="clear_context">clear</button>
        </div>

        <div class="search-popup" v-show="show_search_popup">
            <div id="suggest" v-if="search.context">
                <router-link :to="{ name: 'search', params: { text: suggest } }" v-for="suggest in search.suggest">
                    <p>{{ suggest }}</p>
                </router-link>
            </div>

            <div id="recent" v-else>
                <router-link :to="{ name: 'search', params: { text: recent } }" v-for="recent in search.recent">
                    <p>{{ recent }}</p>
                </router-link>
            </div>
        </div>

        <div class="action">
            <div class="profile" v-if="store.is_login">
                <button @click="show_noti_popup = true">Noti</button>

                <router-link to="/chat">
                    <button>Chat</button>
                </router-link>

                <router-link to="/creator">
                    <button>Creator</button>
                </router-link>

                <router-link to="/profile/self">
                    <img class="profile_avatar_icon" :src="store.domain + store.my_profile.avatar">
                </router-link>

                <button @click="logout">logout</button>
            </div>

            <div class="login" v-else>
                <button @click="show_login_popup = true">Login</button>
            </div>
        </div>

        <div class="popup" v-if="show_login_popup || show_noti_popup || have_new_noti || have_new_chat">
            <div v-if="show_login_popup">
                <AuthenComponent v-on-click-outside="close_popup" />
            </div>
            <div v-if="show_noti_popup">
                <Notification v-on-click-outside="close_popup" />
            </div>
            <div v-if="have_new_noti" v-on-click-outside="close_popup">
                <p v-if="socket_noti_data.user_interact.split(',').length - 1 > 0">
                    {{ socket_noti_data.context }} and {{ socket_noti_data.user_interact.split(",").length - 1 }}
                    other people
                </p>
                <p v-else>{{ socket_noti_data.context }}</p>

                <p v-if="socket_noti_data.type == '1'">liked your video</p>
                <p v-else-if="socket_noti_data.type == '2'">commented your video</p>
                <p v-else-if="socket_noti_data.type == '3'">liked your comment</p>
                <p v-else-if="socket_noti_data.type == '4'">commented your comment</p>
                <p v-else-if="socket_noti_data.type == '5'">followed you</p>
            </div>
            <div v-if="have_new_chat" v-on-click-outside="close_popup">
                <p>new message</p>
            </div>
        </div>

    </div>
</template>

<style>
.header {
    margin-top: 0;
    margin-left: 0;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: fixed;
    z-index: 50;
}
</style>