Vue.component("threshold", {
    template: `
        <div class="col-md-4 ui-widget">
            Protein - protein score threshold:
            <br/>
            <input type="range"
                   v-bind:min="$root.threshold.min"
                   v-bind:max="$root.threshold.max"
                   v-bind:step="$root.threshold.step"
                   v-bind:disabled="$root.wait"
                   v-model="$root.threshold.value"
                   class="ui-slider ui-corner-all ui-slider-horizontal ui-widget ui-widget-content"
            />
            <input type="number"
                   v-bind:min="$root.threshold.min"
                   v-bind:max="$root.threshold.max"
                   v-bind:step="$root.threshold.step"
                   v-bind:disabled="$root.wait"
                   v-model="$root.threshold.value"
            />
        </div>
    `
});