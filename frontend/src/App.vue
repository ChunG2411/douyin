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
  top: 50px;
  left: 50px;
  position: relative;
}
</style>