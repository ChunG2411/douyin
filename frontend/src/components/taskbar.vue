<script setup>
import AuthenComponent from './authen.vue'
import { vOnClickOutside } from '@vueuse/components'

import { reactive, inject, ref } from "vue"

const user_localstore = inject("user_localstore")
const show_login_popup = ref(false)

const close_popup = [() => {
    show_login_popup.value = !show_login_popup.value
}]

</script>

<template>
  <div class="taskbar">
    <router-link to="/">home</router-link>

    <router-link :to="{ name: 'profile', params: { username: user_localstore.user['username'] } }"
      v-if="user_localstore.is_authen">
      profile
    </router-link>
    <button v-else @click="show_login_popup = !show_login_popup">profile</button>

    <router-link :to="{ name: 'profile', params: { username: 'chung' } }">chung</router-link>
  </div>

  <div class="popup" v-if="show_login_popup">
    <AuthenComponent v-on-click-outside="close_popup" />
  </div>
</template>

<style>
.taskbar {
  position: fixed;
  margin-top: 0;
  margin-left: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.popup {
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
</style>