<script setup>
import { Store } from '../assets/store'
import { socket_message, socket_chat } from '../function/socket.js'

import { ref, reactive, watch } from 'vue'
import axios from 'axios'
import jwt_decode from "jwt-decode"


const store = Store()
const decoded = jwt_decode(localStorage.getItem('token'))
const my_user = localStorage.getItem('username')

const chat_list = ref([])
const msg_list = ref([])
const msg_page = ref('0')
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


// scroll
const board_list_msg = ref(null)

const scrollToEnd = () => {
    setTimeout(() => {
        board_list_msg.value.scrollTop = board_list_msg.value.scrollHeight;
    }, 100)
}

// socket message
const new_message = ref(null)

socket_message.onmessage = function (e) {
    if (store.is_login) {
        var data = JSON.parse(e.data)

        if (data.type == "message" && data.data) {
            if (cur_chat.value && cur_chat.value.id == data.data.receiver) {
                if (data.data.sender != decoded.user_id) {
                    new_message.value = data.data
                    msg_list.value.push(new_message.value)
                    scrollToEnd()
                }
            }
            else {
                for (let i = 0; i < chat_list.value.length; i++) {
                    if (chat_list.value[i].id == data.data.receiver) {
                        chat_list.value[i].last_message = "new message"
                    }
                }
            }
        }
    }
}
//

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
                store.msg_error = error.response.data.msg
            }
            catch {
                store.msg_error = error
            }
        })
}
api_get_chat()

