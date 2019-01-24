Vue.component("threshold", {
    model: {
        prop: "threshold",
        event: "threshold-changed"
    },
    props: ["threshold"],
    data: function() {
        return {
            min: 0.4,
            max: 1.0,
            step: 0.001
        }
    },
    template: `
        <div class="col-md-4 ui-widget">
            Protein - protein score threshold:
            <br/>
            <input id="threshold-slider"
                   type="range"
                   v-bind:min="min"
                   v-bind:max="max"
                   v-bind:step="step"
                   v-bind:disabled="$root.wait"
                   v-on:input="$emit('threshold-changed', $event.target.value)"
                   v-on:change="$emit('change')"
                   v-bind:value="threshold"
            />
            <input id="threshold-input"
                   type="number"
                   v-bind:min="min"
                   v-bind:max="max"
                   v-bind:step="step"
                   v-bind:disabled="$root.wait"
                   v-on:input="$emit('threshold-changed', $event.target.value)"
                   v-on:change="$emit('change')"
                   v-bind:value="threshold"
            />
        </div>
    `
});