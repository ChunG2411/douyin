<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'
import config from '../assets/config.js'

const search_value = ref("")
const have_context = ref(false)
const show_search_popup = ref(false)
const recent_search = ref([])
const queryTimeout = ref(null)
const search_result = ref([])
const is_login = ref(false)
const user = ref(null)
const dataUser = reactive({
    name: '',
})


user.value = localStorage.getItem('user') ?? "no user";
setInterval(() => {
    user.value += "1";
}, 1000)
watch(() => user.value, (oldValue, newValue) => {
    console.log(oldValue, newValue);
})
const demo = computed(() => { return {} })
// api
const api_get_search_recent = () => {
    clearTimeout(queryTimeout.value);
    queryTimeout.value = setTimeout(async () => {
        try {
            const result = await axios.get(`${config.domain}/search/recent`)
            recent_search.value = result.data.data
            return
        } catch {
            console.log("error while get recent search.");
        }
    }, 300);
}


const get_search_result = () => {
    have_context.value = true

    if (search_value.value == "") {
        have_context.value = false
        api_get_search_recent()
    }
}

const click_input = () => {
    if (!show_search_popup.value) {
        show_search_popup.value = true
        api_get_search_recent()
    }
}

const clear_context = () => {
    search_value.value = ""
    have_context.value = false
}


</script>

<template>
    <div class="header">
        <div class="logo">
            <router-link to="/">
                <p>Home</p>
                <!-- <img src="../assets/logo.png" id="logo-image"> -->
            </router-link>
        </div>

        <div class="search">
            <input type="text" id="search-bar" placeholder="What do you want to find?" v-model="search_value"
                @input="get_search_result" @click="click_input">
            <button @click="clear_context">clear</button>
        </div>

        <div class="search-popup" v-show="show_search_popup">
            <div id="have-context" v-if="have_context">
                <p>{{ search_result }}</p>
            </div>
            <div id="no-have-context" v-else>
                <p v-for="recent in recent_search">{{ recent }}</p>
            </div>
        </div>

        <div class="action">
        </div>

        <p v-show="user">{{ user }}</p>
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