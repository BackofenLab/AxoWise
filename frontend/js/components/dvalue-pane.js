Vue.component("dvalue-pane", {
    props: ["d_value"],
    data: function() {
        return {
            selected_term: null,
            links: [],
            dboundary: {
                value: 1,
                min: 1,
                max: 10,
                step: 1
            }
        }
    },
    methods: {
        select_node: function(id) {
            var com = this;
            com.$emit("active-node-changed", id);
        },
        check_boundary: function() {
            var com = this;

            $('#demo1').hide().show(0);
            this.eventHub.$emit('dboundary-update', this.dboundary.value);
        }
    },
    watch: {
        "d_value": function(term) {
            var com = this;
            if (term == null) {
                $("#dvaluepane").animate({width: 'hide'}, 350);
                return;
            }

            var minB = - com.dboundary.value;
            var maxB = com.dboundary.value;
            var listB = [minB, minB/2, minB/4, 0, maxB/4, maxB/2, maxB]
            var svg = d3.select("#demo1");
    
            var xScale = d3.scaleLinear()
                            .domain(listB)
                            .range([10, 40, 70, 100, 130, 160, 190]);
            
            var xAxis = d3.axisBottom(xScale)
                        .tickValues(listB);
    
            svg.append("g")
                .attr("transform", "translate(0,80)")
                .attr("color","black")
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
        
            

            // TODO
            $("#dvaluepane").animate({width:'show'}, 350);
        }
    },
    mounted: function() {
        var com = this;

        $("#dboundary-slider").slider();
        $("#dboundary-slider").change(com.check_boundary);
        $("#dboundary-input").change(com.check_boundary);

        $("#dvaluepane").find(".returntext").click(() => com.$emit("d_value-changed", null));
        $("#dvaluepane").find(".close").click(() => com.$emit("d_value-changed", null));
    },
    template: `
        <div id="dvaluepane" class="pane">
            <div class="text">
                <div title="Close" class="left-close returntext">
                    <div class="c cf">
                        <span>Return to the full network</span>
                    </div>
                </div>
                <div class="headertext">
                    <span>Information Pane</span>
                    <svg id="demo1" width="250" height="120"></svg>
                    <h4>D-Value Boundary:</h4>
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
                <div v-show="selected_term !== null" class="nodeattributes">
                    <div class="name">
                        <span>Positive D-Value</span>
                    </div>
                    <div class="p">Proteins:</div>
                    <div class="link">
                        <ul>
                        <li class="membership" v-for="link in links">
                            <a href="#" v-on:click="select_node(link.id)">{{link.label}}</a>
                        </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    `
});
