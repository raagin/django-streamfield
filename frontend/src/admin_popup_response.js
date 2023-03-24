/*global opener */
(function() {
    'use strict';
    var initData = JSON.parse(document.getElementById('django-admin-popup-response-constants').dataset.popupResponse);
    
    switch(initData.action) {
    case 'change':
        opener.streamapps[initData.app_id].updateBlock(initData.block_id, initData.instance_id);
        window.close();
        break;
    case 'delete':
        // opener.console.log("delete", initData);
        break;
    default:
        opener.streamapps[initData.app_id].updateBlock(initData.block_id, initData.instance_id);
        window.close();
        break;
    }
})();
