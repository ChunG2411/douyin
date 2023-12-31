<script setup>
import AuthenComponent from './authen.vue'
import Notification from './notification.vue'
import { Store } from '../assets/store'
import { socket_noti, connect_noti, connect_chat, socket_chat, connect_message } from '../function/socket.js'

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
const show_setup_popup = ref(false)

//socket
connect_noti()
connect_chat()
connect_message()

socket_noti.onmessage = function (e) {
    if (store.is_login) {
        var data = JSON.parse(e.data)
        const decoded = jwt_decode(localStorage.getItem('token'))

        if (data.type == "noti" && data.data) {
            if (decoded.user_id == data.data.user) {
                store.noti = data.data
            }
        }
    }
}

socket_chat.onmessage = function (e) {
    if (store.is_login) {
        var data = JSON.parse(e.data)

        if (data.type == "chat" && data.data) {
            if (data.data.member.includes(localStorage.getItem('username')) && data.data.sender != localStorage.getItem('username')) {
                store.chat = data.data
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
            localStorage.removeItem('theme')
            localStorage.removeItem('lang')
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
    show_setup_popup.value = false
}]

const handleClickSearch = (text) => {
    search.context = text
}

const redirectSearch = () => {
    if (search.context) {
        router.push({ name: 'search', params: { text: search.context } })
    }
    else return
}

</script>

<template>
    <div class="header">
        <router-link :to="{ name: 'home', params: { username: '' } }" class="text normal_color">Anh Chung</router-link>

        <div class="search">
            <input type="text" class="input_search" id="search-bar" :placeholder="store.translate('header', 'search')"
                v-model="search.context" @input="get_search_suggest" @click="click_input" v-on-click-outside="click_outside"
                v-on:keyup.enter="redirectSearch" autocomplete="off">
            <div>
                <font-awesome-icon class="icon gray" :icon="['fas', 'x']" @click="clear_context" />
            </div>

            <div class="search_popup" v-show="show_search_popup">
                <div id="suggest" v-if="search.context">
                    <router-link :to="{ name: 'search', params: { text: suggest } }" v-for="suggest in search.suggest"
                        @click="handleClickSearch(suggest)" class="normal_text normal_color fs_14 search_popup_item">{{
                            suggest }}
                    </router-link>
                </div>
                <div id="recent" v-else>
                    <router-link :to="{ name: 'search', params: { text: recent } }" v-for="recent in search.recent"
                        @click="handleClickSearch(recent)" class="normal_text normal_color fs_14 search_popup_item">{{
                            recent }}
                    </router-link>
                </div>
            </div>
        </div>

        <div class="action">
            <div class="action" v-if="store.is_login">
                <div class="action_item" @click="show_noti_popup = true">
                    <font-awesome-icon :icon="['fas', 'bell']" class="icon normal_color" />
                    <p class="text normal_color fs_14">{{ store.translate("header", "noti") }}</p>
                </div>

                <router-link to="/chat" class="action_item no_decor">
                    <font-awesome-icon :icon="['fas', 'message']" class="icon normal_color" />
                    <p class="text normal_color fs_14">{{ store.translate("header", "chat") }}</p>
                </router-link>

                <router-link to="/creator" class="action_item no_decor">
                    <font-awesome-icon :icon="['fas', 'plus']" class="icon normal_color" />
                    <p class="text normal_color fs_14">{{ store.translate("header", "creator") }}</p>
                </router-link>

                <div class="action_item" id="action_item_hover">
                    <img class="profile_avatar_header" :src="store.domain + store.my_profile.avatar">
                </div>

                <div class="action_item_popup">
                    <router-link to="/profile/self" class="action_item_popup_options no_decor">
                        <font-awesome-icon :icon="['fas', 'user']" class="icon normal_color" />
                        <p class="text normal_color fs_14">{{ store.translate("header", "profile") }}</p>
                    </router-link>
                    <div class="action_item_popup_options" @click="show_setup_popup = true">
                        <font-awesome-icon :icon="['fas', 'gear']" class="icon normal_color" />
                        <p class="text normal_color fs_14">{{ store.translate("header", "setup") }}</p>
                    </div>
                    <div @click="logout" class="action_item_popup_options">
                        <font-awesome-icon :icon="['fas', 'arrow-right-from-bracket']" class="icon normal_color" />
                        <p class="text normal_color fs_14">{{ store.translate("header", "logout") }}</p>
                    </div>
                </div>
            </div>

            <div class="action_item" v-else>
                <p @click="show_login_popup = true" class="text normal_color fs_14">{{ store.translate("header", "login") }}</p>
            </div>
        </div>

        <div class="popup" v-if="show_login_popup || show_noti_popup || show_setup_popup || store.loading">
            <div class="popup_board" v-if="show_login_popup">
                <AuthenComponent v-on-click-outside="close_popup" />
            </div>
            <div class="popup_board" v-if="show_noti_popup">
                <Notification v-on-click-outside="close_popup" />
            </div>
            <div class="popup_board" v-if="show_setup_popup">
                <div class="setup" v-on-click-outside="close_popup">
                    <p class="text normal_color fs_17">{{ store.translate("header", "setup") }}</p>
                    <div class="setup_board">
                        <div class="setup_board_item">
                            <div class="display_flex gap10 align_center">
                                <font-awesome-icon :icon="['fas', 'language']" class="icon_20 normal_color" />
                                <p class="text normal_color">{{ store.translate("header", "language") }}</p>
                            </div>
                            <select class="select" name="language" v-model="store.lang">
                                <option value="en">{{ store.translate("header", "english") }}</option>
                                <option value="zh">{{ store.translate("header", "chinese") }}</option>
                                <option value="vi">{{ store.translate("header", "vietnamese") }}</option>
                            </select>
                        </div>
                        <div class="setup_board_item">
                            <div class="display_flex gap10 align_center">
                                <font-awesome-icon :icon="['fas', 'sun']" class="icon_20 normal_color" />
                                <p class="text normal_color">{{ store.translate("header", "theme") }}</p>
                            </div>
                            <select class="select" name="theme" v-model="store.theme">
                                <option value="dark">{{ store.translate("header", "dark") }}</option>
                                <option value="light">{{ store.translate("header", "light") }}</option>
                            </select>
                        </div>

                    </div>
                </div>
            </div>
            <div class="popup_board" v-if="store.loading">
                <p class="text normal_color fs_15">{{ store.translate("chat", "loading") }}</p>
            </div>
        </div>

    </div>
</template>

<style>
.header {
    margin-top: 0;
    margin-left: 0;
    width: 100%;
    height: 50px;
    padding: 5px 20px 5px 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: fixed;
    z-index: 50;
    background: var(--background_color);
}

.search {
    width: 200px;
    height: max-content;
    padding: 0 10px 0 10px;
    background: var(--background_color);
    border-radius: 15px;
    display: flex;
    justify-content: space-between;
    border: 1px solid var(--boder_color);
}

.input_search {
    border: 0;
    background: var(--background_color);
    color: var(--text_color);
}

.input_search:focus {
    border: 0;
    outline: none;
}

.search_popup {
    position: fixed;
    margin-top: 30px;
    margin-left: 0;
    width: 180px;
    height: max-content;
    background: var(--background_popup_color);
    border-radius: 5px;
    padding: 10px;
    justify-content: left;
    box-shadow: 0 0 2px var(--boder_color);
}

.search_popup_item {
    display: flex;
    flex-direction: column;
    margin-bottom: 3px;
    margin-left: 5px;
}

.action {
    display: flex;
    width: max-content;
    right: 0;
    margin-right: 10px;
}

.action_item {
    display: flex;
    flex-direction: column;
    width: max-content;
    margin-right: 5px;
    cursor: pointer;
    border: 1px solid var(--boder_color);
    border-radius: 5px;
    padding: 5px;
}

.action_item:hover {
    background: var(--hover_color);
}

#action_item_hover:hover+.action_item_popup,
.action_item_popup:hover {
    display: flex;
}

.action_item_popup {
    position: fixed;
    top: 50px;
    right: 5px;
    width: max-content;
    height: max-content;
    background: var(--background_popup_color);
    border-radius: 5px;
    padding: 10px;
    display: none;
    justify-content: space-between;
    box-shadow: 0 0 2px var(--boder_color);
}

.action_item_popup_options {
    display: flex;
    flex-direction: column;
    margin-right: 5px;
    cursor: pointer;
    align-items: center;
    padding: 5px;
    border-radius: 5px;
}

.action_item_popup_options:hover {
    background: var(--hover_color);
}

.setup {
    height: 100%;
}

.setup_board {
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin-left: 10px;
    padding: 10px;
}

.setup_board_item{
    width: 95%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>