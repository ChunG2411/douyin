<script setup>
import TaskbarComponent from './components/taskbar.vue'
import HeaderComponent from './components/header.vue'


</script>

<template>
  <HeaderComponent/>
  <TaskbarComponent/>

  <div class="main">
    <router-view></router-view>
  </div>
</template>

<style>
.main{
  top: 60px;
  left: 120px;
  position: relative;
  background: var(--background_color);
  width: 100vw;
  height: 100vh;
}
</style>