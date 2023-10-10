<script setup>
import { Store } from '../assets/store'
import { socket_noti, connect_noti } from '../function/socket.js'

import { ref, reactive } from 'vue'
import axios from 'axios'
import jwt_decode from "jwt-decode"


const store = Store()
const decoded = jwt_decode(localStorage.getItem('token'))

const chat_list = ref([])
const msg_list = ref([])
const cur_chat = ref(null)

const search_chat = reactive({
    request: '',
    result: []
})

const show_action_chat = ref(false)
const show_add_chat_popup = ref(false)
const preview_image_upload = ref(null)

const form_msg = reactive({
    text: '',
    media: ''
})
const member_chat = ref([])
const follower = ref([])



const api_get_chat = () => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.get(`${store.domain}/api/chat`, header)
        .then(response => {
            chat_list.value = response.data.data
        })
        .catch(error => {
            console.log(error)
            try {
                store.msg_error.value = error.response.data.msg
            }
            catch {
                store.msg_error.value = error
            }
        })
}
api_get_chat()

const api_get_chat_detail = (id) => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.get(`${store.domain}/api/chat/${id}/detail`, header)
        .then(response => {
            msg_list.value = response.data.data
        })
        .catch(error => {
            try {
                store.msg_error.value = error.response.data.msg
            }
            catch {
                store.msg_error.value = error
            }
        })
}

const get_chat_detail = (obj) => {
    api_get_chat_detail(obj.id)
    cur_chat.value = obj
}

const upload_image = (e) => {
    form_msg.media = e.target.files[0]
    preview_image_upload.value = URL.createObjectURL(form_msg.media)
}

const submit_form = (id) => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    const form = new FormData()
    form.append('context', form_msg.text)
    form.append('media', form_msg.media)

    axios.post(`${store.domain}/api/chat/${id}/detail`, form, header)
        .then(response => {
            msg_list.value.push(response.data.data)
            form_msg.text = ''
        })
        .catch(error => {
            try {
                store.msg_error.value = error.response.data.msg
            }
            catch {
                store.msg_error.value = error
            }
        })
}

const remove_form_media = () => {
    form_msg.media = ''
    preview_image_upload.value = null
}

const get_search_chat = () => {
    if (search_chat.request != '') {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        axios.get(`${store.domain}/api/search/chat?text=${search_chat.request}`, header)
            .then(response => {
                search_chat.result = response.data.data
            })
            .catch(error => {
                try {
                    store.msg_error.value = error.response.data.msg
                }
                catch {
                    store.msg_error.value = error
                }
            })
    }
    else {
        search_chat.result = []
    }

}

const add_new_chat = () => {
    show_add_chat_popup.value = true

    axios.get(`${store.domain}/api/user/${localStorage.getItem('username')}/follower-list`)
        .then(response => {
            follower.value = response.data.data
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

const submit_new_chat = () => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }

    var member_list = []
    for (let i = 0; i < member_chat.value.length; i++) {
        member_list.push(member_chat.value[i].username)
    }
    const form = new FormData()
    form.append('member', member_list.toString())

    axios.post(`${store.domain}/api/chat`, form, header)
        .then(response => {
            chat_list.value.push(response.data.data)
            member_chat.value = []
            show_add_chat_popup = false
        })
        .catch(error => {
            try {
                store.msg_error.value = error.response.data.msg
            }
            catch {
                store.msg_error.value = error
            }
        })
}

const delete_chat = (id) => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.delete(`${store.domain}/api/chat?id=${id}`, header)
        .then(response => {
            for (let i = 0; i < chat_list.value.length; i++) {
                if (chat_list.value[i].id == id) {
                    chat_list.value.splice(i, 1)
                }
            }
            cur_chat.value = null
        })
        .catch(error => {
            try {
                store.msg_error.value = "You don't have permission."
            }
            catch {
                store.msg_error.value = error
            }
        })
}

</script>

<template>
    <div class="chat">
        <div>
            <div>
                <button @click="add_new_chat">Add new chat</button>
                <input type="text" placeholder="Search chat" v-model="search_chat.request" @input="get_search_chat">
                <div>
                    <div v-for="result in search_chat.result" @click="get_chat_detail(result)">
                        <div>
                            <img class="avatar_chat" :src="store.domain + result.avatar">
                        </div>
                        <div>
                            <p>{{ result.name }}</p>
                        </div>
                    </div>
                </div>
            </div>
            <div v-for="chat in chat_list" :key="chat.id" @click="get_chat_detail(chat)">
                <div>
                    <img class="avatar_chat" :src="store.domain + chat.avatar">
                </div>
                <div>
                    <p>{{ chat.name }}</p>
                    <small>{{ chat.last_message }}</small>
                </div>
            </div>
        </div>
        <div>
            <div v-if="cur_chat">
                <div>
                    <div>
                        <img class="avatar_chat" :src="store.domain + cur_chat.avatar">
                        <p>{{ cur_chat.name }}</p>
                    </div>
                    <div>
                        <button @click="show_action_chat = !show_action_chat">Detail</button>
                    </div>
                </div>
                <div>
                    <div>
                        <div v-for="msg in msg_list">
                            <div v-if="decoded.user_id == msg.sender" style="background-color: blue;">
                                <p v-if="msg.context">{{ msg.context }}</p>
                                <img :src="store.domain + msg.media" v-if="msg.media">
                            </div>
                            <div v-else>
                                <p v-if="msg.context">{{ msg.context }}</p>
                                <img :src="store.domain + msg.media" v-if="msg.media">
                            </div>
                        </div>
                    </div>
                    <div>
                        <form @submit.prevent="submit_form(cur_chat.id)">
                            <input type="text" v-model="form_msg.text">
                            <input type="file" accept="image/*" @change="upload_image" id="upload_image"
                                style="display: none;">
                            <label for="upload_image">upload</label>

                            <div v-if="preview_image_upload">
                                <img :src="preview_image_upload">
                                <label @click="remove_form_media">Remove</label>
                            </div>

                            <button type="submit">Send</button>
                        </form>
                    </div>
                </div>
            </div>
            <div v-if="show_action_chat && cur_chat">
                <div>
                    <img class="avatar_chat" :src="store.domain + cur_chat.avatar">
                    <p>{{ cur_chat.name }}</p>
                </div>
                <div>
                    <button @click="delete_chat(cur_chat.id)">Delete</button>
                </div>
            </div>
        </div>

        <div class="popup" v-if="show_add_chat_popup">
            <div v-if="show_add_chat_popup">
                <div>
                    <p>member: </p>
                    <div v-for="(member, index) in member_chat" :key="index">
                        <p>{{ member.full_name }}</p>
                        <button @click="member_chat.splice(index, 1)">remove</button>
                    </div>
                </div>
                <div>
                    <p>List follower:</p>
                    <div v-for="user in follower" @click="member_chat.push(user)">
                        <p>{{ user.full_name }}</p>
                    </div>
                </div>
                <button @click="show_add_chat_popup = false">close</button>
                <button @click="submit_new_chat">Create</button>
            </div>
        </div>
    </div>
</template>