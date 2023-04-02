<script>
    export default {
        props: {
            'idx': {
                type: Number,
                default: null
            }
        },
        methods: {
            add (block, model_name) {
                this.$parent.show_add_block = false
                this.$parent.hover = false
                this.$root.addNewBlock(block, model_name, this.idx)
            }
        }
    }
</script>
<template>
    <ul class="stream-blocks-list">
        <li v-for="(block, model_name) in $root.model_info">
            <a class="stream-btn" href="#" v-text="'+ ' + block.model_doc" @click.prevent.stop="add(block, model_name)"></a>
        </li>
    </ul>
</template>
