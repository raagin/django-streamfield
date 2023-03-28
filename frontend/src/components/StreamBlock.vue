<script>
    import draggable from 'vuedraggable'
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
        components: { draggable, BlockOptions, BlockHeader, AddBlockHere },
        beforeMount: function() {
            if (_.isArray(this.block.id)) {
                for (var j = this.block.id.length - 1; j >= 0; j--) {
                    this.updateBlock(this.block.id[j].toString());
                }
            } else {
                this.updateBlock(this.block.id.toString());
            }
        },
        methods: {
            instance_unique_id: function(block, instance_id){
                return this.model_name_lower + instance_id;
            },
            instance_admin_render_url: function(block, instance_id) {
                return '/streamfield/admin-instance/' + this.model_name_lower + '/' + instance_id;
            },
            block_admin_url: function(block) {
                return this.$root.base_admin_url + 'streamblocks/' + this.model_name_lower + '/';
            },
            get_change_model_link: function(block, instance_id){
                return this.block_admin_url(block) + instance_id + 
                        '/change/?_popup=1&block_id=' + block.unique_id + 
                        '&instance_id=' + instance_id +
                        '&app_id=' + this.$root.app_node.id;
            },
            getBlockTitle: function(block, item_id) {
                if (!_.isNumber(item_id) && _.isNumber(item_id[0])) {
                    item_id = item_id[0]
                }
                let block_data = this.$root.blocks[this.instance_unique_id(block, item_id)]
                if (block_data && block_data.hasOwnProperty('title')) {
                    return block_data.title    
                } else{
                    return ''
                }
                
            },
            getContent: function(block, item_id) {
                let block_data = this.$root.blocks[this.instance_unique_id(block, item_id)]
                if (!block_data) return
                return block_data.content;
            },
            updateBlock: function(instance_id) {
                if (instance_id == -1) return
                // change block content
                window.ax.get(this.instance_admin_render_url(this.block, instance_id)).then((response) => {
                    this.$root.blocks[this.instance_unique_id(this.block, instance_id)] = response.data;
                });

                // if added new instance – add new instance id to block list
                let instance_id_int = parseInt(instance_id)
                if (_.isArray(this.block.id) &&  this.block.id.indexOf(instance_id_int) == -1) {
                    this.block.id.push(instance_id_int);
                }

                // if added new instance to block without list
                if ( !_.isArray(this.block.id) && this.block.id == -1 ) {
                    this.block.id = instance_id_int;
                }

            },
            get_add_model_link: function(block){
                return this.block_admin_url(block) +
                        'add/?_popup=1&block_id=' + block.unique_id + 
                        '&app_id=' + this.$root.app_node.id;
            },
        }
    }
</script>
<template>
    <div class="stream-model-block" :class="{ 'collapsed': block.collapsed }">
        <div class="stream-model-block__inner">
            <BlockHeader :block="block" :title="getBlockTitle(block, block.id)"/>
            <div>
                <div v-if="$root.isArray(block.id)" 
                    class="stream-model-block__content"
                    :class="block.model_name.toLowerCase()"
                    :id="'id_' + block.unique_id">
                    <draggable v-model="block.id" group="items" handle=".subblock-move" item-key="id">
                        <template #item="{element: item_id}">
                            <span class="stream-model-subblock">
                                <span class="model-field-content"
                                    :id="'id_' + instance_unique_id(block, item_id)" 
                                    v-html="getContent(block, item_id)"
                                    ></span>
                                <span class="stream-model-subblock-handle">
                                    <span class="subblock-move"></span>
                                    <span class="subblock-delete" @click="deleteInstance(block.unique_id, item_id)"></span>
                                </span>
                                <a class="stream-btn" 
                                    :id="'change_id_' + instance_unique_id(block, item_id)" 
                                    :title="$root.stream_texts['Change']" 
                                    :href="get_change_model_link(block, item_id)"
                                    :data-block="block.unique_id"
                                    :data-instance-id="item_id"
                                    @click.prevent="$root.openPopup"
                                    v-text="$root.stream_texts['Change']"
                                    ></a>
                                    &nbsp;

                            </span>
                        </template>
                    </draggable>
                    <a class="stream-btn" 
                        :id="'add_id_' + block.unique_id"
                        :title="$root.stream_texts['AddOneMore']"
                        :href="get_add_model_link(block)"
                        @click.prevent="$root.openPopup"
                        v-text="'+ ' + $root.stream_texts['AddOneMore']"
                        ></a>
                </div>
                <div v-else
                    class="stream-model-block__content no-subblocks"
                    :class="block.model_name.toLowerCase()">
                    <template v-if="block.id != -1">
                        <span class="model-field-content"
                            :id="'id_' + instance_unique_id(block, block.id)"
                            v-html="getContent(block, block.id)"
                            ></span>
                        <a class="stream-btn" 
                        :id="'change_id_' + instance_unique_id(block, block.id)" 
                        :title="$root.stream_texts['Change']"
                        :href="get_change_model_link(block, block.id)"
                        :data-block="block.unique_id"
                        :data-instance-id="block.id"
                        @click.prevent="$root.openPopup"
                        v-text="$root.stream_texts['Change']"
                        ></a>
                    </template>
                    <template v-else>
                        <a class="stream-btn" 
                        :id="'add_id_' + block.unique_id"
                        title="$root.stream_texts['AddContent']"
                        :href="get_add_model_link(block)"
                        @click.prevent="$root.openPopup"
                        v-text="'+' + $root.stream_texts['AddContent']"
                        ></a>
                    </template>
                </div>
            </div> 
            <BlockOptions :block="block" />
        </div>
        <AddBlockHere :block="block" />
    </div>
</template>