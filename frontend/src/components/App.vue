<script type="text/javascript">
    import draggable from 'vuedraggable'
    import {isArray, isEmpty} from '@/utils.js'
    import StreamBlock from '@/components/StreamBlock.vue'
    import AbstractBlock from '@/components/AbstractBlock.vue'

    // const _ = require('lodash');

    let 
        text_area,
        delete_blocks_from_db,
        popup_size;

    function id_to_windowname(text) {
        text = text.replace(/\./g, '__dot__');
        text = text.replace(/\-/g, '__dash__');
        return text;
    }

    export default {
        props: ['app_node'],
        components: {
            draggable,
            StreamBlock,
            AbstractBlock
        },
        data () {
          return {
            blocks: {}, // save content of all instances
            show_help: false,
            show_add_block: false,
            will_removed: [], // blocks that will be removed from db
            stream: [], // [{model_name: ..., id: ...}, ...]
            model_info: {}, // {'model_name': model.__doc__},
            base_admin_url: "",
            stream_texts: window.stream_texts
          }
        },
        beforeMount: function() {
            text_area = this.app_node.querySelector('textarea')
            delete_blocks_from_db = Boolean(text_area.hasAttribute('delete_blocks_from_db'))
            popup_size = text_area.dataset.popup_size ? JSON.parse(text_area.dataset.popup_size) : [1000, 500]

            this.base_admin_url = text_area.getAttribute('base_admin_url')
            this.stream = JSON.parse(text_area.innerHTML)
            this.model_info = JSON.parse(text_area.getAttribute('model_list_info'))

            if (this.stream.length && !this.stream[0].hasOwnProperty('collapsed')) {
                this.setAllCollapsed(false)
            }
            
            // delete removed instances from db when form submit
            if ( delete_blocks_from_db ) {
                let app = this
                django.jQuery('input[type="submit"]', text_area.closest('form')).on('click', function(e){
                    if ( !app.will_removed.length ) return;
                    
                    e.preventDefault();
                    
                    var all_requests = [];

                    for (var i = app.will_removed.length - 1; i >= 0; i--) {
                        if ( app.will_removed[i].id != -1 ) {

                            // for array
                            if ( isArray(app.will_removed[i].id) ) {
                                var ids = app.will_removed[i].id;
                                for (var j = ids.length - 1; j >= 0; j--) {
                                    all_requests.push(app.deleteAction(app.will_removed[i], ids[j], i));
                                }
                            // for one
                            } else {
                                all_requests.push(app.deleteAction(app.will_removed[i], app.will_removed[i].id, i));
                            }
                        }
                    }

                    Promise.all(all_requests).then(function(){
                        app.will_removed = [];
                        django.jQuery(e.target).trigger('click');
                    });

                }); // EventListener
            }

        },
        methods: {
            isAbstract: function(block) {
                return this.model_info[block.model_name].abstract;
            },
            isEmpty: isEmpty,
            isArray: isArray,
            setAllCollapsed: function(value) {
                this.stream.forEach((v, k) => {
                    v.collapsed = value
                })
            },
            model_title: function(block) {
                var title = '...';
                if (this.model_info[block.model_name]) {
                    title = this.model_info[block.model_name].model_doc
                }
                return title;
                
            },
            getBlockIndex: function(block_unique_id) {
                const block = this.stream.find(function(o) {return o.unique_id = block_unique_id})
                const index = this.stream.indexOf(block)
                return [index, block]
            },
            createUniqueHash: function() {
                return Math.random().toString(36).substring(7)
            },
            updateBlock: function(block_unique_id, instance_id) {
                this.$refs[block_unique_id].updateBlock(instance_id)
            },
            deleteBlock: function(block_unique_id) {
                let [index, block] = this.getBlockIndex(block_unique_id)
                if (confirm('"' + this.model_title(block) + '" - ' + stream_texts['deleteBlock'])) {
                    if (index != -1) {
                        this.stream.splice(index, 1)

                        // prepare to remove from db
                        if ( !this.isAbstract(block)) {
                            this.will_removed.push(block)
                        }
                    }    
                }
            },
            deleteInstance: function(block_unique_id, instance_id) {
                let [block_index, block]  = this.getBlockIndex(block_unique_id)
                if (confirm(stream_texts['deleteInstance'])) {
                    if (block_index != -1) {
                        // remove from block id
                        block.id.splice(block.id.indexOf(parseInt(instance_id)), 1);

                        // prepare to remove from db
                        this.will_removed.push({
                            model_name: block.model_name,
                            id: instance_id
                        });
                        
                    }    
                }
            },
            deleteAction: function(block, id, idx) {
                return window.ax.delete('/streamfield/admin-instance/' + 
                                    block.model_name.toLowerCase() + 
                                    '/' + id + '/delete/')
            },
            addNewBlock: function(block, model_name, idx) {
                let options = {};
                let new_block;

                Object.entries(this.model_info[model_name].options).forEach(([key, option],index) => {
                    options[key] = option.default;
                });
                new_block = {
                    unique_id: this.createUniqueHash(),
                    model_name: model_name,
                    options: options,
                    collapsed: false
                };
                if (!block.abstract) {
                    new_block.id = block.as_list ? [] : -1;
                }
                if (idx) {
                    this.stream.splice(idx, 0, new_block);
                } else {
                    this.stream.push(new_block);
                }
                this.show_add_block = false;
            },
            openPopup: function(e){
                let triggeringLink = e.target;
                let name = id_to_windowname(triggeringLink.id.replace(/^(change|add|delete)_/, ''));
                let href = triggeringLink.href;
                let win = window.open(href, name, 'height=' + popup_size[1] + ',width=' + popup_size[0] + ',resizable=yes,scrollbars=yes');
                win.focus();
                return false;
            }
        },
        watch: {
            stream: {
                handler(nv) {
                    text_area.innerHTML = JSON.stringify(nv.map(function(i){
                        // return only fields that in initial data
                        return {
                            unique_id: i.unique_id,
                            model_name: i.model_name, 
                            id: i.id,
                            options: i.options,
                            collapsed: i.collapsed
                        };
                    }));    
                },
                deep: true    
            }
        }
    }
