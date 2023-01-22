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
        }
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
                </div>
            </div>
        </div>
    </div>
    `
});
