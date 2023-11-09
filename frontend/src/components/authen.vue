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
            api_get_setup()
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

const api_get_setup = () => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.get(`${store.domain}/api/setup`, header)
        .then(response => {
            localStorage.setItem('lang', response.data.data.lang)
            localStorage.setItem('theme', response.data.data.theme)
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
            store.msg_success = store.translate("msg","create")
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
            <p class="text normal_color fs_17">{{ store.translate("authen", "logup") }}</p>
            <form class="authen_form mg_t_5" @submit.prevent="logup">
                <input class="input mg_b_5" type="text" :placeholder="store.translate('authen', 'email')" v-model="user_register.email">
                <input class="input mg_b_5" type="text" :placeholder="store.translate('authen', 'first_name')" v-model="user_register.first_name">
                <input class="input mg_b_5" type="text" :placeholder="store.translate('authen', 'last_name')" v-model="user_register.last_name">
                <select class="select mg_b_5" name="gender" v-model="user_register.gender">
                    <option value="" disabled selected>{{ store.translate("authen", "gender") }}</option>
                    <option value="Male">{{ store.translate("authen", "male") }}</option>
                    <option value="Female">{{ store.translate("authen", "female") }}</option>
                    <option value="Other">{{ store.translate("authen", "other") }}</option>
                </select>
                <input class="input mg_b_5" type="password" :placeholder="store.translate('authen', 'pass')" v-model="user_register.password">

                <div class="msg">
                    <p class="success_msg" v-if="store.msg_success">{{ store.msg_success }}</p>
                    <p class="error_msg" v-if="store.msg_error">{{ store.msg_error }}</p>
                </div>

                <div class="display_flex_column align_center gap5 mg_t_10">
                    <button type="submit" class="fs_15">{{ store.translate("authen", "logup") }}</button>
                    <label class="button fs_15" @click="show_logup = false">{{ store.translate("authen", "haved") }}</label>
                </div>
            </form>
        </div>

        <div class="authen_item" v-else>
            <p class="text normal_color fs_17">{{ store.translate("authen", "login") }}</p>
            <form class="authen_form mg_t_5" @submit.prevent="login">
                <input class="input mg_b_5" type="text" :placeholder="store.translate('authen', 'username_email')" v-model="user_login.username_email">
                <input class="input mg_b_5" type="password" :placeholder="store.translate('authen', 'pass')" v-model="user_login.password">

                <div class="msg">
                    <p class="error_msg" v-if="store.msg_error">{{ store.msg_error }}</p>
                </div>

                <div class="display_flex_column align_center gap5 mg_t_10">
                    <button type="submit" class="fs_15">{{ store.translate("authen", "login") }}</button>
                    <label @click="show_logup = true" class="button fs_15">{{ store.translate("authen", "create") }}</label>
                </div>
            </form>
        </div>
    </div>
</template>

<style>
.authen {
    height: max-content;
}

.authen_item {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.authen_form {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 5px;
}
</style>