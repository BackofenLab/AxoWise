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
            <div class="p">
                <span>Statistics:</span>
                <button v-on:click="expand_proteins()" id="expand-btn">Expand</button>
            </div>
            <div class="p">
                <span>Connections:</span>
                <button v-on:click="copyclipboard()" id="copy-btn">Copy</button>
                <button v-on:click="expand_proteins()" id="expand-btn">Expand</button>
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
        }
    },
    watch: {
        active_decoloumn() {
            var com = this;
            
            if (com.active_decoloumn == null) return;

            this.d_item.value = com.active_decoloumn
            com.$emit('active_item_changed',{ "devalue": this.d_item })
            
        }
    },
    methods: {
        copyclipboard(){
            var com = this;

            var textToCopy = [];
            for(var link of com.links) textToCopy.push(link.label);
            navigator.clipboard.writeText(textToCopy.join("\n"));
        },
        expand_proteins() {
            
            const div = document.getElementById("link")

            if(div.style.visibility == "visible"){
                div.style.visibility = "hidden";
            }else{
                div.style.visibility = "visible";
            }
            
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
        }
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