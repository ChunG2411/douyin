<script setup>
import TaskbarComponent from './components/taskbar.vue'
import HeaderComponent from './components/header.vue'
import { Store } from './assets/store.js'

import { watch } from 'vue'

const store = Store()

watch(() => store.msg_error, (currentvalue, oldvalue) => {
  if (currentvalue) {
    setTimeout(() => {
      store.msg_error = null
    }, 5000)
  }
})
watch(() => store.msg_success, (currentvalue, oldvalue) => {
  if (currentvalue) {
    setTimeout(() => {
      store.msg_success = null
    }, 5000)
  }
})
watch(() => store.noti, (currentvalue, oldvalue) => {
  if (currentvalue) {
    setTimeout(() => {
      store.noti = null
    }, 5000)
  }
})
watch(() => store.chat, (currentvalue, oldvalue) => {
  if (currentvalue) {
    setTimeout(() => {
      store.chat = null
    }, 5000)
  }
})

</script>

<template>
  <HeaderComponent />
  <TaskbarComponent />

  <div class="main">
    <router-view></router-view>
  </div>

  <div class="msg_tag" v-if="store.msg_error || store.msg_success || store.noti || store.chat">
    <div class="msg_tag_item" v-if="store.msg_error">
      <div id="error"></div>

      <div class="tag_content">
        <p class="text normal_color fs_15">Error</p>
        <p class="normal_text normal_color fs_13">{{ store.msg_error }}</p>
      </div>
    </div>

    <div class="msg_tag_item" v-if="store.msg_success">
      <div id="success"></div>

      <div class="tag_content">
        <p class="text normal_color fs_15">Success</p>
        <p class="normal_text normal_color fs_13">{{ store.msg_success }}</p>
      </div>
    </div>

    <div class="msg_tag_item" v-if="store.noti">
      <div id="noti"></div>

      <div class="tag_content">
        <p class="text normal_color fs_15">Notification</p>
        <p class="normal_text normal_color fs_13" v-if="store.noti.user_interact.split(',').length - 1 > 0">{{
          store.noti.context }} and {{ store.noti.user_interact.split(",").length - 1 }}
          other people</p>
        <p class="normal_text normal_color fs_13" v-else>{{ store.noti.context }}</p>
        <p class="normal_text normal_color fs_13" v-if="store.noti.type == '1'">liked your video</p>
        <p class="normal_text normal_color fs_13" v-else-if="store.noti.type == '2'">commented your video</p>
        <p class="normal_text normal_color fs_13" v-else-if="store.noti.type == '3'">liked your comment</p>
        <p class="normal_text normal_color fs_13" v-else-if="store.noti.type == '4'">commented your comment</p>
        <p class="normal_text normal_color fs_13" v-else-if="store.noti.type == '5'">followed you</p>
      </div>
    </div>

    <div class="msg_tag_item" v-if="store.chat">
      <div id="chat"></div>

      <div class="tag_content">
        <p class="text normal_color fs_15">Chat</p>
        <p class="normal_text normal_color fs_13">{{ store.chat.receiver.name }}: {{ store.chat.text }}</p>
      </div>
    </div>

  </div>
</template>

<style>
.main {
  top: 65px;
  left: 125px;
  position: relative;
  background: var(--background_color);
  width: 100vw;
  height: 100vh;
}

.msg_tag {
  position: absolute;
  width: 200px;
  height: max-content;
  bottom: 10px;
  right: 10px;
  z-index: 70;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.msg_tag_item {
  background: var(--background_popup_color);
  border-radius: 5px;
  box-shadow: 0 0 2px var(--boder_color);
  overflow: hidden;
  width: 100%;
  height: max-content;
  position: relative;
}

#error {
  width: 100%;
  height: 5px;
  background: var(--error_msg_color);
}

#success {
  width: 100%;
  height: 5px;
  background: var(--success_msg_color);
}

#noti {
  width: 100%;
  height: 5px;
  background: var(--noti_msg_color);
}

#chat {
  width: 100%;
  height: 5px;
  background: var(--chat_msg_color);
}

.tag_content {
  padding: 10px 10px 15px 10px;
}
</style>