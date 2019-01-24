Vue.component("info", {
    template: `
        <div id="info">
            {{$root.visualization.title}}<br/>
            Nodes: {{$root.visualization.num_nodes}}<br/>
            Edges: {{$root.visualization.num_edges}}<br/>
        </div>
    `
});
