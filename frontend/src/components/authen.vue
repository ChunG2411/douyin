<script setup>
import config from '../assets/config.js'

import { ref, reactive, inject } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const user = reactive({
    username_email: "",
    password: "",
    username: "",
    token: ""
})
const msg = reactive({
    error: ref(null),
    success: ref(null)
})

const queryTimeout = ref(null)
const user_localstore = inject("user_localstore")

const login = () => {
    msg.error = null

    clearTimeout(queryTimeout.value);
    queryTimeout.value = setTimeout(async () => {
        try {
            const data = {
                "username_email": user.username_email,
                "password": user.password
            }
            const result = await axios.post(`${config.domain}/login`, data)
            user.token = result.data.data.access
            user.username = result.data.data.username

        } catch (error) {
            msg.error = error.response.data.msg
            return
        }

        try {
            const header = {
                headers: { Authorization: `Bearer ${user.token}` }
            }
            await axios.get(`${config.domain}/online/${user.username}`, header)

        } catch (error) {
            msg.error = error
            return
        }
        localStorage.setItem('user',
            JSON.stringify({
                username: user.username,
                token: user.token
            })
        )
        location.reload()
    }, 300)
}

const logout = () => {
    clearTimeout(queryTimeout.value);
    queryTimeout.value = setTimeout(async () => {
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
    }, 300)
}

</script>

<template>
    <div class="login" v-if="!user_localstore.is_authen">
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

    <div class="profile" v-else>
        <a :href="'/profile/' + user_localstore.user['username']">my profile</a>
        <button @click="logout">logout</button>
    </div>
</template>
