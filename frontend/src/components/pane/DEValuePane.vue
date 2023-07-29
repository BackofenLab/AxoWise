<template>
    <div class="text" v-if="active_decoloumn !== null">
        <div class="headertext">
            <span>{{ active_decoloumn.toUpperCase() }}</span>
        </div>
        <div class="nodeattributes">
            <div class="legend">
                <svg id="demo1" width="250" height="120"></svg>
                <div class="boundary">
                    <input id="dboundary-slider"
                    type="range"
                    v-bind:min="dboundary.min"
                    v-bind:max="dboundary.max"
                    v-bind:step="dboundary.step"
                    v-model="dboundary.value"
                    v-on:change="check_boundary()"
                    />
                    <input id="dboundary-input"
                    type="number"
                    v-bind:min="dboundary.min"
                    v-bind:max="dboundary.max"
                    v-bind:step="dboundary.step"
                    v-model="dboundary.value"
                    v-on:change="check_boundary()"
                    />
                </div>
            </div>
            <div class="selection">
                <span>Min</span>
                <input id="demin-input"
                type="number"
                v-bind:min="minSelect.min"
                v-bind:max="minSelect.max"
                v-bind:step="minSelect.step"
                v-model="minSelect.value"
                v-on:change="select_proteins()"
                /><br>
                <span>Max</span>
                <input id="demax-input"
                type="number"
                v-bind:min="maxSelect.min"
                v-bind:max="maxSelect.max"
                v-bind:step="maxSelect.step"
                v-model="maxSelect.value"
                v-on:change="select_proteins()"
                />
            </div>
            <div class="p">
            <span>Connections:</span>
            <button v-on:click="copyclipboard()" id="copy-btn">Copy</button>
            <button v-on:click="expand_selected = !expand_selected" id="expand-btn">Expand</button>
            </div>
            <div class="link" id="link" v-show="expand_selected === true">
                <ul>
                    <li class="membership" v-for="link in dvalueNodes" :key="link" >
                        <a href="#" v-on:click="select_node(link)">{{link.label}}</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
import * as d3 from "d3";
export default {
    name: 'DEValuePane',
    props: ['active_decoloumn','gephi_data'],
    emits: ['active_item_changed'],
    data() {
        return {
            links: null,
            hide: true,
            d_item: {
                value: null,
                imageSrc: require('@/assets/pane/d-icon.png')
            },
            dboundary: {
                value: 1,
                min: 1,
                max: 10,
                step: 1
            },
            minSelect: {
                value: -10,
                min: -10,
                max: 0,
                step: 0.1            },
            maxSelect: {
                value: 10,
                min: 0,
                max: 10,
                step: 0.1
            },
            expand_selected: true,
            dvalueNodes: []
        }
    },
    watch: {
        active_decoloumn() {
            var com = this;
            
            if (com.active_decoloumn == null) return;

            this.d_item.value = com.active_decoloumn
            com.dvalueNodes = this.gephi_data.nodes

            var dvalue_list = Object.values(com.gephi_data.nodes).map(item => item.attributes[com.active_decoloumn]).filter(value => value !== undefined)
            com.maxSelect.value = Math.max(...dvalue_list)
            com.minSelect.value = Math.min(...dvalue_list);

            com.$emit('active_item_changed',{ "devalue": this.d_item })
            
        }
    },
    methods: {
        copyclipboard(){
            var com = this;

            var textToCopy = [];
            for(var node of com.dvalueNodes) textToCopy.push(node.label);
            navigator.clipboard.writeText(textToCopy.join("\n"));
        },
        select_proteins() {

            this.dvalueNodes = []
            for (var node of this.gephi_data.nodes) {
                var dvalue = node.attributes[this.active_decoloumn]
                if (dvalue >= this.minSelect.value && dvalue <= this.maxSelect.value) this.dvalueNodes.push(node);
            }

            this.emitter.emit("selectDE", this.dvalueNodes);
            
        },
        draw_legend: function() {
            var com = this;

            var minB = - com.dboundary.value;
            var maxB = com.dboundary.value;
            var listB = [minB, minB/2, minB/4, 0, maxB/4, maxB/2, maxB]

            document.getElementById("demo1").innerHTML = "";
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
            com.draw_legend();
            com.emitter.emit("adjustDE", this.dboundary.value);
        },
        select_node(value) {
            this.emitter.emit("searchNode", value);
        },
    },
    updated() {
        if(this.active_decoloumn != null){
            this.draw_legend()
        }
    }
}
</script>

<style>
    #subsetpane {
        visibility: hidden;
    }
    .pane-show {
        transform: translateX(326px);
    }

    #hide-btn {
        position: relative;
        color: #fff;
        border-style: outset;
        border-width: 1px;
        border-radius: 20px;
        padding: 3px;
        background-color: rgba(0, 0, 0, 0.7);
        margin-bottom: 5px;
        justify-content: center;
    }

    .legend {
        padding: 20px;
        align-items: center;
        justify-content: center;
        display: block;
    }

</style>