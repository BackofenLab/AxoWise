Vue.component("highlight_button", {
    props: ["gephi_json","protein_list"],
    data: function() {
        return  {
            message: "",
            terms: []
        }
    },
    methods: {
        open_list: function() {
            var com = this;
            com.$emit("protein-list-changed", "SHOW");
        },
    },
    template: `
        <div v-show="gephi_json != null" class="toolbar-button">
            <div class="toolbar-theme">
                <button v-on:click="open_list()">Insert Proteins</button>
                <span class="toolbar-icon">L</span>
            </div>
        </div>
    `
});