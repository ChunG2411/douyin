import { defineStore } from 'pinia'
import lang_temp from './lang.json' assert {type: 'json'}

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

        lang: (localStorage.getItem('lang') === null) ? 'en' : localStorage.getItem('lang'),
        theme: (localStorage.getItem('theme') === null) ? 'dark' : localStorage.getItem('theme'),

        comment_tag: {
            video_id: '',
            comment_id: '',
            full_name: ''
        }
    }),
    actions: {
        translate(text1, text2) {
            return lang_temp[this.lang][text1][text2]
        },
    }
})