const api_get_chat_detail = (id) => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.get(`${store.domain}/api/chat/${id}/detail?page=${msg_page.value}`, header)
        .then(response => {
            for (let i = 0; i < response.data.data.length; i++) {
                msg_list.value.unshift(response.data.data[i])
                scrollToEnd()
            }
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

const get_chat_detail = (obj) => {
    msg_page.value = '0'
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

            //socket: message
            socket_message.send(JSON.stringify({
                "sender": localStorage.getItem('username'),
                "receiver": id,
                "context": form_msg.text,
                "media": form_msg.media
            }))
            // socket: chat
            socket_chat.send(JSON.stringify({
                "sender": localStorage.getItem('username'),
                "receiver": id
            }))

            form_msg.text = ''
            form_msg.media = ''
            preview_image_upload.value = null
            scrollToEnd()
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

const load_more_msg = (id) => {
    msg_page.value = String(parseInt(msg_page.value) + 1)
    api_get_chat_detail(id)
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
                    store.msg_error = error.response.data.msg
                }
                catch {
                    store.msg_error = error
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
            show_add_chat_popup.value = false
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
                store.msg_error = "You don't have permission."
            }
            catch {
                store.msg_error = error
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
                store.msg_error = error.response.data.msg
            }
            catch {
                store.msg_error = error
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
                store.msg_error = error.response.data.msg
            }
            catch {
                store.msg_error = error
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
                store.msg_error = error.response.data.msg
            }
            catch {
                store.msg_error = error
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

const handle_action_chat = () => {
    const content_element = document.querySelector('.chat_right_content')
    if (show_action_chat.value) {
        show_action_chat.value = false
        content_element.style.width = '100%'
    }
    else {
        show_action_chat.value = true
        content_element.style.width = '70%'
    }
}

</script>

<template>
    <div class="chat">
        <div class="chat_left">
            <div class="display_flex gap5 align_center">
                <button @click="add_new_chat">New</button>
                <input class="input" type="text" placeholder="Enter chat name..." v-model="search_chat.request"
                    @input="get_search_chat">
                <div class="chat_search_board" v-if="search_chat.result.length > 0">
                    <div class="chat_search_board_item" v-for="result in search_chat.result"
                        @click="get_chat_detail(result)">
                        <img class="chat_avatar" :src="store.domain + result.avatar">
                        <p class="text normal_color fs_15">{{ result.name }}</p>
                    </div>
                </div>
            </div>
            <div class="chat_left_list">
                <div class="chat_left_list_item" v-for="chat in chat_list" :key="chat.id"
                    @click="msg_list = []; get_chat_detail(chat)">
                    <div>
                        <img class="chat_avatar" :src="store.domain + chat.avatar">
                    </div>
                    <div>
                        <p class="text normal_color fs_15">{{ chat.name }}</p>
                        <p class="normal_text gray fs_13">{{ chat.last_message }}</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="chat_right" v-if="cur_chat">
            <div class="chat_right_content">
                <div class="chat_right_content_top">
                    <div class="display_flex align_center gap10">
                        <img class="chat_avatar" :src="store.domain + cur_chat.avatar">
                        <p class="text normal_color fs_15">{{ cur_chat.name }}</p>
                    </div>
                    <div>
                        <button @click="handle_action_chat">Detail</button>
                    </div>
                </div>
                <div class="chat_right_content_bottom">
                    <div class="chat_right_content_bottom_content" ref="board_list_msg">
                        <div class="display_flex justify_center">
                            <p class="normal_text normal_color fs_11 poiter" @click="load_more_msg(cur_chat.id)">
                                Read more
                            </p>
                        </div>
                        <div v-for="(msg, index) in msg_list">
                            <div class="msg_right" v-if="decoded.user_id == msg.sender">
                                <div class="msg_item">
                                    <p class="normal_text normal_color fs_13" v-if="msg.context">{{ msg.context }}</p>
                                    <div>
                                        <img class="message_image" :src="store.domain + msg.media" v-if="msg.media">
                                    </div>
                                </div>
                            </div>
                            <div class="msg_left" v-else>
                                <div class="msg_item">
                                    <p class="normal_text normal_color fs_13" v-if="msg.context">{{ msg.context }}</p>
                                    <div>
                                        <img class="message_image" :src="store.domain + msg.media" v-if="msg.media">
                                    </div>
                                </div>
                            </div>

                            <div v-if="msg.reader.length < cur_chat.member.length">
                                <p class="normal_text normal_color fs_11">{{ msg.reader.length }} member readed</p>
                            </div>
                            <div v-else-if="cur_chat.member.length == msg.reader.length && index == (msg_list.length - 1)">
                                <p class="normal_text normal_color fs_11">{{ msg.reader.length }} member readed</p>
                            </div>
                        </div>
                    </div>
                    <form class="chat_right_content_bottom_form" @submit.prevent="submit_form(cur_chat.id)">
                        <input type="file" accept="image/*" @change="upload_image" id="upload_image" style="display: none;">
                        <label for="upload_image">
                            <font-awesome-icon :icon="['fas', 'image']" class="icon_20 white" />
                        </label>
                        <input type="text" class="input" placeholder="Enter message..." v-model="form_msg.text">

                        <div class="chat_preveiw" v-if="preview_image_upload">
                            <img class="chat_preveiw_image" :src="preview_image_upload">
                            <div class="display_flex_column gap5">
                                <label class="button fs_13" @click="remove_form_media">Remove</label>
                                <label class="button fs_13" for="upload_image">Change</label>
                            </div>
                        </div>
                        <button type="submit">Send</button>
                    </form>
                </div>
            </div>
            <div class="chat_right_action" v-if="show_action_chat">
                <div class="display_flex_column align_center gap10">
                    <img class="chat_avatar" :src="store.domain + cur_chat.avatar">
                    <p class="text normal_color fs_15">{{ cur_chat.name }}</p>
                </div>
                <div class="chat_right_action_item">
                    <div class="display_flex gap10 align_center" v-if="cur_chat.type != 'single'">
                        <font-awesome-icon :icon="['fas', 'pen-to-square']" class="icon_15 white" />
                        <p class="normal_text normal_color fs_15" @click="modify_chat(cur_chat)">Modify</p>
                    </div>
                    <div class="display_flex gap10 align_center">
                        <font-awesome-icon :icon="['fas', 'trash']" class="icon white" />
                        <p class="normal_text normal_color fs_15" @click="delete_chat(cur_chat.id)">Delete</p>

                    </div>
                    <div class="display_flex gap10 align_center">
                        <font-awesome-icon :icon="['fas', 'user-group']" class="icon white" />
                        <p class="normal_text normal_color fs_15"
                            @click="show_member_chat = true; show_member(cur_chat.id)">
                            Member</p>
                    </div>
                    <div class="display_flex gap10 align_center" v-if="cur_chat.type != 'single'">
                        <font-awesome-icon :icon="['fas', 'user-plus']" class="icon white" />
                        <p class="normal_text normal_color fs_15" @click="add_member_to_chat(cur_chat.id)">Add member
                        </p>

                    </div>
                    <div class="display_flex gap10 align_center" v-if="cur_chat.type != 'single'">
                        <font-awesome-icon :icon="['fas', 'user-minus']" class="icon white" />
                        <p class="normal_text normal_color fs_15" @click="remove_member_to_chat(cur_chat.id)">Remove
                            member
                        </p>

                    </div>
                </div>
            </div>
        </div>

        <div class="popup"
            v-if="show_add_chat_popup || show_member_chat || show_add_member_popup || show_remove_member_popup || show_modify_chat">
            <div class="popup_board" v-if="show_add_chat_popup">
                <p class="text normal_color fs_17">Create new chat</p>
                <div class="pd_t_10 pd_l_10 pd_r_10">
                    <p class="text normal_color fs_15 pd_b_5">Select member: </p>
                    <div class="chat_popup_user_board">
                        <div class="chat_popup_user_board_user" v-for="(member, index) in member_chat" :key="index">
                            <div class="display_flex gap15 align_center">
                                <img class="chat_avatar" :src="store.domain + member.avatar">
                                <p class="text normal_color fs_15">{{ member.full_name }}</p>
                            </div>
                            <button @click="member_chat.splice(index, 1)">Remove</button>
                        </div>
                    </div>

                    <p class="text normal)color fs_15 pd_b_5 pd_t_5">List follower:</p>
                    <div class="chat_popup_user_board">
                        <div class="chat_popup_user_board_user" v-for="user in follower">
                            <div class="display_flex gap15 align_center">
                                <img class="chat_avatar" :src="store.domain + user.avatar">
                            <p class="text normal_color fs_15">{{ user.full_name }}</p>
                            </div>
                            <button @click="member_chat.push(user)">Add</button>
                        </div>
                    </div>
                    <div class="display_flex align_center gap10 justify_center">
                        <button @click="show_add_chat_popup = false">close</button>
                        <button @click="submit_new_chat">Create</button>
                    </div>
                </div>
            </div>

            <div class="popup_board" v-if="show_member_chat">
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

            <div class="popup_board" v-if="show_add_member_popup">
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

            <div class="popup_board" v-if="show_remove_member_popup">
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

            <div class="popup_board" v-if="show_modify_chat">
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

<style>
.chat {
    width: 90%;
    height: 90%;
    display: flex;
    gap: 15px;
    padding: 10px;
}

/* ---------------------------------left-------------------------------------- */
.chat_left {
    width: 30%;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 10px;
    position: relative;
}

/* --------------------top------------------------- */
.chat_search_board {
    position: absolute;
    background: var(--background_popup_color);
    box-shadow: 0 0 2px var(--boder_color);
    top: 30px;
    left: 70px;
    border-radius: 5px;
    padding: 5px;
    width: max-content;
    max-height: 400px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 5px;
    z-index: 20;
}

.chat_search_board::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}

.chat_search_board::-webkit-scrollbar-track {
    background: transparent !important;
}

.chat_search_board::-webkit-scrollbar-thumb {
    background: var(--scroll_color);
    border-radius: 5px;
}

.chat_search_board_item {
    padding: 5px 10px;
    border-radius: 5px;
    display: flex;
    gap: 10px;
    align-items: center;
}

.chat_search_board_item:hover {
    background: var(--hover_color);
    cursor: pointer;
}

/* --------------------bot--------------------- */
.chat_left_list {
    display: flex;
    flex-direction: column;
    gap: 5px;
    overflow-y: auto;
    width: 97%;
    height: 93%;
}

.chat_left_list::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}

.chat_left_list::-webkit-scrollbar-track {
    background: transparent !important;
}

.chat_left_list::-webkit-scrollbar-thumb {
    background: var(--scroll_color);
    border-radius: 5px;
}

.chat_left_list_item {
    display: flex;
    gap: 10px;
    padding: 10px;
    border-radius: 5px;
    align-items: center;
    cursor: pointer;
}

.chat_left_list_item:hover {
    background: var(--hover_color);
}


/* ---------------------------------right----------------------------------- */
.chat_right {
    width: 70%;
    height: 100%;
    display: flex;
    gap: 10px;
    position: relative;
}

/* ---------------------action----------------------- */
.chat_right_action {
    width: 30%;
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-items: center;
}

.chat_right_action_item {
    display: flex;
    flex-direction: column;
    gap: 5px;
    align-items: left;
    width: 100%;
}

.chat_right_action_item div {
    padding: 5px 10px;
    cursor: pointer;
    border-radius: 5px;
    display: flex;
    align-items: center;
}

.chat_right_action_item div:hover {
    background: var(--hover_color);
}

/* --------------------content---------------------- */
.chat_right_content {
    display: flex;
    flex-direction: column;
    gap: 5px;
    width: 100%;
}

.chat_right_content_top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 5px;
    border-bottom: 1px solid var(--boder_color);
}

/* ----------------------bottom------------------------ */
.chat_right_content_bottom {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 10px;
    overflow: hidden;
}

/* ------------content------------ */
.chat_right_content_bottom_content {
    width: 100%;
    height: 95%;
    overflow-y: auto;
    gap: 5px;
    display: flex;
    flex-direction: column;
}

.chat_right_content_bottom_content::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}

