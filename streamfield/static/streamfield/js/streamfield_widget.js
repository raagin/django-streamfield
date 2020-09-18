(function(w, $){
    function id_to_windowname(text) {
        text = text.replace(/\./g, '__dot__');
        text = text.replace(/\-/g, '__dash__');
        return text;
    }

    function onReady() {
        var csrftoken = Cookies.get('csrftoken');
        var streamfield_app = document.querySelectorAll('.streamfield_app');
        var ax = axios.create({
          headers: {"X-CSRFToken": csrftoken}
        });
        w.streamapps = {};


        for (var i = 0; i < streamfield_app.length; i++) {
            initStreamApp(streamfield_app[i]);
        }

        function initStreamApp(app_node) {

            var text_area = app_node.querySelector('textarea');
            var initial_data = text_area.innerHTML;
            var model_list_info = text_area.getAttribute('model_list_info');
            var delete_blocks_from_db = Boolean(text_area.hasAttribute('delete_blocks_from_db'));
            var base_admin_url = text_area.getAttribute('base_admin_url');
            var popup_size = text_area.dataset.popup_size ? JSON.parse(text_area.dataset.popup_size) : [1000, 500];

            var data = {
                stream: JSON.parse(initial_data), // [{model_name: ..., id: ...}, ...]
                model_info: JSON.parse(model_list_info), // {'model_name': model.__doc__}
                blocks: {}, // save content of all instances
                show_help: false,
                show_add_block: false,
                will_removed: [] // blocks that will be removed from db
            }

            var app = new Vue({
                el: app_node,
                data: data,
                beforeMount: function() {
                    // update stream objects list
                    // and store all blocks
                    for (var i = data.stream.length - 1; i >= 0; i--) {
                        var block = data.stream[i];
                        
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
                        $('input[type="submit"]', text_area.closest('form')).on('click', function(e){
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
                                $(e.target).trigger('click');
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
                                '&app_id=' + app_node.id;
                    },
                    get_add_model_link: function(block){
                        return this.block_admin_url(block) +
                                'add/?_popup=1&block_id=' + block.unique_id + 
                                '&app_id=' + app_node.id;
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
                        ax.get(this.abstract_block_render_url(block)).then(function (response) {
                            app.$set(app.blocks, block.model_name, response.data);
                        });
        
                    },
                    updateBlock: function(block_unique_id, instance_id) {
                        var block = _.find(this.stream, ['unique_id', block_unique_id]);
                        
                        // change block content
                        ax.get(this.instance_admin_render_url(block, instance_id)).then(function (response) {
                            app.$set(app.blocks, app.instance_unique_id(block, instance_id), response.data);
                        });

                        // if added new instance – add new instance id to block list
                        var instance_id_int = parseInt(instance_id)
                        if (this.isArray(block.id) &&  block.id.indexOf(instance_id_int) == -1) {
                            block.id.push(instance_id_int);
                        }

                        // if added new instance to block without list
                        if ( !this.isArray(block.id) && block.id == -1 ) {
                            block.id = instance_id_int;
                        }

                    },
                    deleteBlock: function(block_unique_id) {
                        var block = _.find(this.stream, ['unique_id', block_unique_id]);
                        var index = this.stream.indexOf(block);
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
                        var block = _.find(this.stream, ['unique_id', block_unique_id]);
                        var block_index = this.stream.indexOf(block);
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
                        return ax.delete('/streamfield/admin-instance/' + 
                                            app.model_name_lower(block) + 
                                            '/' + id + '/delete/')
                    },
                    addNewBlock: function(block, model_name) {
                        var options = {};
                        var new_block;

                        _.forEach(this.model_info[model_name].options, function(option, key) {
                            app.$set(options, key, option.default);
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
                        var triggeringLink = e.target;
                        var name = id_to_windowname(triggeringLink.id.replace(/^(change|add|delete)_/, ''));
                        var href = triggeringLink.href;
                        var win = w.open(href, name, 'height=' + popup_size[1] + ',width=' + popup_size[0] + ',resizable=yes,scrollbars=yes');
                        win.focus();
                        return false;
                    }
                },
                computed: {
                    textarea: function(){
                        return JSON.stringify(this.stream.map(function(i){
                            // return only fields that in initial data
                             return {
                                    unique_id: i.unique_id,
                                    model_name: i.model_name, 
                                    id: i.id,
                                    options: i.options
                                };
                         }));
                    }
                }
            });
            
            w.streamapps[app_node.id] = app;

        } // end initStreamApp function

    };

    w.addEventListener('DOMContentLoaded', function(event) {
        onReady();
    });

})(window, django.jQuery);