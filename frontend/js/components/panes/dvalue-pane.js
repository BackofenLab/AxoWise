Vue.component("dvalue-pane", {
    props: ["d_value","gephi_json"],
    data: function() {
        return {
            selected_term: null,
            dval_proteins: [],
            links: [],
            dboundary: {
                value: 1,
                min: 1,
                max: 10,
                step: 1
            },
            dvalue_min: {
                value: -5,
                min: -10,
                max: 10,
                step: 1
            },
            dvalue_max: {
                value: 5,
                min: -10,
                max: 10,
                step: 1
            },
            pane_check: false,
        }
    },
    methods: {
        select_node: function(id) {
            var com = this;
            com.$emit("active-node-changed", id);
        },
        draw_legend: function() {
            var com = this;

            var minB = - com.dboundary.value;
            var maxB = com.dboundary.value;
            var listB = [minB, minB/2, minB/4, 0, maxB/4, maxB/2, maxB]

            $("#demo1").html("");
            var svg = d3.select("#demo1");

            var xScale = d3.scaleLinear()
                            .domain(listB)
                            .range([10, 40, 70, 100, 130, 160, 190]);
            
            var xAxis = d3.axisBottom(xScale)
                        .tickValues(listB);
            
    
            svg.append("g")
                .attr("transform", "translate(0,80)")
                .attr("color","white")
                .call(xAxis);
            
            var colorScale = d3.scaleLinear()
                                .domain([minB, 0, maxB])
                                .range(["blue", "white", "red"]);
            
            svg.selectAll("circle")
                .data(listB)
                .enter()
                .append("circle")
                .attr("cx", (d) => xScale(d))
                .attr("cy", 60)
                .attr("r", 9)
                .attr("stroke", "black")
                .attr("stroke-width", 1)
                .attr("fill", (d) => colorScale(d));


        },
        check_boundary: function() {
            var com = this;
            this.draw_legend();
            this.eventHub.$emit('dboundary-update', this.dboundary.value);
        },
        hide_panel: function() {
            var com = this;
            if(com.pane_check == false){
                $("#minimizer").find("#dropdown-btn-min").css({'transform': 'rotate(90deg)'});
                $("#dvaluepane").hide();
            }else{
                $("#minimizer").find("#dropdown-btn-min").css({'transform': 'rotate(0deg)'});
                $("#dvaluepane").show();
            }
            com.pane_check = !com.pane_check;
        },
        show_proteins: function(min,max) {
            var com = this;

            //check if min is greater than max
            if(min > max) {
                alert("Your min value is less than max!") 
                return;
            }

            //Get all proteins which dvalue is greater min and less max
            com.dval_proteins = [];
            com.gephi_json.nodes.forEach(node => {
                var dvalue = node.attributes[com.d_value]
                if(dvalue >= min && dvalue <= max){
                    com.dval_proteins.push(node);
                }
            });

            com.$emit("active-layer-changed", com.dval_proteins);

        },
        copyclipboard: function(){
            com = this;

            textToCopy = [];
            for(link of com.dval_proteins) textToCopy.push(link.label);
            navigator.clipboard.writeText(textToCopy.join("\n"));
        },
        expand_proteins: function() {
            var com = this;
            com.edges_expand = !com.edges_expand;
            if(com.edges_expand == false){
                $("#link").hide();
            }else{
                $("#link").show();
            }
            
        },
    },
    watch: {
        "d_value": function(term) {
            var com = this;
            if(term == null || term == "no selection"){
                $("#minimizer").hide();
                return;
            }
            com.draw_legend();

            // TODO
            $("#minimizer").show();
        }
    },
    mounted: function() {
        var com = this;

        $("#dboundary-slider").slider();
        $("#dboundary-slider").change(com.check_boundary);
        $("#dboundary-input").change(com.check_boundary);

        $("#minimizer").find("#dropdown-btn-min").click(() => com.hide_panel());
        $("#minimizer").find("#dropdown-btn-close").click(() => com.$emit("d_value-changed", null));
    },
    template: `
    <div id="minimizer" class="minimize">
        <div class="min-button">
        <button id="dropdown-btn-min"></button>
        <button id="dropdown-btn-close"></button>
        </div>
        <div id="dvaluepane" class="pane">
            <div class="text">
                <div class="headertext">
                    <span>Information Pane</span>
                </div>
                <div class="nodeattributes">
                    <div class="p">
                    <b>Legend:</b>
                    </div>
                    <svg id="demo1" width="250" height="120"></svg>
                    <div class="boundary">
                    <input id="dboundary-slider"
                        type="range"
                        v-bind:min="dboundary.min"
                        v-bind:max="dboundary.max"
                        v-bind:step="dboundary.step"
                        v-model="dboundary.value"
                    />
                    <input id="dboundary-input"
                        type="number"
                        v-bind:min="dboundary.min"
                        v-bind:max="dboundary.max"
                        v-bind:step="dboundary.step"
                        v-model="dboundary.value"
                    />
                    </div>
                    <div class="dvalue-selection">
                        <div class="p">
                        <b>Selection:</b>
                        </div>
                        <div class="selection">
                        <div class="label">
                        <span>Min:</span>
                        <input id="select-input"
                        type="number"
                        v-bind:min="dvalue_min.min"
                        v-bind:max="dvalue_min.max"
                        v-bind:step="dvalue_min.step"
                        v-model="dvalue_min.value"
                        />
                        </div>
                        <div class="label">
                        <span>Max:</span>
                        <input id="select-input-max"
                        type="number"
                        v-bind:min="dvalue_max.min"
                        v-bind:max="dvalue_max.max"
                        v-bind:step="dvalue_max.step"
                        v-model="dvalue_max.value"
                        />
                        </div>
                        <button id="show-dvalue" v-on:click="show_proteins(dvalue_min.value, dvalue_max.value)">Show</button>
                        </div>
                    </div>
                    <div class="p">
                    <span>Proteins:</span>
                    <button v-on:click="copyclipboard()" id="copy-btn">Copy</button>
                    <button v-on:click="expand_proteins()" id="expand-btn">Expand</button>
                    </div>
                    <div class="link" id="link">
                        <ul>
                            <li v-for="node in dval_proteins">
                                <a href="#" v-on:click="select_node(node.id)">{{node.label}}</a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `
});
