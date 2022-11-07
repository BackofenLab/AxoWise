Vue.component("tool-visualization", {
    props: ["gephi_json"],
    data: function() {
        return  {
            edge_thick: {
                value: 0.2,
                min: 0,
                max: 1.0,
                step: 0.1
            },
        }
    },
    methods: {
        edge_update: function() {
            this.eventHub.$emit('edge-update', this.edge_thick.value);
        },
    },
    mounted: function() {
        var com = this;

        $("#edge-slider").slider();
        $("#edge-slider").change(com.edge_update);
        $("#edge-input").change(com.edge_update); //update from input control

    },
    template: `
        <div v-show="gephi_json != null" class="toolbar-button">
            <div class="toolbar-theme">
             <div class="boundary">
                <input id="edge-slider"
                    type="range"
                    v-bind:min="edge_thick.min"
                    v-bind:max="edge_thick.max"
                    v-bind:step="edge_thick.step"
                    v-model="edge_thick.value"
                />
                <input id="edge-input"
                    type="number"
                    v-bind:min="edge_thick.min"
                    v-bind:max="edge_thick.max"
                    v-bind:step="edge_thick.step"
                    v-model="edge_thick.value"
                />
            </div>
            <span class="toolbar-icon">V</span>
            </div>
        </div>
    `
});