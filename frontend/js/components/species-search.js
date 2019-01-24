Vue.component("species-search", {
    template: `
        <div class="col-md-4 ui-widget">
            Species:
            <br/>
            <input id="species-input" type="text" v-model="$root.species.name"></input>
        </div>
    `
});