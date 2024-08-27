import "@/style.sass"
import axios from 'axios'
import { createApp } from 'vue'
import App from '@/components/App.vue'

(function(){
    function initApps(node) {
        let app_nodes = node.querySelectorAll(".streamfield_app:not([id*='__prefix__'])");
        for (let i = 0; i < app_nodes.length; i++) {
            let app_node = app_nodes[i];
            let app = createApp(App, {app_node}).mount(app_node.querySelector('.mount-node'));
            window.streamapps[app_node.id] = app;
        }
    }
    function onReady() {
        window.ax = axios.create({
          headers: {"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value}
        });
        window.streamapps = {};
        initApps(document)
    };
    window.addEventListener('DOMContentLoaded', function(event) {
        onReady();
    });
    document.addEventListener("formset:added", function(event) {
        initApps(event.target)
    });
})();