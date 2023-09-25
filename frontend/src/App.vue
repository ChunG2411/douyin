<script setup>
import HeaderComponent from './components/header.vue'
import TaskbarComponent from './components/taskbar.vue'

import { reactive, provide } from "vue"

const user_localstore = reactive({
    user: JSON.parse(localStorage.getItem('user')),
    is_authen: (localStorage.getItem('user') === null) ? false : true
})

provide("user_localstore", user_localstore)

</script>

<template>
  <HeaderComponent/>
  <TaskbarComponent/>

  <div class="main">
    <router-view></router-view>
  </div>
</template>
