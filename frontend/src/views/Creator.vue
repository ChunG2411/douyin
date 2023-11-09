<script setup>
import { Store } from '../assets/store'

import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'
import { vOnClickOutside } from '@vueuse/components'


const store = Store()

const upload_video_form = reactive({
    descrip: '',
    video: '',
    video_volumn: '1',
    use_video_music: '1',
    music: '',
    music_volumn: '1',
    public: true
})
const upload_music_form = reactive({
    name: '',
    music: ''
})
const active_bar = reactive({
    create_video: true,
    create_music: false,
    manager: false
})

const show_music_list = ref(false)

const music_list = ref([])
const my_video_list = ref([])
const my_music_list = ref([])
const page_music = ref(0)
const page_video = ref(0)
const page_music_select = ref(0)

const preveiw = reactive({
    video: null,
    music: null
})


const close_popup = [() => {
    show_music_list.value = false
}]

const upload_video = (e) => {
    upload_video_form.video = e.target.files[0]
    preveiw.video = URL.createObjectURL(upload_video_form.video)
}

const get_music_list = () => {
    show_music_list.value = true

    axios.get(`${store.domain}/api/music`)
        .then(response => {
            music_list.value = response.data.data
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

const select_music = (object) => {
    upload_video_form.music = object
    upload_video_form.use_video_music = '0'
    show_music_list.value = false
}

const remove_music = () => {
    upload_video_form.music = ''
    upload_video_form.use_video_music = '1'
    music_play.value = false
}

const submit_upload_video = () => {
    store.loading = true

    const form = new FormData()
    form.append('descrip', upload_video_form.descrip)
    form.append('video', upload_video_form.video)
    form.append('use_video_music', upload_video_form.use_video_music)

    if (upload_video_form.use_video_music == '1') {
        form.append('music', '')
    }
    else {
        form.append('music', upload_video_form.music.id)
    }
    form.append('music_volumn', upload_video_form.music_volumn)
    form.append('video_volumn', upload_video_form.video_volumn)
    form.append('public', upload_video_form.public)

    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.post(`${store.domain}/api/user/${localStorage.getItem('username')}/video`, form, header)
        .then(response => {
            store.loading = false
            store.msg_success = store.translate("msg", "success")
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

const delete_video = (id) => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.delete(`${store.domain}/api/user/${localStorage.getItem('username')}/video/${id}`, header)
        .then(response => {
            for (let i = 0; i < my_video_list.value.length; i++) {
                if (my_video_list.value[i].id == id) {
                    my_video_list.value.splice(i, 1)
                }
            }
            store.msg_success = store.translate("msg", "delete")
        })
        .catch(error => {
            try {
                store.error = error.response.data.msg
            }
            catch {
                store.error = error
            }
        })
}

const upload_music = (e) => {
    upload_music_form.music = e.target.files[0]
    preveiw.music = URL.createObjectURL(upload_music_form.music)
}

const submit_upload_music = () => {
    store.loading = true

    const form = new FormData()
    form.append('name', upload_music_form.name)
    form.append('music', upload_music_form.music)

    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.post(`${store.domain}/api/music`, form, header)
        .then(response => {
            store.msg_success = store.translate("msg", "create")
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


const api_get_video_list = () => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }

    axios.get(`${store.domain}/api/user/${localStorage.getItem('username')}/video`, header)
        .then(response => {
            my_video_list.value = response.data.data
        })
        .catch(error => {
            try {
                store.error = error.response.data.msg
            }
            catch {
                store.error = error
            }
        })
}

const api_get_music_list = () => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.get(`${store.domain}/api/music/self`, header)
        .then(response => {
            my_music_list.value = response.data.data
        })
        .catch(error => {
            try {
                store.error = error.response.data.msg
            }
            catch {
                store.error = error
            }
        })
}

const delete_music = (id) => {
    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.delete(`${store.domain}/api/music/${id}`, header)
        .then(response => {
            for (let i = 0; i < my_music_list.value.length; i++) {
                if (my_music_list.value[i].id == id) {
                    my_music_list.value.splice(i, 1)
                }
            }
            store.msg_success = store.translate("msg", "delete")
        })
        .catch(error => {
            try {
                store.error = error.response.data.msg
            }
            catch {
                store.error = error
            }
        })
}

const active_tab = (type) => {
    if (type == "video") {
        active_bar.create_video = true
        active_bar.create_music = false
        active_bar.manager = false
    }
    else if (type == "music") {
        active_bar.create_video = false
        active_bar.create_music = true
        active_bar.manager = false
    }
    else if (type == "manager") {
        active_bar.create_video = false
        active_bar.create_music = false
        active_bar.manager = true
        api_get_video_list()
        api_get_music_list()
    }
}

const loadMoreVideo = (e) => {
    const { scrollTop, offsetHeight, scrollHeight } = e.target
    if ((scrollTop + offsetHeight) >= scrollHeight) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        page_video.value += 1
        axios.get(`${store.domain}/api/user/${localStorage.getItem('username')}/video?page=${page_video.value}`, header)
            .then(response => {
                if (response.data.data.length == 0) {
                    page_video.value -= 1
                }
                else {
                    for (let i = 0; i < response.data.data.length; i++) {
                        my_video_list.value.push(response.data.data[i])
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
const loadMoreMusic = (e) => {
    const { scrollTop, offsetHeight, scrollHeight } = e.target
    if ((scrollTop + offsetHeight) >= scrollHeight) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        page_music.value += 1
        axios.get(`${store.domain}/api/music/self?page=${page_music.value}`, header)
            .then(response => {
                if (response.data.data.length == 0) {
                    page_music.value -= 1
                }
                else {
                    for (let i = 0; i < response.data.data.length; i++) {
                        my_music_list.value.push(response.data.data[i])
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
const loadMoreMusic_list = (e) => {
    const { scrollTop, offsetHeight, scrollHeight } = e.target
    if ((scrollTop + offsetHeight) >= scrollHeight) {
        const header = {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }
        page_music_select.value += 1
        axios.get(`${store.domain}/api/music?page=${page_music_select.value}`, header)
            .then(response => {
                if (response.data.data.length == 0) {
                    page_music_select.value -= 1
                }
                else {
                    for (let i = 0; i < response.data.data.length; i++) {
                        music_list.value.push(response.data.data[i])
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

window.addEventListener('scroll', loadMoreVideo)
window.addEventListener('scroll', loadMoreMusic)
window.addEventListener('scroll', loadMoreMusic_list)

// active tag
const creator_tag = ref(null)

const removeActive_search = () => {
    creator_tag.value.forEach(item => {
        item.classList.remove('creator_active_tag')
    })
}

onMounted(() => {
    creator_tag.value = document.querySelectorAll('.creator_tag_item')
    creator_tag.value.forEach(item => {
        item.addEventListener('click', () => {
            removeActive_search()
            item.classList.add('creator_active_tag')
        })
    })
})

// 
const music_player = ref(null)
const music_play = ref(false)
const video_player = ref(null)

const handle_music = () => {
    if (music_play.value) {
        music_play.value = false
        music_player.value.pause()
    }
    else {
        music_play.value = true
        music_player.value.play()
    }
}

const preview_video = () => {
    if (music_player.value) {
        music_player.value.volume = parseFloat(upload_video_form.music_volumn)
        music_player.value.play()
        music_play.value = true
    }
    video_player.value.volume = parseFloat(upload_video_form.video_volumn)
    video_player.value.play()
}

const endPreview = () => {
    if (music_player.value) {
        music_player.value.pause()
    }
}

const pausePreview = () => {
    if (music_player.value) {
        music_player.value.pause()
        music_play.value = false
    }
}

const playPreview = () => {
    if (music_player.value) {
        music_player.value.play()
        music_play.value = true
    }
}

</script>

<template>
    <div class="creator">
        <div class="creator_tag">
            <button class="creator_tag_item creator_active_tag" @click="active_tab('video')">{{ store.translate("creator",
                "c_video") }}</button>
            <button class="creator_tag_item" @click="active_tab('music')">{{ store.translate("creator", "c_music")
            }}</button>
            <button class="creator_tag_item" @click="active_tab('manager')">{{ store.translate("creator",
                "manager") }}</button>
        </div>
        <div class="creator_board">
            <div class="creator_board_item" id="creator_video" v-if="active_bar.create_video">
                <div class="creator_board_item_left">
                    <video class="video_preveiw_creator" ref="video_player" v-if="preveiw.video" :src="preveiw.video"
                        @ended="endPreview" @pause="pausePreview" @play="playPreview" controls></video>
                    <label class="text normal_color fs_15 poiter" v-else for="upload_video_creator">{{
                        store.translate("creator", "no") }}</label>
                    <label class="change_video_upload button" for="upload_video_creator" v-if="preveiw.video">{{
                        store.translate("profile", "change") }}</label>
                </div>

                <div class="creator_board_item_right">
                    <form @submit.prevent="submit_upload_video">
                        <p class="text normal_color fs_15">{{ store.translate("creator", "des") }}</p>
                        <input type="text" class="input mg_l_10" :placeholder="store.translate('creator', 'des')"
                            v-model="upload_video_form.descrip">
                        <input type="file" id="upload_video_creator" accept="video/*" @change="upload_video"
                            style="display: none;">

                        <p class="text normal_color fs_15">{{ store.translate("creator", "music") }}</p>
                        <div v-if="upload_video_form.music" class="display_flex gap10 mg_l_10">
                            <div class="music_select_preview">
                                <img class="profile_avatar_music_list"
                                    :src="store.domain + upload_video_form.music.user_infor.avatar">
                                <audio ref="music_player" :src="store.domain + upload_video_form.music.music"
                                    style="display: none;" @ended="music_play = true; music_player.play()" @play="music_play = true"></audio>
                                <font-awesome-icon :icon="['fas', 'pause']" class="icon_25 white" id="btnPlayPause_creator"
                                    v-if="music_play" @click="handle_music()" />
                                <font-awesome-icon :icon="['fas', 'play']" class="icon_25 white" id="btnPlayPause_creator"
                                    v-else @click="handle_music()" />
                            </div>
                            <div>
                                <p class="normal_text normal_color fs_15">{{ upload_video_form.music.name }}</p>
                                <p class="button fs_13 mg_t_10" @click="remove_music">{{ store.translate("comment",
                                    "remove") }}</p>
                            </div>
                        </div>
                        <div v-else class="display_flex align_center gap10 mg_l_10">
                            <p class="normal_text normal_color fs_13">{{ store.translate("creator", "used_music") }}</p>
                            <p class="button fs_13" @click="get_music_list">{{ store.translate("creator", "select_music") }}
                            </p>
                        </div>

                        <div class="display_flex_column gap10 mg_l_10">
                            <div class="display_flex gap10 align_center" v-if="upload_video_form.music">
                                <p class="text normal_color fs_15">{{ store.translate("creator", "music_volumn") }}</p>
                                <input type="range" id="volume-bar" min="0" max="1" step="0.1"
                                    v-model="upload_video_form.music_volumn">
                            </div>
                            <div class="display_flex gap10 align_center" v-if="upload_video_form.video">
                                <p class="text normal_color fs_15">{{ store.translate("creator", "video_volumn") }}</p>
                                <input type="range" id="volume-bar" min="0" max="1" step="0.1"
                                    v-model="upload_video_form.video_volumn">
                            </div>
                        </div>

                        <div class="display_flex gap10 align_center">
                            <p class="text normal_color fs_15">{{ store.translate("creator", "public") }}</p>
                            <input type="checkbox" v-model="upload_video_form.public">
                        </div>
                        <div class="display_flex align_center gap10">
                            <button type="submit">{{ store.translate("profile", "submit") }}</button>
                            <label class="button fs_13" v-if="upload_video_form.video" @click="preview_video">{{
                                store.translate("creator", "preview") }}</label>
                        </div>
                    </form>

                    <div class="music_list" v-if="show_music_list" v-on-click-outside="close_popup">
                        <div class="music_list_board" v-if="music_list.length > 0" v-on:scroll="loadMoreMusic_list">
                            <div v-for="music in music_list" :key="music.id" @click="select_music(music)"
                                class="music_list_item">
                                <img class="profile_avatar_music_list" :src="store.domain + music.user_infor.avatar">
                                <div>
                                    <p class="text normal_color fs_15">{{ music.name }}</p>
                                    <p class="normal_text normal_color fs_13">{{ music.video_count }}
                                        {{ store.translate("music", "used") }}</p>
                                </div>
                            </div>
                        </div>
                        <div class="music_list_board" v-else>
                            <p class="text normal_color fs_15">{{ store.translate("creator", "no") }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="creator_board_item" id="creator_music" v-if="active_bar.create_music">
                <form @submit.prevent="submit_upload_music">
                    <p class="text normal_color fs_15">{{ store.translate("creator", "name") }}</p>
                    <input type="text" class="input mg_l_10" :placeholder="store.translate('creator', 'name')"
                        v-model="upload_music_form.name">
                    <input type="file" id="upload_music_creator" accept="audio/mp3" @change="upload_music"
                        style="display: none;">

                    <p class="text normal_color fs_15">{{ store.translate("creator", "music") }}</p>
                    <div v-if="preveiw.music" class="display_flex gap10 align_center mg_l_10">
                        <audio :src="preveiw.music" controls></audio>
                        <p class="button fs_13">{{ store.translate("profile", "change") }}</p>
                    </div>
                    <div class="display_flex gap10 align_center mg_l_10" v-else>
                        <p class="normal_text normal_color fs_13">{{ store.translate("creator", "preview_music") }}</p>
                        <label class="button fs_13" for="upload_music_creator">{{ store.translate("creator",
                            "upload") }}</label>
                    </div>

                    <button type="submit">{{ store.translate("profile", "submit") }}</button>
                </form>
            </div>

            <div class="creator_board_item" id="creator_manager" v-if="active_bar.manager">
                <div class="creator_manager_left">
                    <p class="text normal_color fs_17">{{ store.translate("creator", "video") }}</p>
                    <div class="my_video" v-on:scroll="loadMoreVideo">
                        <div class="my_video_item" v-for="video in my_video_list" :key="video.id">
                            <video class="video_manager" :src="store.domain + video.video" />
                            <div class="display_flex_column gap5">
                                <p class="normal_text normal_color fs_15">{{ video.descrip }}</p>
                                <div class="display_flex align_center gap10">
                                    <div class="display_flex align_center gap5 poiter">
                                        <font-awesome-icon :icon="['fas', 'heart']" class="icon_15 normal_color" />
                                        <p class="normal_text normal_color fs_13">{{ video.like_count }}</p>
                                    </div>

                                    <div class="display_flex align_center gap5 poiter">
                                        <font-awesome-icon :icon="['fas', 'message']" class="icon_15 normal_color" />
                                        <p class="normal_text normal_color fs_13">{{ video.comment_count }}</p>
                                    </div>

                                    <div class="display_flex align_center gap5 poiter">
                                        <font-awesome-icon :icon="['fas', 'star']" class="icon_15 normal_color" />
                                        <p class="normal_text normal_color fs_13">{{ video.save_count }}</p>
                                    </div>

                                    <div class="display_flex align_center gap5 poiter">
                                        <font-awesome-icon :icon="['fas', 'eye']" class="icon_15 normal_color" />
                                        <p class="normal_text normal_color fs_13">{{ video.view }}</p>
                                    </div>
                                </div>
                            </div>
                            <div>
                                <p class="normal_text normal_color fs_13" v-if="video.public">{{ store.translate("creator",
                                    "public") }}</p>
                                <p class="normal_text normal_color fs_13" v-else>{{ store.translate("creator", "private") }}
                                </p>
                                <p class="normal_text normal_color fs_13">{{ video.create_time }} {{
                                    store.translate("creator",
                                        "duration") }}</p>
                            </div>

                            <div class="display_flex gap10 justify_right">
                                <router-link class="button fs_13 no_decor"
                                    :to="{ name: 'video', params: { id: video.id } }">{{ store.translate("search",
                                        "view") }}</router-link>
                                <button @click="delete_video(video.id)">{{ store.translate("comment", "remove") }}</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="creator_manager_right">
                    <p class="text normal_color fs_17">{{ store.translate("creator", "music") }}</p>
                    <div class="my_music" v-on:scroll="loadMoreMusic">
                        <div class="my_music_item" v-for="music in my_music_list" :key="music.id">
                            <img class="profile_avatar_music" :src="store.domain + music.user_infor.avatar">
                            <div>
                                <p class="normal_text normal_color fs_15">{{ music.name }}</p>
                            </div>
                            <div>
                                <p class="normal_text normal_color fs_13">{{ music.video_count }} {{
                                    store.translate("music",
                                        "used") }}</p>
                                <p class="normal_text normal_color fs_13">{{ music.create_time }} {{
                                    store.translate("creator",
                                        "duration") }}</p>
                            </div>
                            <div class="display_flex gap10 justify_right">
                                <router-link class="button fs_13 no_decor"
                                    :to="{ name: 'music', params: { id: music.id } }">{{ store.translate("search",
                                        "view") }}</router-link>
                                <button @click="delete_music(music.id)">{{ store.translate("comment", "remove") }}</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
.creator {
    width: 98%;
    height: 99%;
    display: flex;
    flex-direction: column;
    gap: 15px;
    padding: 10px;
}

.creator_tag {
    display: flex;
    gap: 5px;
    width: 100%;
}

.creator_active_tag {
    background: var(--hover_color);
}

.creator_board {
    width: 100%;
    height: 94%;
    background: var(--background_video);
    border-radius: 10px;
}

.creator_board_item {
    padding: 10px;
    width: 98%;
    height: 97%;
    position: relative;
}

#creator_video {
    display: flex;
    gap: 10px;
}

.creator_board_item_left {
    width: 60%;
    height: 100%;
    display: grid;
    place-items: center;
    background: var(--hover_color);
    border-radius: 10px;
    position: relative;
}

.video_preveiw_creator {
    width: 100%;
}

.change_video_upload {
    position: absolute;
    bottom: 10px;
}

.creator_board_item_right {
    width: 40%;
    height: 100%;
    display: flex;
    flex-direction: column;
    background: var(--hover_color);
    border-radius: 10px;
    position: relative;
}

.creator_board_item_right form {
    padding: 20px;
    width: 90%;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.music_select_preview {
    width: 80px;
    height: 80px;
    position: relative;
    display: grid;
    place-items: center;
}

#btnPlayPause_creator {
    position: absolute;
    z-index: 50;
}

.music_list {
    position: absolute;
    background: var(--background_popup_color);
    padding: 10px;
    border-radius: 10px;
    box-shadow: 0 0 2px var(--boder_color);
    left: 10px;
    top: 10px;
    width: max-content;
    height: 400px;
}

.music_list_board {
    width: max-content;
    height: 100%;
    overflow-y: scroll;
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.music_list_board::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}

.music_list_board::-webkit-scrollbar-track {
    background: transparent !important;
}

.music_list_board::-webkit-scrollbar-thumb {
    background: var(--scroll_color);
    border-radius: 5px;
}

.music_list_item {
    border-radius: 5px;
    display: flex;
    gap: 10px;
    cursor: pointer;
    padding: 5px 10px;
}

.music_list_item:hover {
    background: var(--hover_color);
}

#creator_music form {
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

#creator_manager {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.creator_manager_left {
    height: 49%;
    width: 100%;
    overflow: hidden;
}

.my_video {
    height: 90%;
    overflow-y: scroll;
}

.my_video::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}

.my_video::-webkit-scrollbar-track {
    background: transparent !important;
}

.my_video::-webkit-scrollbar-thumb {
    background: var(--scroll_color);
    border-radius: 5px;
}

.my_video_item {
    display: grid;
    grid-template-columns: 100px 200px 200px auto;
    border-radius: 10px;
    padding: 10px;
    align-items: center;
    gap: 50px;
}

.my_video_item:hover {
    background: var(--hover_color);
}


.creator_manager_right {
    width: 100%;
    height: 49%;
    overflow: hidden;
}

.my_music {
    height: 93%;
    overflow-y: scroll;
}

.my_music::-webkit-scrollbar {
    width: 5px;
    height: 5px;
}

.my_music::-webkit-scrollbar-track {
    background: transparent !important;
}

.my_music::-webkit-scrollbar-thumb {
    background: var(--scroll_color);
    border-radius: 5px;
}

.my_music_item {
    display: grid;
    grid-template-columns: 100px 200px 200px auto;
    border-radius: 10px;
    padding: 10px;
    align-items: center;
    gap: 50px;
}

.my_music_item:hover {
    background: var(--hover_color);
}
</style>