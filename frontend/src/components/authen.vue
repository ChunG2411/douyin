<script setup>
import { ref } from 'vue'
import axios from 'axios'
import config from '../assets/config.js'
import { useRouter } from 'vue-router'

const username_email = ref("")
const password = ref("")
const token = ref("")
const error_msg = ref("")
const queryTimeout = ref(null)
const router = useRouter()


const login = () => {
    error_msg.value = ""

    clearTimeout(queryTimeout.value);
    queryTimeout.value = setTimeout(async () => {
        try {
            const data = {
                    "username_email": username_email.value,
                    "password": password.value
                }
            const result = await axios.post(`${config.domain}/login`, data)
            token.value = result.data.data
            localStorage.setItem('user', JSON.stringify(token.value))
        } catch (error) {
            error_msg.value = error.response.data.msg
            return
        }

        try {
            const header = {
                    headers: { Authorization: `Bearer ${token.value.access}` }
                }
            await axios.get(`${config.domain}/online/${token.value.username}`, header)
        } catch (error) {
            error_msg.value = error
        }

        location.reload()
    }, 300)

    // router.push({
    //     name: 'home'
    // })
    
}

const logout = () => {
    clearTimeout(queryTimeout.value);
    queryTimeout.value = setTimeout(async () => {
        try {
            const header = {
                    headers: { Authorization: `Bearer ${token.value.access}` }
                }
            await axios.get(`${config.domain}/offline/${token.value.username}`, header)
        } catch (error) {
            error_msg.value = error
        }
    }, 300)

    localStorage.removeItem('user')
}

</script>

<template>
    <div class="login">
        <form @submit.prevent="login">
            <input type="text" placeholder="Username or email" v-model="username_email">
            <input type="password" placeholder="Password" v-model="password">
            <button @click="login">Login</button>
            <small class="error-msg">{{ error_msg }}</small>
        </form>
    </div>

    <div class="logout">
        <button @click="logout">logout</button>
    </div>
</template>
