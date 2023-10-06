<script setup>
import CommentItem from './comment_item.vue'
import { defineProps } from 'vue'

const props = defineProps({
    data: String
})
</script>

<template>
    <CommentItem :data="props.data"/>
</template>