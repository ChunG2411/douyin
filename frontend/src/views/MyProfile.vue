<script setup>
import VideoListComponent from '../components/video_list.vue'
import { Store } from '../assets/store.js'

import { reactive, ref, onMounted } from 'vue'
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

    preview_image_upload.value = store.domain + profile.infor.avatar
    modify_form.username = profile.infor.username
    modify_form.email = profile.infor.email
    modify_form.first_name = profile.infor.first_name
    modify_form.last_name = profile.infor.last_name
    modify_form.gender = profile.infor.gender
    modify_form.birth = profile.infor.birth
    modify_form.address = profile.infor.address
    modify_form.introduce = profile.infor.introduce
    modify_form.avatar = profile.infor.avatar
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

// active tag
const tag_item = ref(null)

const remove_active_tag = () => {
    tag_item.value.forEach(item => {
        item.classList.remove('active_tag')
    })
}
onMounted(() => {
    tag_item.value = document.querySelectorAll('.tag_item')
    tag_item.value.forEach(item => {
        item.addEventListener('click', () => {
            remove_active_tag()
            item.classList.add('active_tag')
            profile.active_tab = item.id
        })
    })
})

</script>

<template>
    <div class="profile">
        <div class="profile_infor" v-if="profile.infor">
            <div class="profile_infor_left">
                <div class="profile_infor_avatar">
                    <img class="profile_avatar" :src="store.domain + profile.infor.avatar"
                        @click="show_avatar_popup = true">
                </div>
                <div class="profile_infor_content">
                    <div>
                        <p class="fullname fs_20">{{ profile.infor.full_name }}</p>
                        <p class="username gray fs_13" @click="show_username_popup = true">@{{ profile.infor.username }}</p>
                    </div>
                    <div class="profile_follow_infor">
                        <button @click="show_followed" class="fs_13">{{store.translate("profile", "followed")}}: {{ profile.infor.followed_count }}</button>
                        <button @click="show_follower" class="fs_13">{{store.translate("profile", "follower")}}: {{ profile.infor.follower_count }}</button>
                    </div>
                    <div>
                        <div class="display_flex gap10">
                            <div class="display_flex gap5 align_center">
                                <font-awesome-icon :icon="['fas', 'transgender']" class="icon gray" />
                                <p class="normal_text gray fs_13" v-if="profile.infor.gender">{{ profile.infor.gender }}
                                </p>
                            </div>
                            <div class="display_flex gap5 align_center">
                                <font-awesome-icon :icon="['fas', 'cake-candles']" class="icon gray" />
                                <p class="normal_text gray fs_13" v-if="profile.infor.birth">{{ profile.infor.birth }}</p>
                            </div>
                        </div>
                        <div class="display_flex gap5 align_center">
                            <font-awesome-icon :icon="['fas', 'location-dot']" class="icon gray" />
                            <p class="normal_text gray fs_13" v-if="profile.infor.address">{{ profile.infor.address }}</p>
                        </div>
                        <p class="normal_text gray fs_15" v-if="profile.infor.introduce">{{ profile.infor.introduce }}</p>
                    </div>
                </div>
            </div>
            <div class="profile_infor_right">
                <button @click="show_modify_popup = true" class="display_flex gap10 align_center">
                    <font-awesome-icon :icon="['fas', 'pen']" class="icon normal_color"/>
                    <p class="normal_text normal_colo fs_15">{{store.translate("profile", "modify")}}</p>
                </button>
            </div>
        </div>

        <div class="profile_video">
            <div class="profile_video_tag">
                <div class="tag_item active_tag" id="video">
                    <p class="text normal_color fs_15">{{store.translate("profile", "create")}}</p>
                </div>
                <div class="tag_item" id="like">
                    <p class="text normal_color fs_15">{{store.translate("profile", "like")}}</p>
                </div>
                <div class="tag_item" id="save">
                    <p class="text normal_color fs_15">{{store.translate("profile", "save")}}</p>
                </div>
            </div>
            <VideoListComponent :active="profile.active_tab" :username="store.my_profile.username" />
        </div>

        <div class="popup"
            v-if="show_modify_popup || show_followed_popup || show_follower_popup || show_avatar_popup || show_username_popup">
            <div class="popup_board" id="modify_popup" v-if="show_modify_popup" v-on-click-outside="close_popup">
                <p class="text normal_color fs_17">{{store.translate("profile", "modify")}}</p>
                <form @submit.prevent="modify_submit" class="modify_form">
                    <div class="display_flex gap5 align_center justify_space mg_t_5 mg_b_5">
                        <p class="normal_text normal_color fs_15">{{store.translate("authen", "email")}}</p>
                        <input class="input" type="text" v-model="modify_form.email" required>
                    </div>
                    <div class="display_flex gap5 align_center justify_space mg_b_5">
                        <p class="normal_text normal_color fs_15">{{store.translate("authen", "first_name")}}</p>
                        <input class="input" type="text" v-model="modify_form.first_name" required>
                    </div>
                    <div class="display_flex gap5 align_center justify_space mg_b_5">
                        <p class="normal_text normal_color fs_15">{{store.translate("authen", "last_name")}}</p>
                        <input class="input" type="text" v-model="modify_form.last_name" required>
                    </div>
                    <div class="display_flex gap5 align_center justify_space mg_b_5">
                        <p class="normal_text normal_color fs_15">{{store.translate("authen", "gender")}}</p>
                        <select class="select" name="gender" v-model="modify_form.gender">
                            <option value="Male">{{store.translate("authen", "male")}}</option>
                            <option value="Female">{{store.translate("authen", "female")}}</option>
                            <option value="Other">{{store.translate("authen", "other")}}</option>
                        </select>
                    </div>
                    <div class="display_flex gap5 align_center justify_space mg_b_5">
                        <p class="normal_text normal_color fs_15">{{store.translate("profile", "birth")}}</p>
                        <input class="input" type="date" v-model="modify_form.birth">
                    </div>
                    <div class="display_flex gap5 align_center justify_space mg_b_5">
                        <p class="normal_text normal_color fs_15">{{store.translate("profile", "address")}}</p>
                        <input class="input" type="text" v-model="modify_form.address">
                    </div>
                    <div class="display_flex gap5 align_center justify_space mg_b_5">
                        <p class="normal_text normal_color fs_15">{{store.translate("profile", "intro")}}</p>
                        <input class="input" type="text" v-model="modify_form.introduce">
                    </div>
                    <div class="display_flex justify_center mg_t_5 mg_b_5">
                        <button type="submit" class="fs_15">{{store.translate("profile", "submit")}}</button>
                    </div>
                </form>
            </div>

            <div class="popup_board" id="followed_popup" v-if="show_followed_popup" v-on-click-outside="close_popup">
                <p class="text normal_color fs_17">{{store.translate("profile", "followed")}}</p>
                <div class="follow_board">
                    <div class="follow_board_item poiter" v-for="user in profile.followed">
                        <div class="follow_context">
                            <img class="profile_avatar_folllow" :src="store.domain + user.avatar">
                            <p class="text normal_color fs_15">{{ user.full_name }}</p>
                        </div>
                        <button>
                            <router-link class="text normal_color fs_15"
                                :to="{ name: 'guest_profile', params: { username: user.username } }">{{store.translate("search", "view")}}</router-link>
                        </button>
                    </div>
                </div>
            </div>
            <div class="popup_board" id="follower_popup" v-if="show_follower_popup" v-on-click-outside="close_popup">
                <p class="text normal_color fs_17">{{store.translate("profile", "follower")}}</p>
                <div class="follow_board">
                    <div class="follow_board_item poiter" v-for="user in profile.follower">
                        <div class="follow_context">
                            <img class="profile_avatar_folllow" :src="store.domain + user.avatar">
                            <p class="text normal_color fs_15">{{ user.full_name }}</p>
                        </div>
                        <button>
                            <router-link class="text normal_color fs_15"
                                :to="{ name: 'guest_profile', params: { username: user.username } }">{{store.translate("search", "view")}}</router-link>
                        </button>
                    </div>
                </div>
            </div>

            <div class="popup_board" id="avatar_popup" v-if="show_avatar_popup" v-on-click-outside="close_popup">
                <p class="text normal_color fs_17">{{store.translate("profile", "avatar")}}</p>

                <form @submit.prevent="modify_submit" class="display_flex_column gap5 align_center">
                    <img class="show_profile_avatar" :src="store.domain + profile.infor?.avatar"
                        v-if="!preview_image_upload">
                    <img class="show_profile_avatar" :src="preview_image_upload" v-else>

                    <label class="button fs_15" for="image-upload">{{store.translate("profile", "change")}}</label>
                    <input type="file" id="image-upload" accept="image/*" style="display: none;" @change="upload_image">
                    <button type="submit" class="fs_15">{{store.translate("profile", "submit")}}</button>
                </form>
            </div>

            <div class="popup_board" id="username_popup" v-if="show_username_popup" v-on-click-outside="close_popup">
                <p class="text normal_color fs_17">{{store.translate("profile", "username")}}</p>

                <form @submit.prevent="modify_submit" class="display_flex_column gap5 align_center">
                    <input class="input" type="text" v-model="modify_form.username">
                    <button type="submit" class="fs_15">{{store.translate("profile", "submit")}}</button>
                </form>
            </div>
        </div>
    </div>
