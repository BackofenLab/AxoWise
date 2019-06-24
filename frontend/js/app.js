var APP = null;

$(document).ready(function () {
    APP = new Vue({
        el: '#pgdb-app',
        data: {
            gephi_json: null,
            active_node: null,
            active_term: null
        },
        methods: {}
    });
});