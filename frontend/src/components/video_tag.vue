<script setup>
import { defineProps, ref, onMounted } from 'vue'

const props = defineProps({
    src: String
})

const player = ref(null)
const btnPlayPause = ref(null)
const btnMute = ref(null)
const progressBar = ref(null)
const volumeBar = ref(null)

const curtime = ref('00:00')
const durtime = ref('00:00')

const video_play = ref(true)
const video_mute = ref(true)


onMounted(() => {
    player.value = document.getElementById('video-element')
    btnPlayPause.value = document.getElementById('btnPlayPause')
    btnMute.value = document.getElementById('btnMute')
    progressBar.value = document.getElementById('progress-bar')
    volumeBar.value = document.getElementById('volume-bar')

    player.value.addEventListener('click', playPauseVideo)

    volumeBar.value.addEventListener("change", function (evt) {
        player.value.volume = evt.target.value
    })

    player.value.addEventListener('timeupdate', updatetime, false)

    player.value.addEventListener('play', function () {
        video_play.value = false
    }, false)

    player.value.addEventListener('pause', function () {
        video_play.value = true
    }, false)

    player.value.addEventListener('volumechange', function (e) {
        if (player.value.muted) video_mute.value = false
        else video_mute.value = true
    }, false)

    player.value.addEventListener('ended', function () { this.play(); }, false)
})


function playPauseVideo() {
    if (player.value.paused || player.value.ended) {
        player.value.play()
    }
    else {
        player.value.pause()
    }
}

function muteVolume() {
    if (player.value.muted) {
        player.value.muted = false;
    }
    else {
        player.value.muted = true;
    }
}

function updatetime() {
    var percentage = Math.floor((100 / player.value.duration) * player.value.currentTime);
    progressBar.value.value = percentage;
    progressBar.value.innerHTML = percentage + '% played';

    var curmin = Math.floor(player.value.currentTime / 60)
    var cursec = Math.floor(player.value.currentTime - curmin * 60);
    var durmin = Math.floor(player.value.duration / 60)
    var dursec = Math.floor(player.value.duration - durmin * 60);

    if (curmin < 10) {
        curmin = '0' + curmin
    }
    if (cursec < 10) {
        cursec = '0' + cursec
    }
    if (durmin < 10) {
        durmin = '0' + durmin
    }
    if (dursec < 10) {
        dursec = '0' + dursec
    }
    curtime.value = curmin + ':' + cursec
    durtime.value = durmin + ':' + dursec
}

</script>

<template>
    <video class="video" id="video-element" :src="props.src" autoplay></video>
    <div class="controls">
        <progress class="controls_bar mg_b_5" id='progress-bar' min='0' max='100' value='0'>0% played</progress>
        <div class="controls_button">
            <div class="display_flex gap10 align_center">
                <font-awesome-icon :icon="['fas', 'play']" class="icon_15" id="btnPlayPause" v-if="video_play"
                    @click="playPauseVideo()" />
                <font-awesome-icon :icon="['fas', 'pause']" class="icon_15" id="btnPlayPause" v-else
                    @click="playPauseVideo()" />
                <p class="normal_text normal_color fs_15">{{ curtime }} / {{ durtime }}</p>
            </div>
            <div class="display_flex gap10 align_center">
                <input type="range" id="volume-bar" min="0" max="1" step="0.1" value="1">
                <font-awesome-icon :icon="['fas', 'volume-high']" class="icon_15" id="btnMute" @click='muteVolume()'
                    v-if="video_mute" />
                <font-awesome-icon :icon="['fas', 'volume-xmark']" class="icon_15" id="btnMute" @click='muteVolume()'
                    v-else />
            </div>
        </div>
    </div>
</template>

<style>
.video {
    width: 100%;
    height: 100%;
}

.controls {
    position: absolute;
    display: flex;
    flex-direction: column;
    bottom: 5px;
    width: 99%;
    padding: 5px;
}

.controls_bar {
    width: 100%;
    height: 5px;
}

.controls_button {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 95%;
    padding: 0 20px 0 20px;
}

#volume-bar {
    width: 100px;
    height: 5px;
    cursor: pointer;
    overflow: hidden;
    border-radius: 5px;
    background: var(--text_color);
}
</style>