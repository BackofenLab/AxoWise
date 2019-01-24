Vue.component("protein-list", {
    template: `
        <div class="col-md-4 ui-widget">
            Protein list:
            <br/>
            <textarea id="protein-list-input"
                      v-model="$root.protein_list.value"
                      v-bind:disabled="$root.wait"
            ></textarea>
            <br/>
            <button id="protein-list-btn"
                    class="btn btn-primary"
                    v-bind:disabled="$root.wait"
                    v-on:click="$root.wait = true"
            >Submit</button>
        </div>
    `
});