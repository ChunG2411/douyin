<script setup>
import { Store } from '../assets/store'
import { socket_message, socket_chat } from '../function/socket.js'

import { ref, reactive } from 'vue'
import axios from 'axios'
import jwt_decode from "jwt-decode"
import { vOnClickOutside } from '@vueuse/components'


const store = Store()
const decoded = jwt_decode(localStorage.getItem('token'))
const my_user = localStorage.getItem('username')

const chat_list = ref([])
const msg_list = ref([])
const msg_page = ref('0')
const chat_page = ref(0)
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
const show_leader_member_popup = ref(false)
const show_image_popup = ref(false)

const preview_image_upload = ref(null)
const preview_modify_image_upload = ref(null)
const preview_image_chat = ref(null)

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
        board_list_msg.value.scrollTop = board_list_msg.value.scrollHeight
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
                    new_message.value.reader.push(decoded.user_id)
                    msg_list.value.push(new_message.value)
                    scrollToEnd()
                }
            }
            else {
                for (let i = 0; i < chat_list.value.length; i++) {
                    if (chat_list.value[i].id == data.data.receiver) {
                        chat_list.value[i].last_message = store.translate("chat", "new")
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
    store.loading = true

    axios.get(`${store.domain}/api/chat/${id}/detail?page=${msg_page.value}`, header)
        .then(response => {
            for (let i = 0; i < response.data.data.length; i++) {
                msg_list.value.unshift(response.data.data[i])
                if (msg_page.value == '0') {
                    scrollToEnd()
                }
                else {
                    board_list_msg.value.scrollTop = board_list_msg.value.scrollHeight
                }
            }
            store.loading = false
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
                "receiver": id,
                "content": form_msg.text
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
            store.msg_success = store.translate("msg", "create")
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
            store.msg_success = store.translate("msg", "delete")
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
            store.msg_success = store.translate("msg", "add")
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
            store.msg_success = store.translate("msg", "remove")
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

const change_key = (id) => {
    show_member(id)
    show_leader_member_popup.value = true
}

const submit_change_key = (username) => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }

    const form = new FormData()
    form.append('username', username)

    axios.put(`${store.domain}/api/chat/${cur_chat.value.id}/change-key`, form, header)
        .then(response => {
            location.reload()
            store.msg_success = store.translate("msg", "change")
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

const exit_chat = (id) => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.get(`${store.domain}/api/chat/${id}/exit`, header)
        .then(response => {
            for (let i = 0; i < chat_list.value.length; i++) {
                if (chat_list.value[i].id == id) {
                    chat_list.value.splice(i, 1)
                }
            }
            cur_chat.value = null
            store.msg_success = store.translate("msg", "exit")
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
            store.msg_success = store.translate("msg", "modify")
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

const close_popup = [() => {
    show_modify_chat.value = false
    show_remove_member_popup.value = false
    show_add_member_popup.value = false
    show_member_chat.value = false
    show_add_chat_popup.value = false
    show_leader_member_popup.value = false
    show_image_popup.value = false

    add_member_list.value = []
    preview_image_chat.value = null
}]

const loadMoreChat = (e) => {
    const { scrollTop, offsetHeight, scrollHeight } = e.target
    if ((scrollTop + offsetHeight) >= scrollHeight) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        chat_page.value += 1
        axios.get(`${store.domain}/api/chat?page=${chat_page.value}`, header)
            .then(response => {
                if (response.data.data.length == 0) {
                    chat_page.value -= 1
                }
                else {
                    for (let i = 0; i < response.data.data.length; i++) {
                        chat_list.value.push(response.data.data[i])
                    }
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
}

</script>

<template>
    <div class="chat">
        <div class="chat_left">
            <div class="display_flex gap5 align_center">
                <button @click="add_new_chat">
                    <font-awesome-icon :icon="['fas', 'plus']" class="icon_17 normal_color" />
                </button>

                <input class="input" type="text" :placeholder="store.translate('header', 'search')"
                    v-model="search_chat.request" @input="get_search_chat">
                <div class="chat_search_board" v-if="search_chat.result.length > 0">
                    <div class="chat_search_board_item" v-for="result in search_chat.result"
                        @click="get_chat_detail(result)">
                        <img class="chat_avatar" :src="store.domain + result.avatar">
                        <p class="text normal_color fs_15" v-if="store.my_profile.username == result.user">{{ result.partner
                        }}
                        </p>
                        <p class="text normal_color fs_15" v-else>{{ result.name }}</p>
                    </div>
                </div>
            </div>
            <div class="chat_left_list" v-on:scroll="loadMoreChat">
                <div class="chat_left_list_item" v-for="chat in chat_list" :key="chat.id"
                    @click="msg_list = []; get_chat_detail(chat)">
                    <div>
                        <img class="chat_avatar" :src="store.domain + chat.avatar">
                    </div>
                    <div>
                        <p class="text normal_color fs_15" v-if="store.my_profile.username == chat.user">{{ chat.partner }}
                        </p>
                        <p class="text normal_color fs_15" v-else>{{ chat.name }}</p>
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
                        <p class="text normal_color fs_15" v-if="store.my_profile.username == cur_chat.user">{{
                            cur_chat.partner
                        }}</p>
                        <p class="text normal_color fs_15" v-else>{{ cur_chat.name }}</p>
                    </div>
                    <font-awesome-icon :icon="['fas', 'bars']" class="icon_25 normal_color mg_r_5 poiter"
                        @click="handle_action_chat" />
                </div>
                <div class="chat_right_content_bottom">
                    <div class="chat_right_content_bottom_content" ref="board_list_msg">
                        <div v-for="(msg, index) in msg_list">
                            <div class="display_flex justify_center">
                                <p class="normal_text normal_color fs_11 poiter" @click="load_more_msg(cur_chat.id)"
                                    v-if="index == 0 && msg.have_more == 'True'">
                                    {{ store.translate("comment", "more") }}
                                </p>
                            </div>
                            <div class="msg_right" v-if="decoded.user_id == msg.sender">
                                <div class="msg_item">
                                    <p class="normal_text normal_color fs_13" v-if="msg.context">{{ msg.context }}</p>
                                    <div>
                                        <img class="message_image" :src="store.domain + msg.media" v-if="msg.media"
                                            @click="preview_image_chat = store.domain + msg.media; show_image_popup = true">
                                    </div>
                                </div>
                            </div>
                            <div class="msg_left" v-else>
                                <div class="msg_item">
                                    <p class="normal_text normal_color fs_13" v-if="msg.context">{{ msg.context }}</p>
                                    <div>
                                        <img class="message_image" :src="store.domain + msg.media" v-if="msg.media"
                                            @click="preview_image_chat = store.domain + msg.media; show_image_popup = true">
                                    </div>
                                </div>
                            </div>

                            <div v-if="msg.reader.length < cur_chat.member.length">
                                <p class="normal_text normal_color fs_11">{{ msg.reader.length }} {{ store.translate("chat",
                                    "readed") }}</p>
                            </div>
                            <div v-else-if="cur_chat.member.length == msg.reader.length && index == (msg_list.length - 1)">
                                <p class="normal_text normal_color fs_11">{{ msg.reader.length }} {{ store.translate("chat",
                                    "readed") }}</p>
                            </div>
                        </div>
                    </div>
                    <form class="chat_right_content_bottom_form" @submit.prevent="submit_form(cur_chat.id)">
                        <input type="file" accept="image/*" @change="upload_image" id="upload_image" style="display: none;">
                        <label for="upload_image">
                            <font-awesome-icon :icon="['fas', 'image']" class="icon_25 normal_color" />
                        </label>
                        <input type="text" class="input" :placeholder="store.translate('chat', 'message')"
                            v-model="form_msg.text">

                        <div class="chat_preveiw" v-if="preview_image_upload">
                            <img class="chat_preveiw_image" :src="preview_image_upload">
                            <div class="display_flex_column gap5">
                                <label class="button fs_13" @click="remove_form_media">{{ store.translate("comment",
                                    "remove") }}</label>
                                <label class="button fs_13" for="upload_image">{{ store.translate("profile",
                                    "change") }}</label>
                            </div>
                        </div>
                        <button type="submit" class="submit_icon">
                            <font-awesome-icon :icon="['fas', 'paper-plane']" class="icon_20 normal_color" />
                        </button>
                    </form>
                </div>
            </div>
            <div class="chat_right_action" v-if="show_action_chat">
                <div class="display_flex_column align_center gap10">
                    <img class="chat_avatar_detail" :src="store.domain + cur_chat.avatar"
                        @click="preview_image_chat = store.domain + cur_chat.avatar; show_image_popup = true">
                    <p class="text normal_color fs_15" v-if="store.my_profile.username == cur_chat.user">{{ cur_chat.partner
                    }}</p>
                    <p class="text normal_color fs_15" v-else>{{ cur_chat.name }}</p>
                </div>
                <div class="chat_right_action_item">
                    <div class="display_flex gap10 align_center" v-if="cur_chat.type != 'single'">
                        <font-awesome-icon :icon="['fas', 'pen-to-square']" class="icon_15 normal_color" />
                        <p class="normal_text normal_color fs_15" @click="modify_chat(cur_chat)">
                            {{ store.translate("profile", "modify") }}</p>
                    </div>
                    <div class="display_flex gap10 align_center" v-if="cur_chat.type == 'single'">
                        <font-awesome-icon :icon="['fas', 'trash']" class="icon_15 normal_color" />
                        <p class="normal_text normal_color fs_15" @click="delete_chat(cur_chat.id)">
                            {{ store.translate("noti", "delete") }}</p>
                    </div>
                    <div class="display_flex gap10 align_center"
                        v-if="cur_chat.type != 'single' && cur_chat.user == my_user">
                        <font-awesome-icon :icon="['fas', 'trash']" class="icon_15 normal_color" />
                        <p class="normal_text normal_color fs_15" @click="delete_chat(cur_chat.id)">
                            {{ store.translate("noti", "delete") }}</p>
                    </div>
                    <div class="display_flex gap10 align_center">
                        <font-awesome-icon :icon="['fas', 'user-group']" class="icon normal_color" />
                        <p class="normal_text normal_color fs_15"
                            @click="show_member_chat = true; show_member(cur_chat.id)">
                            {{ store.translate("chat", "member") }}</p>
                    </div>
                    <div class="display_flex gap10 align_center" v-if="cur_chat.type != 'single'">
                        <font-awesome-icon :icon="['fas', 'user-plus']" class="icon normal_color" />
                        <p class="normal_text normal_color fs_15" @click="add_member_to_chat(cur_chat.id)">
                            {{ store.translate("chat", "add_member") }}
                        </p>
                    </div>
                    <div class="display_flex gap10 align_center"
                        v-if="cur_chat.type != 'single' && store.my_profile.username == cur_chat.user">
                        <font-awesome-icon :icon="['fas', 'user-minus']" class="icon normal_color" />
                        <p class="normal_text normal_color fs_15" @click="remove_member_to_chat(cur_chat.id)">
                            {{ store.translate("chat", "remove_member") }}
                        </p>
                    </div>
                    <div class="display_flex gap10 align_center"
                        v-if="cur_chat.type != 'single' && store.my_profile.username == cur_chat.user">
                        <font-awesome-icon :icon="['fas', 'key']" class="icon normal_color" />
                        <p class="normal_text normal_color fs_15" @click="change_key(cur_chat.id)">
                            {{ store.translate("chat", "key") }}
                        </p>
                    </div>
                    <div class="display_flex gap10 align_center" v-if="cur_chat.type != 'single'">
                        <font-awesome-icon :icon="['fas', 'arrow-right-from-bracket']" class="icon normal_color" />
                        <p class="normal_text normal_color fs_15" @click="exit_chat(cur_chat.id)">
                            {{ store.translate("chat", "exit") }}
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <div class="popup"
            v-if="show_add_chat_popup || show_member_chat || show_add_member_popup || show_remove_member_popup || show_modify_chat || show_leader_member_popup || show_image_popup">
            <div class="popup_board" v-if="show_add_chat_popup" v-on-click-outside="close_popup">
                <p class="text normal_color fs_17">{{ store.translate("chat", "add_chat") }}</p>
                <div class="chat_popup_add">
                    <div>
                        <p class="text normal_color fs_15">{{ store.translate("chat", "select_member") }}</p>
                        <div class="chat_popup_add_board">
                            <div class="chat_popup_add_board_item" v-for="(member, index) in member_chat" :key="index"
                                @click="member_chat.splice(index, 1)">
                                <img class="chat_avatar" :src="store.domain + member.avatar">
                                <p class="text normal_color fs_15">{{ member.full_name }}</p>
                            </div>
                        </div>
                    </div>
                    <div>
                        <p class="text normal_color fs_15">{{ store.translate("chat", "list_follower") }}</p>
                        <div class="chat_popup_add_board">
                            <div class="chat_popup_add_board_item" v-for="user in follower" @click="member_chat.push(user)">
                                <img class="chat_avatar" :src="store.domain + user.avatar">
                                <p class="text normal_color fs_15">{{ user.full_name }}</p>
                            </div>
                        </div>
                    </div>
                    <div class="display_flex justify_center">
                        <button @click="submit_new_chat" class="fs_17">{{ store.translate("chat", "create") }}</button>
                    </div>
                </div>
            </div>

            <div class="popup_board" v-if="show_member_chat" v-on-click-outside="close_popup">
                <p class="text normal_color fs_17">{{ store.translate("chat", "member") }}</p>
                <div class="chat_popup_member">
                    <div class="chat_popup_member_item" v-for="member in member_list" :key="member.id">
                        <router-link :to="{ name: 'guest_profile', params: { username: member.username } }"
                            v-if="member.username != my_user && cur_chat.user != member.username"
                            class="display_flex gap20 align_center no_decor">
                            <img class="chat_avatar" :src="store.domain + member.avatar">
                            <p class="text normal_color fs_15">{{ member.full_name }}</p>
                        </router-link>

                        <router-link :to="{ name: 'guest_profile', params: { username: member.username } }"
                            v-else-if="member.username != my_user && cur_chat.user == member.username"
                            class="display_flex gap20 align_center no_decor">
                            <img class="chat_avatar" :src="store.domain + member.avatar">
                            <div class="display_flex gap10 align_center">
                                <p class="text normal_color fs_15">{{ member.full_name }}</p>
                                <font-awesome-icon :icon="['fas', 'key']" class="icon normal_color" />
                            </div>
                        </router-link>

                        <router-link to="/profile/self"
                            v-else-if="member.username == my_user && cur_chat.user != member.username"
                            class="display_flex gap20 align_center no_decor">
                            <img class="chat_avatar" :src="store.domain + member.avatar">
                            <p class="text normal_color fs_15">{{ member.full_name }} {{ store.translate("chat", "you") }}
                            </p>
                        </router-link>

                        <router-link to="/profile/self"
                            v-else-if="member.username == my_user && cur_chat.user == member.username"
                            class="display_flex gap20 align_center no_decor">
                            <img class="chat_avatar" :src="store.domain + member.avatar">
                            <div class="display_flex gap10 align_center">
                                <p class="text normal_color fs_15">{{ member.full_name }} {{ store.translate("chat", "you")
                                }}</p>
                                <font-awesome-icon :icon="['fas', 'key']" class="icon normal_color" />
                            </div>
                        </router-link>
                    </div>
                </div>
            </div>

            <div class="popup_board" v-if="show_leader_member_popup" v-on-click-outside="close_popup">
                <p class="text normal_color fs_17">{{ store.translate("chat", "member") }}</p>
                <div class="chat_popup_member">
                    <div class="chat_popup_member_item" v-for="member in member_list" :key="member.id">
                        <div v-if="member.username != my_user && cur_chat.user != member.username"
                            class="display_flex align_center justify_space no_decor width_100">
                            <div class="display_flex gap20 align_center">
                                <img class="chat_avatar" :src="store.domain + member.avatar">
                                <p class="text normal_color fs_15">{{ member.full_name }}</p>
                            </div>
                            <div class="display_flex gap10 align_center">
                                <router-link :to="{ name: 'guest_profile', params: { username: member.username } }"
                                    class="button no_decor fs_13">
                                    {{ store.translate("search", "view") }}
                                </router-link>
                                <button class="fs_13" @click="submit_change_key(member.username)">{{ store.translate("chat",
                                    "change")
                                }}</button>
                            </div>
                        </div>

                        <router-link :to="{ name: 'guest_profile', params: { username: member.username } }"
                            v-else-if="member.username != my_user && cur_chat.user == member.username"
                            class="display_flex gap20 align_center no_decor">
                            <img class="chat_avatar" :src="store.domain + member.avatar">
                            <div class="display_flex gap10 align_center">
                                <p class="text normal_color fs_15">{{ member.full_name }}</p>
                                <font-awesome-icon :icon="['fas', 'key']" class="icon normal_color" />
                            </div>
                        </router-link>

                        <div v-else-if="member.username == my_user && cur_chat.user != member.username"
                            class="display_flex align_center justify_space no_decor width_100">
                            <div class="display_flex gap20 align_center">
                                <img class="chat_avatar" :src="store.domain + member.avatar">
                                <p class="text normal_color fs_15">{{ member.full_name }}</p>
                            </div>
                        </div>

                        <div v-else-if="member.username == my_user && cur_chat.user == member.username"
                            class="display_flex gap20 align_center no_decor">
                            <img class="chat_avatar" :src="store.domain + member.avatar">
                            <div class="display_flex gap10 align_center">
                                <p class="text normal_color fs_15">{{ member.full_name }} {{ store.translate("chat", "you")
                                }}</p>
                                <font-awesome-icon :icon="['fas', 'key']" class="icon normal_color" />
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="popup_board" v-if="show_add_member_popup" v-on-click-outside="close_popup">
                <p class="text normal_color fs-17">{{ store.translate("chat", "add_member") }}</p>
                <div class="chat_popup_add">
                    <div>
                        <p class="text normal_color fs_15">{{ store.translate("chat", "new_member") }}</p>
                        <div class="chat_popup_add_board">
                            <div class="chat_popup_add_board_item" v-for="(member, index) in add_member_list"
                                @click="add_member_list.splice(index, 1)">
                                <img class="chat_avatar" :src="store.domain + member.avatar">
                                <p class="text normal_color fs_15">{{ member.full_name }}</p>
                            </div>
                        </div>
                    </div>
                    <div>
                        <p class="text normal_color fs_15">{{ store.translate("chat", "list_follower") }}</p>
                        <div class="chat_popup_add_board">
                            <div class="chat_popup_add_board_item" v-for="user in follower" :key="user.id"
                                @click="add_member_list.push(user)">
                                <img class="chat_avatar" :src="store.domain + user.avatar">
                                <p class="text normal_color fs_15">{{ user.full_name }}</p>
                            </div>
                        </div>
                    </div>
                    <div class="display_flex justify_center">
                        <button @click="submit_add_new_member" class="fs_17">{{ store.translate("profile",
                            "submit") }}</button>
                    </div>
                </div>
            </div>

            <div class="popup_board" v-if="show_remove_member_popup" v-on-click-outside="close_popup">
                <p class="text normal_color fs_17">{{ store.translate("chat", "remove_member") }}</p>
                <div class="chat_popup_member">
                    <div class="chat_popup_member_item" v-for="(member, index) in member_list" :key="index">
                        <div class="display_flex align_center justify_space width_100">
                            <div class="display_flex gap20 align_center">
                                <img class="chat_avatar" :src="store.domain + member.avatar">
                                <p class="text normal_color fs_15">{{ member.full_name }}</p>
                            </div>
                            <button @click="submit_remove_member(member.username, index)"
                                v-if="my_user != member.username">{{ store.translate("comment", "remove") }}</button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="popup_board" v-if="show_modify_chat" v-on-click-outside="close_popup">
                <p class="text normal_color fs_17">{{ store.translate("profile", "modify") }}</p>
                <form @submit.prevent="submit_modify_form" class="chat_popup_modify">
                    <div>
                        <p class="text normal_color fs_15">{{ store.translate("chat", "name") }}</p>
                        <input type="text" class="input mg_l_10 mg_t_10" v-model="form_modify.name">
                    </div>
                    <div>
                        <p class="text normal_color fs_15">{{ store.translate("profile", "avatar") }}</p>
                        <div class="display_flex_column gap20 mg_t_10 align_center">
                            <img class="chat_avatar_detail" :src="store.domain + cur_chat.avatar"
                                v-if="!preview_modify_image_upload">
                            <img class="chat_avatar_detail" :src="preview_modify_image_upload" v-else>
                            <input type="file" accept="image/*" style="display: none;" id="modify_upload_avatar"
                                @change="change_avatar_chat">
                            <label for="modify_upload_avatar" class="button fs_15">{{ store.translate("profile",
                                "change") }}</label>
                        </div>
                    </div>
                    <div class="display_flex justify_center">
                        <button type="submit" class="fs_17">{{ store.translate("profile", "submit") }}</button>
                    </div>
                </form>
            </div>

            <div class="popup_board" v-if="show_image_popup" v-on-click-outside="close_popup">
                <img class="preview_image_chat" :src="preview_image_chat">
            </div>
        </div>
    </div>
</template>

<style>
.chat {
    width: 98%;
    height: 98%;
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
    padding: 5px 15px;
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
    padding: 5px 15px;
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
/* -------------member--------------- */
.chat_popup_member {
    margin-left: 10px;
    max-height: 550px;
    height: max-content;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 5px;
    margin-top: 10px;
}

.chat_popup_member::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}

.chat_popup_member::-webkit-scrollbar-track {
    background: transparent !important;
}

.chat_popup_member::-webkit-scrollbar-thumb {
    background: var(--scroll_color);
    border-radius: 5px;
}

.chat_popup_member_item {
    display: flex;
    align-items: center;
    border-radius: 5px;
    padding: 5px 10px;
    cursor: pointer;
}

.chat_popup_member_item:hover {
    background: var(--hover_color);
}

/* ---------add------------- */
.chat_popup_add {
    margin-left: 10px;
    max-height: 550px;
    height: max-content;
    display: flex;
    flex-direction: column;
    gap: 5px;
    margin-top: 10px;
}

.chat_popup_add_board {
    display: flex;
    flex-direction: column;
    gap: 5px;
    height: 200px;
    overflow-y: auto;
    margin-top: 5px;
}

.chat_popup_add_board::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}

.chat_popup_add_board::-webkit-scrollbar-track {
    background: transparent !important;
}

.chat_popup_add_board::-webkit-scrollbar-thumb {
    background: var(--scroll_color);
    border-radius: 5px;
}

.chat_popup_add_board_item {
    display: flex;
    gap: 20px;
    align-items: center;
    border-radius: 5px;
    cursor: pointer;
    padding: 5px 10px;
}

.chat_popup_add_board_item:hover {
    background: var(--hover_color);
}

/* ---------------modify------------ */
.chat_popup_modify {
    margin-left: 10px;
    max-height: 550px;
    height: max-content;
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-top: 10px;
}
</style>