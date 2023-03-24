<script type="text/javascript">
	import {isEmpty} from 'lodash'
	import draggable from 'vuedraggable'

	let 
		text_area,
		initial_data, 
		model_list_info, 
		delete_blocks_from_db, 
		base_admin_url, 
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
        },
        data () {
          return {
          	blocks: {}, // save content of all instances
	        show_help: false,
	        show_add_block: false,
	        will_removed: [], // blocks that will be removed from db
	        collapsed: false,
	        stream: [], // [{model_name: ..., id: ...}, ...]
	        model_info: {}, // {'model_name': model.__doc__}
	        stream_texts: window.stream_texts
          }
        },
        beforeMount: function() {
        	text_area = this.app_node.querySelector('textarea');
            initial_data = text_area.innerHTML;
		    model_list_info = text_area.getAttribute('model_list_info');
		    delete_blocks_from_db = Boolean(text_area.hasAttribute('delete_blocks_from_db'));
		    base_admin_url = text_area.getAttribute('base_admin_url');
		    popup_size = text_area.dataset.popup_size ? JSON.parse(text_area.dataset.popup_size) : [1000, 500];

		    this.stream = JSON.parse(initial_data) // [{model_name: ..., id: ...}, ...]
	        this.model_info = JSON.parse(model_list_info) // {'model_name': model.__doc__}

		    // update stream objects list
            // and store all blocks
            for (var i = this.stream.length - 1; i >= 0; i--) {
                var block = this.stream[i];
                
                if ( ! this.isAbstract(block)) {
                    if (this.isArray(block.id)) {
                        for (var j = block.id.length - 1; j >= 0; j--) {
                            this.updateBlock(block.unique_id, block.id[j].toString());
                        }
                    } else {
                        this.updateBlock(block.unique_id, block.id.toString());
                    }
                } else {
                    this.updateAbstractBlock(block.unique_id);
                }
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
                            if ( app.isArray(app.will_removed[i].id) ) {
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
            isArray: function(obj) {
                return _.isArray(obj);
            },
            isAbstract: function(block) {
                return this.model_info[block.model_name].abstract;
            },
            isEmpty: isEmpty,
            model_title: function(block) {
                var title = '...';
                if (this.model_info[block.model_name]) {
                    title = this.model_info[block.model_name].model_doc;
                }
                return title;
                
            },
            model_name_lower: function(block){
                return block.model_name.toLowerCase()
            },
            instance_unique_id: function(block, instance_id){
                return block.model_name.toLowerCase() + instance_id;
            },
            create_unique_hash: function() {
                return Math.random().toString(36).substring(7);
            },
            block_admin_url: function(block) {
                return base_admin_url + 'streamblocks/' + this.model_name_lower(block) + '/';
            },
            instance_admin_render_url: function(block, instance_id) {
                return '/streamfield/admin-instance/' + this.model_name_lower(block) + '/' + instance_id;
            },
            abstract_block_render_url: function(block) {
                return '/streamfield/abstract-block/' + this.model_name_lower(block) + '/';
            },
            get_change_model_link: function(block, instance_id){
                return this.block_admin_url(block) + instance_id + 
                        '/change/?_popup=1&block_id=' + block.unique_id + 
                        '&instance_id=' + instance_id +
                        '&app_id=' + this.app_node.id;
            },
            get_add_model_link: function(block){
                return this.block_admin_url(block) +
                        'add/?_popup=1&block_id=' + block.unique_id + 
                        '&app_id=' + this.app_node.id;
            },
            getBlockContent: function(block, item_id) {
                return this.blocks[this.instance_unique_id(block, item_id)];
            },
            getAbstractBlockContent: function(block) {
                return this.blocks[block.model_name];
            },
            updateAbstractBlock(block_unique_id) {
                var block = _.find(this.stream, ['unique_id', block_unique_id]);

                // change block content
                window.ax.get(this.abstract_block_render_url(block)).then((response) => {
                    this.blocks[block.model_name] = response.data;
                });

            },
            updateBlock: function(block_unique_id, instance_id) {
                let block = _.find(this.stream, ['unique_id', block_unique_id]);
                // change block content
                window.ax.get(this.instance_admin_render_url(block, instance_id)).then((response) => {
                    this.blocks[this.instance_unique_id(block, instance_id)] = response.data;
                });

                // if added new instance – add new instance id to block list
                let instance_id_int = parseInt(instance_id)
                if (this.isArray(block.id) &&  block.id.indexOf(instance_id_int) == -1) {
                    block.id.push(instance_id_int);
                }

                // if added new instance to block without list
                if ( !this.isArray(block.id) && block.id == -1 ) {
                    block.id = instance_id_int;
                }

            },
            deleteBlock: function(block_unique_id) {
                let block = _.find(this.stream, ['unique_id', block_unique_id]);
                let index = this.stream.indexOf(block);
                if (confirm('"' + this.model_title(block) + '" - ' + stream_texts['deleteBlock'])) {
                    if (index != -1) {
                        this.stream.splice(index, 1);

                        // prepare to remove from db
                        if ( !this.isAbstract(block)) {
                            this.will_removed.push(block);
                        }
                    }    
                }
                
            },
            deleteInstance: function(block_unique_id, instance_id) {
                let block = _.find(this.stream, ['unique_id', block_unique_id]);
                let block_index = this.stream.indexOf(block);
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
                                    athismodel_name_lower(block) + 
                                    '/' + id + '/delete/')
            },
            addNewBlock: function(block, model_name) {
                let options = {};
                let new_block;

                _.forEach(this.model_info[model_name].options, function(option, key) {
                    athis$set(options, key, option.default);
                });
                new_block = {
                    unique_id: this.create_unique_hash(),
                    model_name: model_name,
                    options: options
                };
                if (!block.abstract) {
                    new_block.id = block.as_list ? [] : -1;
                }
                this.stream.push(new_block);
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
                            options: i.options
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
        
        <div style="text-align: right;" v-if="stream.length > 1">
            <a href="javascript:;" @click="collapsed=!collapsed" v-html=" !collapsed ? '&minus; ' +  stream_texts['CollapseAll']: '&plus; ' + stream_texts['OpenAll']" class="collapse-handler"></a>
        </div>

        <div class="streamfield-models" :class="{collapsed}">
            <draggable v-model="stream" group="stream" handle=".block-move" item-key="unique_id">
	            <template #item="{element: block}">
	            	<div class="stream-model-block">
		                <h3 class="streamblock__block__title"><span v-text="model_title(block)"></span>
		                    <span class="streamblock__block-handle">
		                        <span class="block-move"></span>
		                        <span class="block-delete" @click="deleteBlock(block.unique_id)"></span>
		                    </span>
		                </h3>
		                <div v-if="!isAbstract(block)" >
		                    <div v-if="isArray(block.id)" 
		                        class="stream-model-block__content"
		                        :class="model_name_lower(block)"
		                        :id="'id_' + block.unique_id">
		                        <draggable v-model="block.id" group="items" handle=".subblock-move" item-key="id">
		                        	<template #item="{element: item_id}">
				                        <span class="stream-model-subblock">
				                            <span class="model-field-content"
				                                :id="'id_' + instance_unique_id(block, item_id)" 
				                                v-html="getBlockContent(block, item_id)"
				                                ></span>
				                            <span class="stream-model-subblock-handle">
				                                <span class="subblock-move"></span>
				                                <span class="subblock-delete" @click="deleteInstance(block.unique_id, item_id)"></span>
				                            </span>
				                            <a class="stream-btn" 
				                                :id="'change_id_' + instance_unique_id(block, item_id)" 
				                                :title="stream_texts['Change']" 
				                                :href="get_change_model_link(block, item_id)"
				                                :data-block="block.unique_id"
				                                :data-instance-id="item_id"
				                                @click.prevent="openPopup"
				                                v-text="stream_texts['Change']"
				                                ></a>
				                                &nbsp;

				                        </span>
			                    	</template>
		                        </draggable>
		                        <a class="stream-btn" 
		                            :id="'add_id_' + block.unique_id"
		                            :title="stream_texts['AddOneMore']"
		                            :href="get_add_model_link(block)"
		                            @click.prevent="openPopup"
		                            v-text="'+ ' + stream_texts['AddOneMore']"
		                            ></a>
		                    </div>
		                    <div v-else
		                        class="stream-model-block__content no-subblocks"
		                        :class="model_name_lower(block)">
		                        <template v-if="block.id != -1">
		                            <span class="model-field-content"
		                                :id="'id_' + instance_unique_id(block, block.id)"
		                                v-html="getBlockContent(block, block.id)"
		                                ></span>
		                            <a class="stream-btn" 
		                            :id="'change_id_' + instance_unique_id(block, block.id)" 
		                            :title="stream_texts['Change']"
		                            :href="get_change_model_link(block, block.id)"
		                            :data-block="block.unique_id"
		                            :data-instance-id="block.id"
		                            @click.prevent="openPopup"
		                            v-text="stream_texts['Change']"
		                            ></a>
		                        </template>
		                        <template v-else>
		                            <a class="stream-btn" 
		                            :id="'add_id_' + block.unique_id"
		                            title="stream_texts['AddContent']"
		                            :href="get_add_model_link(block)"
		                            @click.prevent="openPopup"
		                            v-text="'+' + stream_texts['AddContent']"
		                            ></a>
		                        </template>
		                    </div>
		                </div> 
		                <!-- /v-if="isAbstract" -->
		                <div v-else >
		                    <div class="stream-model-block__content no-subblocks abstract-block"
		                        :class="model_name_lower(block)">
		                        <span v-html="getAbstractBlockContent(block)"></span>
		                    </div>
		                </div>
		                <div class="stream-block__options" v-if="model_info[block.model_name] && !isEmpty(model_info[block.model_name].options)">
		                    <div class="stream-block__option" v-for="(option, key) in model_info[block.model_name].options">
		                        <template v-if="option.type == 'checkbox' || option.type == 'text'">
		                            <span v-text="option.label"></span>: <input :type="option.type" v-model="block.options[key]">
		                        </template>
		                        <template v-else-if="option.type == 'select'">
		                            <span v-text="option.label"></span>: 
		                            <select :name="option.label" v-model="block.options[key]">
		                                <option v-for="opt in option.options" :value="opt.value" v-text="opt.name"></option>
		                            </select>
		                        </template>
		                    </div>
		                </div>
		            </div>
	            </template>
            </draggable>
            <div class="stream-insert-new-block">
                <div class="add-new-block-button" @click="show_add_block=!show_add_block" v-text="stream_texts['AddNewBlock']"></div>
                <ul v-if="show_add_block">
                    <li v-for="(block, model_name) in model_info">
                        <a class="stream-btn" href="#" v-text="'+ ' + block.model_doc" @click.prevent="addNewBlock(block, model_name)"></a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>