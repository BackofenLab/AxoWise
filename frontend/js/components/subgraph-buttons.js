Vue.component("subgraph-buttons", {
    template: `
        <div class="col-md-4 ui-widget">
            <button id="reduce-graph-btn"
                    class="btn btn-warning"
                    v-bind:disabled="$root.wait"
            >Reduce</button>
            <button id="undo-graph-btn"
                    class="btn btn-secondary"
                    v-bind:disabled="$root.wait"
            >Undo</button>
        </div>
    `
});