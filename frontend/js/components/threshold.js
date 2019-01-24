Vue.component("threshold", {
    template: `
        <div class="col-md-4 ui-widget">
            Protein - protein score threshold:
            <br/>
            <input id="threshold-slider"
                   type="range"
                   v-bind:min="$root.threshold.min"
                   v-bind:max="$root.threshold.max"
                   v-bind:step="$root.threshold.step"
                   v-bind:disabled="$root.wait"
                   v-on:change="$root.threshold_resubmit"
                   v-model="$root.threshold.value"
            />
            <input id="threshold-input"
                   type="number"
                   v-bind:min="$root.threshold.min"
                   v-bind:max="$root.threshold.max"
                   v-bind:step="$root.threshold.step"
                   v-bind:disabled="$root.wait"
                   v-on:change="$root.threshold_resubmit"
                   v-model="$root.threshold.value"
            />
        </div>
    `
});