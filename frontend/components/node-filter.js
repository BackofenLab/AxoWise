Vue.component("node-filter", {
    template: `
        <div class="col-md-4 ui-widget">
            <label for="protein">Protein</label><input type="checkbox" checked="true" name="protein">
            <label for="pathway">Pathway</label><input type="checkbox" checked="true" name="pathway">
            <label for="class">Class</label><input type="checkbox" checked="true" name="class">
        </div>
    `
});