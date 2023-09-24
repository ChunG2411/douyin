<script setup>
import HeaderComponent from '../components/header.vue'
import TaskbarComponent from '../components/taskbar.vue'

import { provide, reactive } from 'vue'

const user_store = reactive({
    user: JSON.parse(localStorage.getItem('user')),
    is_authen: (localStorage.getItem('user') === null) ? false : true
})

provide("user_store", user_store)

</script>

<template>
    <HeaderComponent />
    <TaskbarComponent />

    <div class="home">
        <p>home page</p>
    </div>
</template>