</template>

<style>
.profile {
    width: 98%;
    height: 100%;
}

.profile_infor {
    width: 97%;
    height: 30%;
    padding: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.profile_infor_left {
    display: flex;
}

.profile_infor_avatar {
    padding: 10px 20px;
}

.fullname {
    font-size: 20px;
    font-weight: 500;
    color: var(--text_color);
    margin-bottom: 0;
}

.username {
    font-size: 13px;
    font-weight: 350;
    color: var(--text_color);
    margin: 0;
}

.profile_follow_infor {
    margin: 5px 0 5px 0;
    display: flex;
    gap: 5px;
}

.profile_video {
    width: 97%;
    height: 65%;
    padding: 10px;
}

.profile_video_tag {
    display: flex;
    width: 100%;
    padding: 5px;
    height: 20px;
    margin-bottom: 10px;
    align-items: center;
}

.tag_item {
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
}

.active_tag {
    background: var(--hover_color);
}

.follow_board {
    height: 93%;
    overflow-y: scroll;
    display: flex;
    flex-direction: column;
    margin-top: 10px;
}

.follow_board::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}

.follow_board::-webkit-scrollbar-track {
    background: transparent !important;
}

.follow_board::-webkit-scrollbar-thumb {
    background: var(--scroll_color);
    border-radius: 5px;
}

.follow_board_item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
    align-items: center;
    padding: 10px;
    border-radius: 10px;
}

.follow_board_item:hover {
    background: var(--hover_color);
}

.follow_context {
    display: flex;
    gap: 10px;
    align-items: center;
}

.modify_form {
    width: 80%;
    margin-left: 25px;
}
</style>