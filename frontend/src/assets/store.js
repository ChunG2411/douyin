import { defineStore } from 'pinia'
import { ref } from "vue"


export const Store = defineStore('store', {
    state: () => ({
        domain: "http://127.0.0.1:8000",
        home: "http://127.0.0.1:5000",
        my_profile: {
            username: localStorage.getItem('username'),
            avatar: null
        },
        is_login: (localStorage.getItem('token') === null) ? false : true,

        msg_error: null,
        msg_success: null,
        noti: null,
        chat: null,

        loading: false,

        comment_tag: {
            video_id: '',
            comment_id: '',
            full_name: ''
        }
    })
})
