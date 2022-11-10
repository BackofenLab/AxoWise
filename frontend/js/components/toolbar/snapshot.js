Vue.component("snapshot", {
    props: ["gephi_json"],
    data: function() {
        return  {
            export_file: "graph",
        }
    },
    methods: {
        snapshot: function() {
            this.eventHub.$emit('export-graph', (0 === this.export_file.length) ? 'graph.png' : this.export_file + '.png');
        },
    },
    mounted: function() {
        var com = this;

    },
    template: `
        <div v-show="gephi_json != null" class="toolbar-button">
            <div class="toolbar-theme">
                <button v-on:click="snapshot()" id="export_json">Snapshot</button>
                <span class="toolbar-icon">S</span>
            </div>
        </div>
    `
});