<script setup>
import AuthenComponent from './authen.vue'
import { Store } from '../assets/store'

import { vOnClickOutside } from '@vueuse/components'
import { ref } from "vue"

const store = Store()

const show_login_popup = ref(false)

const close_popup = [() => {
  show_login_popup.value = !show_login_popup.value
}]

</script>

<template>
  <div class="taskbar">
    <router-link to="/">home</router-link>

    <router-link to="/followed" v-if="store.is_login">followed</router-link>
    <button v-else @click="show_login_popup = !show_login_popup">followed</button>

    <router-link to="/profile/self" v-if="store.is_login">profile</router-link>
    <button v-else @click="show_login_popup = !show_login_popup">profile</button>

    <router-link :to="{ name: 'guest_profile', params: { username: 'chung' } }">chung</router-link>
    <router-link :to="{ name: 'guest_profile', params: { username: 'chung1' } }">chung1</router-link>

  </div>

  <div class="popup" v-if="show_login_popup">
    <AuthenComponent v-on-click-outside="close_popup" />
  </div>
</template>

<style>
.taskbar {
  position: fixed;
  margin-top: 50px;
  margin-left: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  z-index: 50;
}
</style>