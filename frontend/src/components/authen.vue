<script setup>
import { Store } from '../assets/store.js'

import { ref, reactive } from 'vue'
import axios from 'axios'

const store = Store()

const user_login = reactive({
    username_email: "",
    password: "",
})
const user_register = reactive({
    email: "",
    first_name: "",
    last_name: "",
    gender: "",
    password: ""
})

const show_logup = ref(false)

const login = () => {
    const data = {
        "username_email": user_login.username_email,
        "password": user_login.password
    }
    axios.post(`${store.domain}/api/login`, data)
        .then(response => {
            localStorage.setItem('token', response.data.data.access)
            localStorage.setItem('username', response.data.data.username)
            api_user_online()
        })
        .catch(error => {
            try {
                store.msg_error = error.response.data.msg
            }
            catch {
                store.msg_errorr = error
            }
        })
}

const api_user_online = () => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.get(`${store.domain}/api/online`, header)
        .then(response => {
            location.reload()
        })
        .catch(error => {
            localStorage.removeItem('token')
            try {
                store.msg_error = error.response.data.msg
            }
            catch {
                store.msg_error = error
            }

        })
}

const logup = () => {
    axios.post(`${store.domain}/api/user/register`, user_register)
        .then(response => {
            store.msg_success = "Create successful."
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

</script>

<template>
    <div class="authen">
        <div class="authen_item" v-if="show_logup">
            <form class="authen_form" @submit.prevent="logup">
                <input type="text" placeholder="Email" v-model="user_register.email">
                <input type="text" placeholder="First name" v-model="user_register.first_name">
                <input type="text" placeholder="Last name" v-model="user_register.last_name">
                <select name="gender" v-model="user_register.gender">
                    <option value="" disabled selected>Gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                </select>
                <input type="password" placeholder="Password" v-model="user_register.password">
                <button type="submit">Logup</button>

                <div class="msg">
                    <p class="success_msg" v-if="store.msg_success">{{ store.msg_success }}</p>
                    <p class="error_msg" v-if="store.msg_error">{{ store.msg_error }}</p>
                </div>
            </form>

            <div class="action">
                <button @click="show_logup = false">I have account</button>
            </div>
        </div>

        <div class="authen_item" v-else>
            <form class="authen_form" @submit.prevent="login">
                <input type="text" placeholder="Username or email" v-model="user_login.username_email">
                <input type="password" placeholder="Password" v-model="user_login.password">
                <button type="submit">Login</button>

                <div class="msg">
                    <p class="error_msg" v-if="store.msg_error">{{ store.msg_error }}</p>
                </div>
            </form>

            <div class="action">
                <button @click="show_logup = true">Create new account</button>
            </div>
        </div>
    </div>
</template>

<style>
.authen {
    height: max-content;
    background: transparent;
}
.authen_item{
    display: flex;
    flex-direction: column;
    align-items: center;
}

.authen_form{
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 5px;
}
.authen_form input{
    border: 1px solid var(--boder_color);
    border-radius: 10px;
    height: 20px;
    width: 200px;
    padding: 5px 10px;
    background: var(--background_color);
    color: var(--text_color);
    margin-bottom: 5px;
}
.authen_form select{
    background: var(--background_color);
    height: 30px;
    width: 100px;
    margin-bottom: 5px;
    color: var(--text_color);
    border: 1px solid var(--boder_color);
    border-radius: 10px;
    padding: 5px 10px;
}
</style>