<script setup>
import VideoListComponent from '../components/video_list.vue'
import config from '../assets/config.js'

import { reactive, ref, inject, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { vOnClickOutside } from '@vueuse/components'


const route = useRoute()

watch(() => route.params.username, (currentvalue, oldvalue) => {
    check_my_profile(currentvalue)
    api_get_user_infor(currentvalue)
})

const profile = reactive({
    infor: null,
    is_my_profile: false
})

const modify_form = reactive({
    first_name: "",
    last_name: "",
    gender: "",
    birth: "",
    address: ""
})

const user_followed = ref({})
const user_follower = ref({})

const user_localstore = inject("user_localstore")

const params_user = ref(route.params.username)

const msg_error = ref(null)
const action = ref("video")
const follow_status = ref('')

const show_modify_popup = ref(false)
const show_followed_popup = ref(false)
const show_follower_popup = ref(false)

const close_popup = [() => {
    show_modify_popup.value = false
    show_followed_popup.value = false
    show_follower_popup.value = false
}]

const check_my_profile = (username) => {
    if (user_localstore.is_authen) {
        if (username === user_localstore.user["username"]) {
            profile.is_my_profile = true
        }
        else {
            profile.is_my_profile = false
        }
    }
}
check_my_profile(params_user.value)

const api_get_user_infor = (username) => {
    axios.get(`${config.domain}/user/${username}`)
        .then(response => {
            profile.infor = response.data.data

            modify_form.first_name = response.data.data.first_name
            modify_form.last_name = response.data.data.last_name
            modify_form.gender = response.data.data.gender
            modify_form.birth = response.data.data.birth
            modify_form.address = response.data.data.address

            params_user.value = username
            action.value = "video"
        })
        .catch(e => {
            console.log(e)
            msg_error.value = e
        })
}
api_get_user_infor(params_user.value);


const modify_submit = () => {
    const header = {
            headers: { Authorization: `Bearer ${user_localstore.user["token"]}` }
        }
    axios.put(`${config.domain}/user/modify/${profile.infor.id}`, modify_form, header)
        .then(response => {
            location.reload()
        })
        .catch(e => {
            console.log(e)
            msg_error.value = e
        })
}


const api_get_followed = () => {
    axios.get(`${config.domain}/user/${profile.infor.username}/followed-list`)
        .then(response => {
            user_followed.value = response.data.data
        })
        .catch(e => {
            console.log(e)
            msg_error.value = e
        })
}
const api_get_follower = () => {
    axios.get(`${config.domain}/user/${profile.infor.username}/follower-list`)
        .then(response => {
            user_follower.value = response.data.data
        })
        .catch(e => {
            console.log(e)
            msg_error.value = e
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

const follow = () => {

}


</script>

<template>
    <div class="profile">
        <div class="profile-infor" v-if="profile.infor">
            <div>
                <div>
                    <p>fullname: {{ profile.infor.full_name }}</p>
                    <button @click="show_followed">followed: {{ profile.infor.followed_count }}</button>
                    <button @click="show_follower">follower: {{ profile.infor.follower_count }}</button>
                    <p>username: {{ profile.infor.username }}</p>
                    <p v-if="profile.infor.gender">gender: {{ profile.infor.gender }}</p>
                    <p v-if="profile.infor.birth">birth: {{ profile.infor.birth }}</p>
                    <p v-if="profile.infor.address">address: {{ profile.infor.address }}</p>
                    <p v-if="profile.infor.introduce">introduce: {{ profile.infor.introduce }}</p>
                </div>
                <div v-if="profile.is_my_profile">
                    <button @click="show_modify_popup = !show_modify_popup">Modify</button>
                </div>
                <div v-else>
                    <button @click="follow">{{ follow_status }}</button>
                </div>
            </div>
            <div>
                <p id="created" @click="action = 'video'">created ({{ profile.infor.video_count }})</p>
                <p id="like" @click="action = 'like'" v-if="profile.is_my_profile">like</p>
                <p id="save" @click="action = 'save'" v-if="profile.is_my_profile">save</p>
            </div>
        </div>

        <div class="profile-video">
            <VideoListComponent :action="action" :username="params_user" />
        </div>

        <div class="profile-popup" v-if="msg_error || show_modify_popup || show_followed_popup || show_follower_popup">
            <div id="error-popup" v-if="msg_error">
                <p>{{ msg_error }}</p>
            </div>

            <div id="modify-popup" v-if="show_modify_popup" v-on-click-outside="close_popup">
                <form @submit.prevent="modify_submit">
                    <span>
                        <p>first_name</p>
                        <input type="text" v-model="modify_form.first_name">
                    </span>
                    <span>
                        <p>last_name</p>
                        <input type="text" v-model="modify_form.last_name">
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
                    <br>
                    <button type="submit">Submit</button>
                </form>
            </div>

            <div id="followed-popup" v-if="show_followed_popup" v-on-click-outside="close_popup">
                <b>Followed</b>
                <p v-for="user in user_followed">{{ user.username }}</p>
            </div>
            <div id="follower-popup" v-if="show_follower_popup" v-on-click-outside="close_popup">
                <b>Follower</b>
                <p v-for="user in user_follower">{{ user.username }}</p>
            </div>
        </div>
    </div>
</template>

<style>
.profile-popup {
    background: rgba(226, 226, 226, 0.7);
    position: absolute;
    width: 100%;
    height: 100%;
    display: grid;
    place-items: center;
    z-index: 100;
    top: 0;
    left: 0;
}

.profile-popup div {
    background: white;
}
</style>