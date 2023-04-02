<script>
    export default {
        props: ['block']
    }
</script>
<template>
    <div class="stream-block__options" v-if="$root.model_info[block.model_name] && !$root.isEmpty($root.model_info[block.model_name].options)">
        <div class="stream-block__option" v-for="(option, key) in $root.model_info[block.model_name].options">
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
</template>