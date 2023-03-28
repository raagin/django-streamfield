<script>
    import BlockList from '@/components/BlockList.vue'

    let st;
    export default {
        props: ['block'],
        components: { BlockList },
        data () {
            return {
                hover: false,
                show_add_block: false
            }
        },
        methods: {
            show () {
                st = setTimeout( () => {
                    this.hover=true
                }, 500)
            },
            hide () {
                clearTimeout(st)
                this.hover = false
            },
            get_index () {
                let [idx] = this.$root.getBlockIndex(this.block.unique_id)
                return idx + 1
            },
            hideAddBlock () {
                this.show_add_block = false
                this.hide()
            }
        }
    }
</script>
<template>
    <div class="add_here" :class="{'show': hover, show_add_block }" @mouseover="show" @mouseout="hide" @click="show_add_block=!show_add_block">
        <BlockList v-if="show_add_block" :idx="get_index()"  @hide_add_block="hideAddBlock"/>
    </div>
</template>