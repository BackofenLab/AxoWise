Vue.component("hubs", {
    props: ["gephi_json"],
    data: function() {
        return  {
            message: "",
        }
    },
    methods: {
        get_hubs: function() {
            var com = this;

            console.log("start")
        },
    },
    template: `
        <div v-show="gephi_json != null" class="toolbar-button">
            <div class="toolbar-theme">
                <button v-on:click="get_hubs()" id="hide_hubs">Hide Hubs</button>
                <span class="toolbar-icon">H</span>
            </div>
        </div>
    `
});