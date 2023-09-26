<script setup>
import AuthenComponent from './authen.vue'
import config from '../assets/config.js'

import { ref, reactive, inject } from 'vue'
import axios from 'axios'
import { vOnClickOutside } from '@vueuse/components'

const show_search_popup = ref(false)
const show_login_popup = ref(false)
let queryTimeout = null

const search = reactive({
    value: ref(null),
    had_context: ref(false),
    suggest: ref(null),
    recent: ref(null)
})

const user_localstore = inject("user_localstore")


const api_get_search_recent = () => {
    clearTimeout(queryTimeout);
    queryTimeout = setTimeout(async () => {
        try {
            const header = {
                headers: { Authorization: `Bearer ${user_localstore.user["token"]}` }
            }
            const result = await axios.get(`${config.domain}/search/recent`, header)
            search.recent = result.data.data
            return
        } catch {
            console.log("error while get recent search.");
        }
    }, 100);
}

const api_get_search_suggest = () => {
    clearTimeout(queryTimeout);
    queryTimeout = setTimeout(async () => {
        try {
            const result = await axios.get(`${config.domain}/search/suggest?text=${search.value}`)
            search.suggest = result.data.data
            return
        } catch {
            console.log("error while get recent search.");
        }
    }, 100);
}


const get_search_suggest = () => {
    if (search.value == "" || search.value == null) {
        search.had_context = false
        search.suggest = null
        search.recent = null

        if (user_localstore.is_authen) {
            api_get_search_recent()
        }
    }
    else {
        search.had_context = true
        api_get_search_suggest()
    }
}

const click_input = () => {
    show_search_popup.value = true

    if (user_localstore.is_authen) {
        api_get_search_recent()
    }
}

const click_outside = () => {
    show_search_popup.value = false
}

const clear_context = () => {
    search.value = null
    search.had_context = false
    search.recent = null
    search.suggest = null
}

const logout = () => {
    clearTimeout(queryTimeout);
    queryTimeout = setTimeout(async () => {
        try {
            const header = {
                headers: { Authorization: `Bearer ${user_localstore.user["token"]}` }
            }
            await axios.get(`${config.domain}/offline/${user_localstore.user["username"]}`, header)
            localStorage.removeItem('user')

        } catch (error) {
            msg.error = error
        }
        location.reload()
    }, 100)
}

const close_popup = [() => {
    show_login_popup.value = !show_login_popup.value
}]

</script>

<template>
    <div class="header">
        <router-link to="/">home</router-link>

        <div class="search">
            <input type="text" id="search-bar" placeholder="What do you want to find?" v-model="search.value"
                @input="get_search_suggest" @click="click_input" v-on-click-outside="click_outside">
            <button @click="clear_context">clear</button>
        </div>

        <div class="search-popup" v-show="show_search_popup">
            <div id="suggest" v-if="search.had_context">
                <p v-for="suggest in search.suggest">{{ suggest }}</p>
            </div>
            <div id="recent" v-else>
                <p v-for="recent in search.recent">{{ recent }}</p>
            </div>
        </div>

        <div class="action">
            <div class="profile" v-if="user_localstore.is_authen">
                <router-link :to="{ name: 'profile', params: { username: user_localstore.user['username'] } }">
                    profile
                </router-link>
                <button @click="logout">logout</button>
            </div>
            <div class="login" v-else>
                <button @click="show_login_popup = !show_login_popup">login</button>
            </div>
        </div>

        <div class="popup" v-if="show_login_popup">
            <AuthenComponent v-on-click-outside="close_popup" />
        </div>

    </div>
</template>

<style>
.header {
    margin: 0;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.popup {
    background: rgba(226, 226, 226, 0.7);
    position: absolute;
    width: 100%;
    height: 100%;
    display: grid;
    place-items: center;
    z-index: 100;
    top: 0;
    left: 0;
}
</style>