.chat_right_content_bottom_content::-webkit-scrollbar-track {
    background: transparent !important;
}

.chat_right_content_bottom_content::-webkit-scrollbar-thumb {
    background: var(--scroll_color);
    border-radius: 5px;
}

.msg_left {
    width: 95%;
    display: flex;
    justify-content: left;
}

.msg_left .msg_item {
    background: var(--background_popup_color);
    padding: 5px 10px;
    max-width: 55%;
    width: max-content;
    border-radius: 10px;
    box-shadow: 0 0 1px var(--boder_color);
    align-items: left;
}

.msg_left .msg_item div {
    overflow: hidden;
}

.msg_right {
    width: 98%;
    display: flex;
    justify-content: right;
}

.msg_right .msg_item {
    background: var(--background_popup_color);
    border-radius: 10px;
    box-shadow: 0 0 1px var(--boder_color);
    max-width: 55%;
    width: max-content;
    padding: 5px 10px;
}

.msg_right .msg_item div {
    overflow: hidden;
}

/* --------------form------------ */
.chat_right_content_bottom_form {
    position: absolute;
    bottom: 0;
    left: 0;
    padding: 10px 0;
    width: 100%;
    border-top: 1px solid var(--boder_color);
    display: flex;
    gap: 10px;
    align-items: center;
    position: relative;
}

.chat_preveiw {
    position: absolute;
    bottom: 50px;
    background: var(--background_popup_color);
    padding: 10px;
    border-radius: 10px;
    box-shadow: 0 0 2px var(--boder_color);
    display: flex;
    gap: 10px;
    align-items: center;
}

/* -----------------------------------------------------popup----------------------------------------- */
.chat_popup_user_board{
    display: flex;
    flex-direction: column;
    gap: 5px;
    overflow-y: auto;
    height: 200px;
    padding: 5px;
}
.chat_popup_user_board::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}

.chat_popup_user_board::-webkit-scrollbar-track {
    background: transparent !important;
}

.chat_popup_user_board::-webkit-scrollbar-thumb {
    background: var(--scroll_color);
    border-radius: 5px;
}

.chat_popup_user_board_user {
    display: flex;
    justify-content: space-between;
    padding: 5px;
    border-radius: 5px;
    cursor: pointer;
}

.chat_popup_user_board_user:hover {
    background: var(--hover_color);
}
</style>