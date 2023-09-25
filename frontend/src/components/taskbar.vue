<script setup>
import { reactive, inject } from "vue"

const user_localstore = inject("user_localstore")


</script>

<template>
  <div class="taskbar">
    <router-link to="/">home</router-link>
    <!-- <router-link :to="'/profile/' + user_localstore.user['username']" v-if="user_localstore.is_authen">profile</router-link>
    <router-link :to="'/profile/chung'" v-if="user_localstore.is_authen">profile</router-link>
    <button v-else>profile</button> -->
    <router-link :to="{name: 'profile', params: {username: user_localstore.user['username']}}">admin</router-link>
    <router-link :to="{name: 'profile', params: {username: 'chung'}}">chung</router-link>
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
</style>