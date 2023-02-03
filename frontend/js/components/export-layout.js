Vue.component("export-layout", {
    props: ["gephi_json"],
    data: function() {
        return  {
            message: "",
            terms: []
        }
    },
    methods: {
        export_graph: function() {
            var com = this;

            let dataStr = JSON.stringify(com.gephi_json);
            let dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
        
            let exportFileDefaultName = 'data.json';
        
            let linkElement = document.createElement('a');
            linkElement.setAttribute('href', dataUri);
            linkElement.setAttribute('download', exportFileDefaultName);
            linkElement.click();
        },
    },
    mounted: function() {
        var com = this;
        var jsonObj = null;

        $(document).on('change', '#graph-file', function(event) {
            var reader = new FileReader();
          
            reader.onload = function(event) {
              jsonObj = JSON.parse(event.target.result);
              com.$emit("gephi-json-changed", jsonObj);
            }
          
            reader.readAsText(event.target.files[0]);
          });

    },
    template: `
    <div class="cf">
        <div v-show="gephi_json == null">
            <h4>Import Graph:</h4>
            <input type="file" id="graph-file" accept=".json">
            <br/><br/>
        </div>
        <div v-show="gephi_json != null">
            <button v-on:click="export_graph()" id="export_json">Export Json</button>
        </div>
    </div>
    `
});