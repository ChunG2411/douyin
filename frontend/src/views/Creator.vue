<script setup>
import { Store } from '../assets/store'

import { ref, reactive, watch } from 'vue'
import axios from 'axios'
import { vOnClickOutside } from '@vueuse/components'


const store = Store()

const upload_video_form = reactive({
    descrip: '',
    video: '',
    use_video_music: '1',
    music: '',
    puclic: false
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
}

const submit_upload_video = () => {
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
    form.append('public', upload_video_form.public)

    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.post(`${store.domain}/api/user/${localStorage.getItem('username')}/video`, form, header)
        .then(response => {
            store.msg_success = "Create successful."
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
                    my_video_list.value.pop(my_video_list.value[i])
                }
            }
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
    const form = new FormData()
    form.append('name', upload_music_form.name)
    form.append('music', upload_music_form.music)

    const header = {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    }
    axios.post(`${store.domain}/api/music`, form, header)
        .then(response => {
            store.msg_success = "Create successful."
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
                    my_music_list.value.pop(my_music_list.value[i])
                }
            }
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

</script>

<template>
    <div class="creator">
        <div>
            <p @click="active_tab('video')">create video</p>
            <p @click="active_tab('music')">create music</p>
            <p @click="active_tab('manager')">manager</p>
        </div>
        <div>
            <div v-if="active_bar.create_video">
                <form @submit.prevent="submit_upload_video">
                    <input type="text" v-model="upload_video_form.descrip">
                    <input type="file" accept="video/*" @change="upload_video">

                    <div v-if="preveiw.video">
                        <video :src="preveiw.video" controls></video>
                    </div>

                    <div v-if="upload_video_form.music">
                        <img class="profile_avatar_music_list"
                            :src="store.domain + upload_video_form.music.user_infor.avatar">
                        <p>{{ upload_video_form.music.name }}</p>
                        <label @click="remove_music">remove</label>
                    </div>
                    <div v-else>
                        <label @click="get_music_list">music</label>
                    </div>
                    <input type="checkbox" v-model="upload_video_form.public">
                    
                    <button type="submit">Submit</button>
                </form>

                <div v-if="show_music_list" v-on-click-outside="close_popup">
                    <div v-for="music in music_list" :key="music.id" @click="select_music(music)"
                        v-if="music_list.length > 0">
                        <img class="profile_avatar_music_list" :src="store.domain + music.user_infor.avatar">
                        <p>{{ music.name }}</p>
                        <small>{{ music.video_count }}</small>
                    </div>
                    <div v-else>
                        <p>Don't have any music</p>
                    </div>
                </div>
            </div>

            <div v-if="active_bar.create_music">
                <form @submit.prevent="submit_upload_music">
                    <input type="text" v-model="upload_music_form.name">
                    <input type="file" accept="audio/mp3" @change="upload_music">

                    <div v-if="preveiw.music">
                        <audio :src="preveiw.music" controls></audio>
                    </div>

                    <button type="submit">Submit</button>
                </form>
            </div>

            <div v-if="active_bar.manager">
                <div>
                    <b>video</b>
                    <div v-for="video in my_video_list" :key="video.id">
                        <video class="video_manager" :src="store.domain + video.video" />
                        <p>{{ video.descrip }}</p>
                        <div>
                            <small v-if="video.public">Public</small>
                            <small v-else>Private</small>
                            <small>{{ video.create_time }}</small>
                        </div>
                        <div>
                            <p>{{ video.like_count }}</p>
                            <p>{{ video.comment_count }}</p>
                            <p>{{ video.save_count }}</p>
                        </div>
                        <div>
                            <router-link :to="{ name: 'video', params: { id: video.id } }">
                                <button>View</button>
                            </router-link>
                            <button @click="delete_video(video.id)">Delete</button>
                        </div>
                    </div>
                </div>
                <div>
                    <b>music</b>
                    <div v-for="music in my_music_list" :key="music.id">
                        <img class="profile_avatar_music" :src="store.domain + music.user_infor.avatar">
                        <p>{{ music.name }}</p>
                        <div>
                            <small>{{ music.create_time }}</small>
                        </div>
                        <div>
                            <p>{{ music.video_count }} used</p>
                        </div>
                        <div>
                            <router-link :to="{ name: 'music', params: { id: music.id } }">
                                <button>View</button>
                            </router-link>
                            <button @click="delete_music(music.id)">Delete</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>