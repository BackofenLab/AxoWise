Vue.component("node-filter", {
    model: {
        prop: "show",
        event: "checked"
    },
    props: ["show"],
    mounted: function() {
        $("#show-proteins").checkboxradio({
            icon: false,
            classes: {
                "ui-checkboxradio-checked": "protein-color"
            }
        });

        $("#show-pathways").checkboxradio({
            icon: false,
            classes: {
                "ui-checkboxradio-checked": "pathway-color"
            }
        });

        $("#show-classes").checkboxradio({
            icon: false,
            classes: {
                "ui-checkboxradio-checked": "class-color"
            }
        });
    },
    template: `
        <div class="col-md-4 ui-widget">
            Filter nodes by type:<br/>
            <label for="show-proteins">Protein</label>
            <input type="checkbox"
                   v-model="show.proteins"
                   id="show-proteins"
            >

            <label for="show-pathways">Pathway</label>
            <input type="checkbox"
                   v-model="show.pathways"
                   id="show-pathways"
            >

            <label for="show-classes">Class</label>
            <input type="checkbox"
                   v-model="show.classes"
                   id="show-classes"
            >
        </div>
    `
});