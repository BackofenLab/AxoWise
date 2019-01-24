Vue.component("protein", {
    template: `
        <div class="col-md-4 ui-widget">
            Protein:
            <br/>
            <input id="protein-input"
                   type="text"
                   v-model="$root.protein.name"
                   v-bind:disabled="$root.wait">
            </input>
            <br/>
            <button id="protein-btn"
                    class="btn btn-primary"
                    v-bind:disabled="$root.wait"
                    v-on:click="$root.wait = true"
            >Submit</button>
        </div>
    `
});