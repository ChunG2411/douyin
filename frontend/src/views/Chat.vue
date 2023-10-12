<script setup>
import { Store } from '../assets/store'
import { socket_chat } from '../function/socket.js'

import { ref, reactive, watch } from 'vue'
import axios from 'axios'
import jwt_decode from "jwt-decode"


const store = Store()
const decoded = jwt_decode(localStorage.getItem('token'))
const my_user = localStorage.getItem('username')

const chat_list = ref([])
const msg_list = ref([])
const cur_chat = ref(null)
const member_list = ref([])

const search_chat = reactive({
    request: '',
    result: []
})

const show_modify_chat = ref(false)
const show_member_chat = ref(false)
const show_action_chat = ref(false)
const show_add_chat_popup = ref(false)
const show_add_member_popup = ref(false)
const show_remove_member_popup = ref(false)

const preview_image_upload = ref(null)
const preview_modify_image_upload = ref(null)

const form_msg = reactive({
    text: '',
    media: ''
})
const form_modify = reactive({
    name: '',
    avatar: ''
})

const member_chat = ref([])
const follower = ref([])
const add_member_list = ref([])


watch(store.chat_socket?.context, (currentvalue) => {
    if (cur_chat.value.id == currentvalue.receiver) {
        api_get_chat_detail(cur_chat.value.id)
    }
})


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

            //socket noti: chat
            socket_chat.send(JSON.stringify({
                "sender": localStorage.getItem('username'),
                "receiver": id,
                "context": form_msg.text,
                "media": form_msg.media
            }))

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