</script>
<template>
    <div>
        <div class="stream-help-text" v-if="stream_texts['help_text']">
            <div class="stream-help-text__title" @click="show_help=!show_help" v-text="stream_texts['Help?']"></div>
            <div v-show="show_help" class="stream-help-text__content" v-html="stream_texts['help_text']"></div>
        </div>
        
        <div class="collapse-handlers" v-if="stream.length > 1">
            <a href="javascript:;" @click="setAllCollapsed(false)" v-html="stream_texts['Open all'] + ' &plus;' " class="collapse-handler"></a> &nbsp;
            <a href="javascript:;" @click="setAllCollapsed(true)" v-html="stream_texts['Collapse all'] + ' &minus;'" class="collapse-handler"></a>
        </div>

        <div class="streamfield-models">
            <draggable v-model="stream" group="stream" handle=".block-move" item-key="unique_id">
                <template #item="{element: block}">
                    <StreamBlock v-if="!isAbstract(block)" :block="block" :ref="block.unique_id"/>
                    <AbstractBlock v-else :block="block" />
                </template>
            </draggable>
            <div class="stream-insert-new-block">
                <div class="add-new-block-button" @click="show_add_block=!show_add_block" v-text="stream_texts['AddNewBlock']"></div>
                <div class="stream-insert-new-block-models" v-if="show_add_block">
                    <ul>
                        <li v-for="(block, model_name) in model_info">
                            <a class="stream-btn" href="#" v-text="'+ ' + block.model_doc" @click.prevent="addNewBlock(block, model_name)"></a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>