<script setup>
import AuthenComponent from '../components/authen.vue'
import config from '../assets/config.js'

import { ref, reactive, inject } from 'vue'
import axios from 'axios'
import { vOnClickOutside } from '@vueuse/components'
import { useRouter } from 'vue-router'

const router = useRouter()
const show_search_popup = ref(false)
let queryTimeout = null

const search = reactive({
    value: ref(null),
    had_context: ref(false),
    suggest: ref(null),
    recent: ref(null)
})

const user_store = inject("user_store")


const api_get_search_recent = () => {
    clearTimeout(queryTimeout);
    queryTimeout = setTimeout(async () => {
        try {
            const header = {
                headers: { Authorization: `Bearer ${user_store.user["token"]}` }
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

        if (user_store.is_authen) {
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

    if (user_store.is_authen) {
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

const navigating_home =()=>{
    router.push('/')
}

</script>

<template>
    <div class="header">
        <div class="logo" @click="navigating_home">
            <p>Home</p>
        </div>

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
            <AuthenComponent />
        </div>

    </div>
</template>

<style>
.header {
    margin: 0;
    width: 100%;
    height: 50px;
    background: transparent;
}
</style>