const api_get_follower = () => {
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

const add_new_chat = () => {
    show_add_chat_popup.value = true
    api_get_follower()
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

const show_member = (id) => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.get(`${store.domain}/api/chat/${id}/member`, header)
        .then(response => {
            member_list.value = response.data.data
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

const add_member_to_chat = () => {
    api_get_follower()
    show_add_member_popup.value = true
}

const submit_add_new_member = () => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }

    var member_list = []
    for (let i = 0; i < add_member_list.value.length; i++) {
        member_list.push(add_member_list.value[i].username)
    }

    const form = new FormData()
    form.append('member', member_list.toString())

    axios.post(`${store.domain}/api/chat/${cur_chat.value.id}/add`, form, header)
        .then(response => {
            store.msg_success = response.data.data
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

const remove_member_to_chat = (id) => {
    show_member(id)
    show_remove_member_popup.value = true
}

const submit_remove_member = (username, index) => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }

    const form = new FormData()
    form.append('member', username)

    axios.post(`${store.domain}/api/chat/${cur_chat.value.id}/remove`, form, header)
        .then(response => {
            store.msg_success = response.data.data
            member_list.value.splice(index, 1)
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

const modify_chat = (cur_chat) => {
    show_modify_chat.value = true
    form_modify.name = cur_chat.name
}

const close_modify_chat = () => {
    show_modify_chat.value = false
    form_modify.name = cur_chat.name
    form_modify.avatar = ''
    preview_modify_image_upload.value = null
}

const change_avatar_chat = (e) => {
    form_modify.avatar = e.target.files[0]
    preview_modify_image_upload.value = URL.createObjectURL(form_modify.avatar)
}

const submit_modify_form = () => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }

    const form = new FormData()
    form.append('name', form_modify.name)
    form.append('avatar', form_modify.avatar)

    axios.put(`${store.domain}/api/chat?id=${cur_chat.value.id}`, form, header)
        .then(response => {
            store.msg_success = response.data.data
            location.reload()
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
                        <div v-for="(msg, index) in msg_list">
                            <div v-if="decoded.user_id == msg.sender" style="background-color: blue;">
                                <div>
                                    <p v-if="msg.context">{{ msg.context }}</p>
                                    <img :src="store.domain + msg.media" v-if="msg.media">
                                </div>
                            </div>
                            <div v-else>
                                <div>
                                    <p v-if="msg.context">{{ msg.context }}</p>
                                    <img :src="store.domain + msg.media" v-if="msg.media">
                                </div>
                            </div>
                            <div v-if="msg.reader.length < cur_chat.member.length">
                                <small>{{ msg.reader.length }} member readed</small>
                            </div>
                            <div v-else-if="cur_chat.member.length == msg.reader.length && index == (msg_list.length - 1)">
                                <small>{{ msg.reader.length }} member readed</small>
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
                    <button @click="modify_chat(cur_chat)">Modify</button>
                    <button @click="delete_chat(cur_chat.id)">Delete</button>
                    <button @click="show_member_chat = true; show_member(cur_chat.id)">
                        Member({{ cur_chat.member.length }})
                    </button>
                    <button @click="add_member_to_chat(cur_chat.id)">Add member to chat</button>
                    <button @click="remove_member_to_chat(cur_chat.id)">Remove member to chat</button>
                </div>
            </div>
        </div>

        <div class="popup"
            v-if="show_add_chat_popup || show_member_chat || show_add_member_popup || show_remove_member_popup || show_modify_chat">
            <div v-if="show_add_chat_popup">
                <div>
                    <b>member: </b>
                    <div v-for="(member, index) in member_chat" :key="index">
                        <p>{{ member.full_name }}</p>
                        <button @click="member_chat.splice(index, 1)">remove</button>
                    </div>
                </div>
                <div>
                    <b>list follower:</b>
                    <div v-for="user in follower" @click="member_chat.push(user)">
                        <p>{{ user.full_name }}</p>
                    </div>
                </div>
                <button @click="show_add_chat_popup = false">close</button>
                <button @click="submit_new_chat">Create</button>
            </div>

            <div v-if="show_member_chat">
                <b>member:</b>
                <div>
                    <div v-for="member in member_list" :key="member.id">
                        <router-link :to="{ name: 'guest_profile', params: { username: member.username } }"
                            v-if="member.username != my_user">
                            <p>{{ member.full_name }}</p>
                        </router-link>
                        <router-link to="/profile/self" v-else>
                            <p>{{ member.full_name }} (You)</p>
                        </router-link>
                    </div>
                </div>
                <button @click="show_member_chat = false; member_list = []">close</button>
            </div>

            <div v-if="show_add_member_popup">
                <b>new member:</b>
                <div>
                    <div v-for="(member, index) in add_member_list" @click="add_member_list.splice(index, 1)">
                        <p>{{ member.full_name }}</p>
                    </div>
                </div>
                <div>
                    <b>follower:</b>
                    <div v-for="user in follower" :key="user.id" @click="add_member_list.push(user)">
                        <p>{{ user.full_name }}</p>
                    </div>
                </div>
                <button @click="show_add_member_popup = false; add_member_list = []">close</button>
                <button @click="submit_add_new_member">Create</button>
            </div>

            <div v-if="show_remove_member_popup">
                <b>member:</b>
                <div>
                    <div v-for="(member, index) in member_list" :key="index">
                        <div v-if="my_user != member.username">
                            <p>{{ member.full_name }}</p>
                            <button @click="submit_remove_member(member.username, index)">Remove</button>
                        </div>
                    </div>
                </div>
                <button @click="show_remove_member_popup = false">close</button>
            </div>

            <div v-if="show_modify_chat">
                <form @submit.prevent="submit_modify_form">
                    <div>
                        <p>name</p>
                        <input type="text" v-model="form_modify.name">
                    </div>
                    <div>
                        <p>avatar</p>
                        <img class="modify_avatar_chat" :src="store.domain + cur_chat.avatar"
                            v-if="!preview_modify_image_upload">
                        <img class="modify_avatar_chat" :src="preview_modify_image_upload" v-else>
                        <input type="file" accept="image/*" style="display: none;" id="modify_upload_avatar"
                            @change="change_avatar_chat">
                        <label for="modify_upload_avatar">change</label>
                    </div>
                    <button type="submit">Submit</button>
                </form>
                <button @click="close_modify_chat">close</button>
            </div>
        </div>
    </div>
</template>