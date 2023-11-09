<script setup>
import TaskbarComponent from './components/taskbar.vue'
import HeaderComponent from './components/header.vue'
import { Store } from './assets/store.js'

import { watch, ref } from 'vue'
import axios from 'axios'


const store = Store()

const show_popup = ref(false)

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
watch(() => store.lang, (currentvalue, oldvalue) => {
  show_popup.value = true
  api_change_setup()
  setTimeout(() => {
    show_popup.value = false
  }, 5000)
})
watch(() => store.theme, (currentvalue, oldvalue) => {
  show_popup.value = true
  api_change_setup()
  setTimeout(() => {
    show_popup.value = false
  }, 5000)
})


const api_change_setup = () => {
  const header = {
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
  }

  const form = new FormData()
  form.append('lang', store.lang)
  form.append('theme', store.theme)

  axios.put(`${store.domain}/api/setup`, form, header)
    .then(response => {
      localStorage.setItem('lang', store.lang)
      localStorage.setItem('theme', store.theme)
      change_theme(store.theme)
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

const change_theme = (type) => {
  if (type=="light") {
    document.documentElement.style.setProperty('--background_color', '#fafafa')
    document.documentElement.style.setProperty('--background_popup_color', '#ebebeb')
    document.documentElement.style.setProperty('--text_color', '#000000')
    document.documentElement.style.setProperty('--hover_color', '#b3b3b3a2')
    document.documentElement.style.setProperty('--scroll_color', '#c4c2c2')
    document.documentElement.style.setProperty('--boder_color', '#595959')
    document.documentElement.style.setProperty('--background_video', '#ebebeb')
    document.documentElement.style.setProperty('.normal_color', '#000000')
  }
  else {
    document.documentElement.style.setProperty('--background_color', '#161823')
    document.documentElement.style.setProperty('--background_popup_color', '#232430')
    document.documentElement.style.setProperty('--text_color', 'rgb(233, 233, 233)')
    document.documentElement.style.setProperty('--hover_color', '#444444a2')
    document.documentElement.style.setProperty('--scroll_color', '#555555')
    document.documentElement.style.setProperty('--boder_color', '#ababab')
    document.documentElement.style.setProperty('--background_video', '#1d1f2e')
    document.documentElement.style.setProperty('.normal_color', 'rgb(212, 212, 212)')
  }
}
change_theme(localStorage.getItem('theme'))

</script>

<template>
  <HeaderComponent />
  <TaskbarComponent />

  <div class="main">
    <router-view></router-view>
  </div>

  <div class="msg_tag" v-if="store.msg_error || store.msg_success || store.noti || store.chat || show_popup">
    <div class="msg_tag_item" v-if="store.msg_error">
      <div id="error"></div>

      <div class="tag_content">
        <p class="text normal_color fs_15">{{ store.translate("msg", "error") }}</p>
        <p class="normal_text normal_color fs_13">{{ store.msg_error }}</p>
      </div>
    </div>

    <div class="msg_tag_item" v-if="store.msg_success">
      <div id="success"></div>

      <div class="tag_content">
        <p class="text normal_color fs_15">{{ store.translate("msg", "success") }}</p>
        <p class="normal_text normal_color fs_13">{{ store.msg_success }}</p>
      </div>
    </div>

    <div class="msg_tag_item" v-if="store.noti">
      <div id="noti"></div>

      <div class="tag_content">
        <p class="text normal_color fs_15">{{ store.translate("noti", "noti") }}</p>
        <p class="normal_text normal_color fs_13" v-if="store.noti.user_interact.split(',').length - 1 > 0">{{
          store.noti.context }} {{ store.translate("noti", "and") }} {{ store.noti.user_interact.split(",").length - 1 }}
          {{ store.translate("noti", "other") }}</p>
        <p class="normal_text normal_color fs_13" v-else>{{ store.noti.context }}</p>
        <p class="normal_text normal_color fs_13" v-if="store.noti.type == '1'">{{ store.translate("noti", "like_video")
        }}</p>
        <p class="normal_text normal_color fs_13" v-else-if="store.noti.type == '2'">{{ store.translate("noti",
          "cmt_video") }}</p>
        <p class="normal_text normal_color fs_13" v-else-if="store.noti.type == '3'">{{ store.translate("noti",
          "like_cmt") }}</p>
        <p class="normal_text normal_color fs_13" v-else-if="store.noti.type == '4'">{{ store.translate("noti", "cmt_cmt")
        }}</p>
        <p class="normal_text normal_color fs_13" v-else-if="store.noti.type == '5'">{{ store.translate("noti", "follow")
        }}</p>
      </div>
    </div>

    <div class="msg_tag_item" v-if="store.chat">
      <div id="chat"></div>

      <div class="tag_content">
        <p class="text normal_color fs_15">{{ store.translate("header", "chat") }}</p>
        <p class="normal_text normal_color fs_13">{{ store.chat.receiver.name }}: {{ store.chat.text }}</p>
      </div>
    </div>

    <div class="msg_tag_item" v-if="show_popup">
      <div class="tag_content">
        <p class="text normal_color fs_15">{{ store.translate("msg", "change") }}</p>
      </div>
    </div>

  </div>
</template>

<style>
.main {
  top: 60px;
  left: 125px;
  position: relative;
  background: var(--background_color);
  width: calc(100vw - 125px);
  height: calc(100vh - 60px);
  overflow: hidden;
  min-width: 500px;
  min-height: 500px;
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