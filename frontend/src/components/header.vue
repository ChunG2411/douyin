<script setup>
import AuthenComponent from './authen.vue'
import { Store } from '../assets/store'

import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'

import axios from 'axios'
import { vOnClickOutside } from '@vueuse/components'


const store = Store()
const router = useRouter()

const search = reactive({
    context: null,
    suggest: null,
    recent: null
})

const show_search_popup = ref(false)
const show_login_popup = ref(false)


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
}]

const redirectSearch = () => {
    router.push({ name: 'search', params: { text: search.context } })
}

const get_noti = () => {
    console.log("notification")
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
                <button @click="get_noti">Noti</button>

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

        <div class="popup" v-if="show_login_popup">
            <AuthenComponent v-on-click-outside="close_popup" />
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