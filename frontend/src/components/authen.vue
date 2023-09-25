<script setup>
import config from '../assets/config.js'

import { ref, reactive, inject } from 'vue'
import axios from 'axios'

const user = reactive({
    username_email: "",
    password: "",
    username: "",
    token: ""
})
const msg = reactive({
    error: null,
    success: null
})

let queryTimeout = null

const login = () => {
    msg.error = null

    clearTimeout(queryTimeout)
    queryTimeout = setTimeout(async () => {
        try {
            const data = {
                "username_email": user.username_email,
                "password": user.password
            }
            const result = await axios.post(`${config.domain}/login`, data)
            user.token = result.data.data.access
            user.username = result.data.data.username
            msg.success = "login success"
        } catch (error) {
            msg.error = error.response.data.msg
            return
        }

        localStorage.setItem('user',
            JSON.stringify({
                username: user.username,
                token: user.token
            })
        )
        api_user_online()
    }, 100)
}

const api_user_online = () => {
    clearTimeout(queryTimeout)
    queryTimeout = setTimeout(async () => {
        try {
            const header = {
                headers: { Authorization: `Bearer ${user.token}` }
            }
            await axios.get(`${config.domain}/online/${user.username}`, header)

        } catch (error) {
            msg.error = error
            return
        }
    }, 100)
    location.reload()
}

</script>

<template>
    <div class="login">
        <form @submit.prevent="login">
            <input type="text" placeholder="Username or email" v-model="user.username_email">
            <input type="password" placeholder="Password" v-model="user.password">
            <button @click="login">Login</button>

            <div class="login-msg">
                <small class="error-msg" v-if="msg.error">{{ msg.error }}</small>
                <small class="success-msg" v-if="msg.success">{{ msg.success }}</small>
            </div>
        </form>
    </div>
</template>

<style>
.login {
    background: white;
}
</style>