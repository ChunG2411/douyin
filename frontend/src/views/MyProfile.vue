<script setup>
import VideoListComponent from '../components/video_list.vue'
import { Store } from '../assets/store.js'

import { reactive, ref } from 'vue'
import axios from 'axios'
import { vOnClickOutside } from '@vueuse/components'

const store = Store()

const profile = reactive({
    infor: null,
    followed: null,
    follower: null,
    active_tab: "video"
})

const modify_form = reactive({
    username: "",
    email: "",
    first_name: "",
    last_name: "",
    gender: "",
    birth: "",
    address: "",
    introduce: "",
    avatar: ""
})

const preview_image_upload = ref(null)

const show_modify_popup = ref(false)
const show_followed_popup = ref(false)
const show_follower_popup = ref(false)
const show_avatar_popup = ref(false)
const show_username_popup = ref(false)

const close_popup = [() => {
    show_modify_popup.value = false
    show_followed_popup.value = false
    show_follower_popup.value = false
    show_avatar_popup.value = false
    show_username_popup.value = false
}]


const api_get_my_profile = () => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.get(`${store.domain}/api/user/self`, header)
        .then(response => {
            profile.infor = response.data.data

            modify_form.username = response.data.data.username
            modify_form.email = response.data.data.email
            modify_form.first_name = response.data.data.first_name
            modify_form.last_name = response.data.data.last_name
            modify_form.gender = response.data.data.gender
            modify_form.birth = response.data.data.birth
            modify_form.address = response.data.data.address
            modify_form.introduce = response.data.data.introduce
            modify_form.avatar = response.data.data.avatar
        })
        .catch(error => {
            console.log(error);
            try {
                store.msg_error = error.response.data.msg
            }
            catch {
                store.msg_error = error
            }
        })
}
api_get_my_profile()

const modify_submit = () => {
    const form = new FormData()
    if (modify_form.username != profile.infor.username) {
        form.append('username', modify_form.username)

    }
    if (modify_form.email != profile.infor.email) {
        form.append('email', modify_form.email)
    }
    if (modify_form.avatar != profile.infor.avatar) {
        form.append('avatar', modify_form.avatar)
    }
    form.append('first_name', modify_form.first_name)
    form.append('last_name', modify_form.last_name)
    form.append('gender', modify_form.gender)
    form.append('birth', modify_form.birth)
    form.append('address', modify_form.address)
    form.append('introduce', modify_form.introduce)

    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.put(`${store.domain}/api/user/modify/${profile.infor.id}`, form, header)
        .then(response => {
            if (modify_form.username != profile.infor.username) {
                localStorage.setItem('username', modify_form.username)
            }
            location.reload()
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


const api_get_followed = () => {
    axios.get(`${store.domain}/api/user/${profile.infor.username}/followed-list`)
        .then(response => {
            profile.followed = response.data.data
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
const api_get_follower = () => {
    axios.get(`${store.domain}/api/user/${profile.infor.username}/follower-list`)
        .then(response => {
            profile.follower = response.data.data
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

const show_followed = () => {
    show_followed_popup.value = true
    api_get_followed()
}

const show_follower = () => {
    show_follower_popup.value = true
    api_get_follower()
}

const upload_image = (e) => {
    modify_form.avatar = e.target.files[0]
    preview_image_upload.value = URL.createObjectURL(modify_form.avatar)
}

</script>

<template>
    <div class="profile">
        <div class="profile-infor" v-if="profile.infor">
            <div>
                <div>
                    <img class="profile_avatar" :src="store.domain + profile.infor.avatar"
                        @click="show_avatar_popup = true">
                    <p>fullname: {{ profile.infor?.full_name }}</p>

                    <button @click="show_followed">followed: {{ profile.infor.followed_count }}</button>
                    <button @click="show_follower">follower: {{ profile.infor.follower_count }}</button>

                    <p @click="show_username_popup = true">username: {{ profile.infor.username }}</p>

                    <p v-if="profile.infor.gender">gender: {{ profile.infor.gender }}</p>
                    <p v-if="profile.infor.birth">birth: {{ profile.infor.birth }}</p>
                    <p v-if="profile.infor.address">address: {{ profile.infor.address }}</p>
                    <p v-if="profile.infor.introduce">introduce: {{ profile.infor.introduce }}</p>
                </div>

                <div>
                    <button @click="show_modify_popup = true">Modify</button>
                </div>
            </div>

            <div>
                <p id="created" @click="profile.active_tab = 'video'">created ({{ profile.infor.video_count }})</p>
                <p id="like" @click="profile.active_tab = 'like'">like</p>
                <p id="save" @click="profile.active_tab = 'save'">save</p>
            </div>
        </div>

        <div class="profile-video">
            <VideoListComponent :active="profile.active_tab" :username="store.my_profile.username" />
        </div>

        <div class="popup"
            v-if="store.msg_error || show_modify_popup || show_followed_popup || show_follower_popup || show_avatar_popup || show_username_popup">
            <div id="error-popup" v-if="store.msg_error">
                <p>{{ store.msg_error }}</p>
            </div>

            <div id="modify-popup" v-if="show_modify_popup" v-on-click-outside="close_popup">
                <form @submit.prevent="modify_submit">
                    <span>
                        <p>email</p>
                        <input type="text" v-model="modify_form.email" required>
                    </span>
                    <span>
                        <p>first_name</p>
                        <input type="text" v-model="modify_form.first_name" required>
                    </span>
                    <span>
                        <p>last_name</p>
                        <input type="text" v-model="modify_form.last_name" required>
                    </span>
                    <span>
                        <p>gender</p>
                        <select name="gender" v-model="modify_form.gender">
                            <option value="Male">Male</option>
                            <option value="Female">Female</option>
                            <option value="Other">Other</option>
                        </select>
                    </span>
                    <span>
                        <p>birth</p>
                        <input type="date" v-model="modify_form.birth">
                    </span>
                    <span>
                        <p>address</p>
                        <input type="text" v-model="modify_form.address">
                    </span>
                    <span>
                        <p>introduce</p>
                        <input type="text" v-model="modify_form.introduce">
                    </span>
                    <br>
                    <button type="submit">Submit</button>
                </form>
            </div>

            <div id="followed-popup" v-if="show_followed_popup" v-on-click-outside="close_popup">
                <b>Followed</b>
                <p v-for="user in profile.followed">{{ user.username }}</p>
            </div>
            <div id="follower-popup" v-if="show_follower_popup" v-on-click-outside="close_popup">
                <b>Follower</b>
                <p v-for="user in profile.follower">{{ user.username }}</p>
            </div>

            <div id="avatar-popup" v-if="show_avatar_popup" v-on-click-outside="close_popup">
                <form @submit.prevent="modify_submit">
                    <img class="show_profile_avatar" :src="store.domain + profile.infor?.avatar"
                        v-if="!preview_image_upload">
                    <img class="show_profile_avatar" :src="preview_image_upload" v-else>

                    <label for="image-upload">change</label>
                    <input type="file" id="image-upload" accept="image/*" style="display: none;" @change="upload_image">
                    <button type="submit">submit</button>
                </form>
            </div>

            <div id="username-popup" v-if="show_username_popup" v-on-click-outside="close_popup">
                <form @submit.prevent="modify_submit">
                    <p>username</p>
                    <input type="text" v-model="modify_form.username">
                    <button type="submit">submit</button>
                </form>
            </div>

        </div>
    </div>
</template>

<style>
.popup div {
    background: white;
}
</style>