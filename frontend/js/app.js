var APP = null;

$(document).ready(function () {
    APP = new Vue({
        el: '#pgdb-app',
        data: {
            gephi_json: null,
            active_node: null,
            active_term: null
        },
        watch: {
            active_node: function(node) {
                var com = this;
                if (node == null) return;

                com.active_term = null;
            },
            active_term: function(term) {
                var com = this;
                if (term == null) return;

                com.active_node = null;
            }
        },
        methods: {}
    });
});