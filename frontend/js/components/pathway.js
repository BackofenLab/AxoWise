Vue.component("pathway", {
    template: `
        <div class="col-md-4 ui-widget">
            Pathway:
            <br/>
            <input id="pathway-input"
                   type="text"
                   v-model="$root.pathway.name"
                   v-bind:disabled="$root.wait"
            ></input>
            <br/>
            <button id="pathway-btn"
                    class="btn btn-primary btn-xs"
                    v-bind:disabled="$root.wait"
                    v-on:click="$root.wait = true"
            >Submit</button>
        </div>
    `
});