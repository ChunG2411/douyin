import { defineStore } from 'pinia'
import { ref } from "vue"
import axios from 'axios'


export const Store = defineStore('store', {
    state: () => ({
        domain: "http://127.0.0.1:8000",
        home: "http://127.0.0.1:5000",
        my_profile: {
            username: localStorage.getItem('username'),
            avatar: null
        },
        is_login: ref((localStorage.getItem('token') === null) ? false : true),
        msg_error: ref(null),
        msg_success: ref(null)
    })
})
