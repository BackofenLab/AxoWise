Vue.component("subset-dialog", {
    props: ["active_subset"],
    watch: {
        "active_subset": function(subset) {
            if (subset.length < 1) return;

            $("#dialog").dialog("open");
        }
    },
    mounted: function() {
        $("#dialog").dialog({
            autoOpen: false,
            resizable: false,
            height: "auto",
            width: 400,
            modal: true,
            buttons: {
                "Close": function() {
                    $( this ).dialog( "close" );
                }
            }
        });
    },
    template: `
        <div id="dialog" title="Protein subset">
            <p v-for="node in active_subset">
                {{node.label}}
            </p>
        </div>
    `
});
