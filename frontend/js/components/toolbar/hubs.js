Vue.component("hubs", {
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
        draw_hubs: function() {
            //TODO
            console.log("Start");
        },
    },
    mounted: function() {
        var com = this;

        $("#hubs-slider").slider();
        $("#hubs-slider").change(com.draw_hubs);
        $("#hubs-input").change(com.draw_hubs);

    },
    template: `
        <div v-show="gephi_json != null" class="toolbar-button">
            <div class="toolbar-theme">
             <div class="boundary">
                <input id="hubs-slider"
                    type="range"
                    v-bind:min="edge_thick.min"
                    v-bind:max="edge_thick.max"
                    v-bind:step="edge_thick.step"
                    v-model="edge_thick.value"
                />
                <input id="hubs-input"
                    type="number"
                    v-bind:min="edge_thick.min"
                    v-bind:max="edge_thick.max"
                    v-bind:step="edge_thick.step"
                    v-model="edge_thick.value"
                />
            </div>
            <span class="toolbar-icon">H</span>
            </div>
        </div>
    `
});