Vue.component("node-filter", {
    template: `
        <div class="col-md-4 ui-widget">
            <label for="protein">Protein</label>
            <input type="checkbox"
                   v-model="$root.visualization.proteins"
                   name="protein"
            >

            <label for="pathway">Pathway</label>
            <input type="checkbox"
                   v-model="$root.visualization.pathways"
                   name="pathway"
            >

            <label for="class">Class</label>
            <input type="checkbox"
                   v-model="$root.visualization.classes"
                   name="class"
            >
        </div>
    `
});