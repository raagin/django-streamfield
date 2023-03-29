import "@/style.sass"
import axios from 'axios'
import Cookies from 'js-cookie'
import { createApp } from 'vue'
import App from '@/components/App.vue'

(function(w, $){
    function onReady() {
        let streamfield_app = document.querySelectorAll('.streamfield_app');
        w.ax = axios.create({
          headers: {"X-CSRFToken": Cookies.get('csrftoken')}
        });
        w.streamapps = {};
        for (let i = 0; i < streamfield_app.length; i++) {
            let app_node =streamfield_app[i];
            let app = createApp(App, {app_node}).mount(app_node.querySelector('.mount-node'));
            w.streamapps[streamfield_app[i].id] = app;
        }
    };

    w.addEventListener('DOMContentLoaded', function(event) {
        onReady();
    });

})(window, django.jQuery);