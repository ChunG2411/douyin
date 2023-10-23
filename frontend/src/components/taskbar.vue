<script setup>
import AuthenComponent from './authen.vue'
import { Store } from '../assets/store'

import { vOnClickOutside } from '@vueuse/components'
import { ref, onMounted } from "vue"

const store = Store()
const taskbar_item = ref(null)

const show_login_popup = ref(false)

const close_popup = [() => {
  show_login_popup.value = !show_login_popup.value
}]


const changeActive = () => {
  taskbar_item.value.forEach(item => {
    item.classList.remove('active_taskbar')
  })
}


onMounted(() => {
  taskbar_item.value = document.querySelectorAll('.taskbar_item')

  taskbar_item.value.forEach(item => {
    item.addEventListener('click', () => {
      changeActive()
      item.classList.add('active_taskbar')
    })
  })
})

</script>

<template>
  <div class="taskbar">
    <div class="taskbar_item active_taskbar">
      <font-awesome-icon :icon="['fas', 'house']" class="icon white icon_margin_right" />
      <router-link class="text normal_color" to="/">home</router-link>
    </div>

    <router-link class="taskbar_item no_decor" to="/followed" v-if="store.is_login">
      <font-awesome-icon :icon="['fas', 'star']" class="icon white icon_margin_right" />
      <p class="text normal_color">followed</p>
    </router-link>

    <div class="taskbar_item" v-else @click="show_login_popup = !show_login_popup">
      <font-awesome-icon :icon="['fas', 'star']" class="icon white icon_margin_right" />
      <p class="text normal_color">followed</p>
    </div>

    <router-link class="taskbar_item no_decor" v-if="store.is_login" to="/profile/self">
      <font-awesome-icon :icon="['fas', 'user']" class="icon white icon_margin_right" />
      <p class="text normal_color">profile</p>
    </router-link>

    <div class="taskbar_item" v-else @click="show_login_popup = !show_login_popup">
      <font-awesome-icon :icon="['fas', 'user']" class="icon white icon_margin_right" />
      <p class="text normal_color">profile</p>
    </div>
  </div>

  <div class="popup" v-if="show_login_popup">
    <AuthenComponent v-on-click-outside="close_popup" />
  </div>
</template>

<style>
.taskbar {
  position: fixed;
  margin-top: 55px;
  margin-left: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  width: 110px;
  z-index: 10;
  padding: 5px;
  background: var(--background_color);
}

.taskbar_item {
  width: 100%;
  height: 35px;
  font-weight: 500;
  border-radius: 5px;
  margin-bottom: 5px;
  cursor: pointer;
  display: flex;
  place-items: center;
  justify-content: left;
}

.taskbar_item:hover {
  background: var(--hover_color);
}

.active_taskbar {
  background: var(--hover_color);
}

.icon_margin_right {
  margin-right: 10px;
  padding-left: 10px;
}
</style>