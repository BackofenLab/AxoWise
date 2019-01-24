Vue.component("node-filter", {
    template: `
        <div class="col-md-4 ui-widget">
            Filter nodes by type:<br/>
            <label for="show-proteins">Protein</label>
            <input type="checkbox"
                   v-model="$root.visualization.proteins"
                   id="show-proteins"
            >

            <label for="show-pathways">Pathway</label>
            <input type="checkbox"
                   v-model="$root.visualization.pathways"
                   id="show-pathways"
            >

            <label for="show-classes">Class</label>
            <input type="checkbox"
                   v-model="$root.visualization.classes"
                   id="show-classes"
            >
        </div>
    `
});