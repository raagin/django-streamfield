<script>
    import BlockHeader from '@/components/BlockHeader.vue'
    import BlockOptions from '@/components/BlockOptions.vue'
    import AddBlockHere from '@/components/AddBlockHere.vue'

    export default {
        props: ['block'],
        data () {
            return {
                model_name_lower: this.block.model_name.toLowerCase()
            }
        },
        components: { BlockOptions, BlockHeader, AddBlockHere },
        beforeMount: function() {
            this.getContent();
        },
        methods: {
            render_url: function(block) {
                return '/streamfield/abstract-block/' + this.model_name_lower + '/';
            },
            getContent() {
                let block = _.find(this.$root.stream, ['unique_id', this.block.unique_id]);
                window.ax.get(this.render_url(this.block)).then((response) => {
                    this.$root.blocks[this.block.model_name] = response.data;
                });
            }
        }
    }
</script>
<template>
<div class="stream-model-block" :class="{ 'collapsed': block.collapsed }">
    <div class="stream-model-block__inner">
        <BlockHeader :block="block" />
        <div class="stream-model-block__content no-subblocks abstract-block"
            :class="model_name_lower">
            <span v-html="$root.blocks[this.block.model_name]"></span>
        </div>
        <BlockOptions :block="block" />
    </div>
    <AddBlockHere :block="block" />
</div>
</template>