Vue.component("info", {
    template: `
        <div id="info" class="col-md-4">
            {{$root.visualization.title}}<br/>
            Nodes: {{$root.visualization.num_nodes}}<br/>
            Edges: {{$root.visualization.num_edges}}<br/>
        </div>
    `
});
