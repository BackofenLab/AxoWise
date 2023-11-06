<template>
    <div class="text" v-show="active_decoloumn !== null">
        <div id="colorbar-difexp">
            <div class='colorbar-text' v-if="active_decoloumn !== null">
                {{active_decoloumn.toUpperCase()}}
            </div>
        </div>
        <div class="nodeattributes">
            <div id="legend" class="subsection">
                <div class="subsection-header">
                    <span>legend</span>
                </div>
                <div class="subsection-main">
                    <svg id="demo1" width="250" height="120"></svg>
                    <input
                    type="range"
                    v-bind:min="dboundary.min"
                    v-bind:max="dboundary.max"
                    v-bind:step="dboundary.step"
                    v-model="dboundary.value"
                    v-on:change="check_boundary()"
                    />
                </div>
            </div>
            <div id="pathway-connections" class="subsection">
                <div class="subsection-header">
                    <span>contained proteins</span>
                </div>
                <div class="subsection-main">
                    <RegulatedProteins
                    :active_decoloumn='active_decoloumn'
                    :gephi_data='gephi_data'
                    ></RegulatedProteins>
                </div>
            </div>
        </div>

        <!-- <div class="nodeattributes">
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
        </div> -->
    </div>
</template>

<script>
import RegulatedProteins from '@/components/pane/modules/difexp/RegulatedProteins.vue'
import * as d3 from "d3";
export default {
    name: 'DEValuePane',
    props: ['active_decoloumn','gephi_data'],
    emits: ['active_item_changed'],
    components:{
        RegulatedProteins
    },
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
            expand_selected: true,
        }
    },
    watch: {
        active_decoloumn() {
            var com = this;
            
            if (com.active_decoloumn == null) return;

            this.d_item.value = com.active_decoloumn

            com.$emit('active_item_changed',{ "Differential expression": this.d_item })
            
        }
    },
    methods: {
        copyclipboard(){
            var com = this;

            var textToCopy = [];
            for(var node of com.dvalueNodes) textToCopy.push(node.label);
            navigator.clipboard.writeText(textToCopy.join("\n"));
        },
        draw_legend: function() {
            var com = this;

            var minB = - com.dboundary.value;
            var maxB = com.dboundary.value;
            var listB = [minB, minB/2, minB/4, 0, maxB/4, maxB/2, maxB]
            var svgWidth = 125;
            var svgHeight = 100;

            document.getElementById("demo1").innerHTML = "";
            var svg = d3.select("#demo1")
            .attr("width", "100%")
            .attr("height", "100%")
            .attr("viewBox", `0 0 ${svgWidth*2} ${svgHeight}`);

            var xScale = d3.scaleLinear()
                            .domain(listB)
                            .range([10, 40, 70, 100, 130, 160, 190]);
            
            var xAxis = d3.axisBottom(xScale)
                        .tickValues(listB);
            
    
            svg.append("g")
                .attr("transform", "translate(0,68)")
                .attr("color","white")
                .call(xAxis);
            
            var colorScale = d3.scaleLinear()
                                .domain([minB, 0, maxB])
                                .range(["blue", "white", "red"]);

            var gradient = svg.append("defs")
            .append("linearGradient")
            .attr("id", "legendGradient")
            .attr("x1", "0%")
            .attr("x2", "100%");

            gradient.append("stop")
            .attr("offset", "0%")
            .attr("stop-color", colorScale(minB));

            gradient.append("stop")
            .attr("offset", "50%")
            .attr("stop-color", colorScale(0));

            gradient.append("stop")
            .attr("offset", "100%")
            .attr("stop-color", colorScale(maxB));

            // Create the legend bar using the linear gradient
            svg.append("rect")
            .attr("x", 10) // Adjust the x-coordinate to center it
            .attr("y", 50) // Adjust the y-coordinate to center it vertically
            .attr("width", 180)
            .attr("height", 15)
            .style("fill", "url(#legendGradient");


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
    #colorbar-difexp{
        position: relative;
        display: flex;
        border-radius: 5px;
        margin-top: 5%;
        width: 70%;
        color: white;
        align-items: center;
        text-align: center;
        justify-content: center;
        transform: translate(20%);
        font-family: 'ABeeZee', sans-serif;
        font-size: 0.9vw;
    }
    #colorbar-difexp .colorbar-text{
        width: 100%;
        background: rgb(74,45,255);
        background: linear-gradient(90deg, rgba(74,45,255,1) 0%, rgba(255,0,0,1) 100%);
        border-radius: 5px;
    }

    #legend {
        height: 25%;
    }

    #legend input[type=range]{
        position: absolute;
        top: 70%;
        left: 3vw;
        appearance: none;
        outline: none;
        width: 10vw;
        height: 0.3vw;
        border-radius: 5px;
        background-color: #ccc;
    }
    
    #legend input[type=range]::-webkit-slider-thumb {
        background: #fafafa;
        appearance: none;
        box-shadow: 1px 2px 26px 1px #bdbdbd;
        width: 0.8vw;
        height: 0.8vw;
        border-radius: 50%;
    }

    #demo1 {
        position: absolute;
        text-align: center;
        width: 100%;
    }

</style>