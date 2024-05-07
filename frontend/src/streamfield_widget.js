import "@/style.sass"
import axios from 'axios'
import { createApp } from 'vue'
import App from '@/components/App.vue'

(function(){
    function onReady() {
        let streamfield_app = document.querySelectorAll('.streamfield_app');
        window.ax = axios.create({
          headers: {"X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value}
        });
        window.streamapps = {};
        for (let i = 0; i < streamfield_app.length; i++) {
            let app_node =streamfield_app[i];
            let app = createApp(App, {app_node}).mount(app_node.querySelector('.mount-node'));
            window.streamapps[streamfield_app[i].id] = app;
        }
    };
    window.addEventListener('DOMContentLoaded', function(event) {
        onReady();
    });
})();