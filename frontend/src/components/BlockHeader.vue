<script>
    export default {
        props: ['block', 'title'],
        methods: {
            headerClick () {
                this.block.collapsed = !this.block.collapsed
            }
        }
    }
</script>
<template>
    <h3 class="streamblock__block__title">
        <span class="streamblock__block__title-click" @click="headerClick"></span>
        <span class="streamblock__block__model_title">{{ $root.model_title(block) }}</span>&nbsp;
        <span v-if="title" class="streamblock__block__subtitle"> &mdash; {{ title }}</span>
        <span class="streamblock__block-handle">
            <span class="block-move"></span>
            <span class="block-delete" @click="$root.deleteBlock(block.unique_id)"></span>
        </span>
    </h3>
</template>