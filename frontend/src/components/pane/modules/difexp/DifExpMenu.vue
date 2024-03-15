<template>
    <div id="colorbar-difexp">
        <div class="tool-section-term">
            <div class="filter-section">
                <div id="pathway-filter" class="pre-full" v-on:click="handling_filter_menu()" :class="{ full: category_filtering == true }">
                    <span>{{ category }}</span>
                    <img  class="remove-filter" src="@/assets/pathwaybar/cross.png" v-on:click.stop="active_categories(null)" v-if="category !== 'Selection'">
                </div>
                <div id="pathway-filter-categories" v-show="category_filtering == true">
                        <div class="element" v-for="(entry, index) in dcoloumns" :key="index" v-on:click="active_categories(entry);" :class="{ active_cat: category == entry}">
                            <a>{{ entry }}</a>
                        </div>
                </div>
            </div>
        </div>
        <div class="list-section" v-if="active_decoloumn !== null">
            <svg id="demo1" width="250" height="120"></svg>
            <input id="legend"
            type="range"
            v-bind:min="dboundary.min"
            v-bind:max="dboundary.max"
            v-bind:step="dboundary.step"
            v-model="dboundary.value"
            v-on:change="check_boundary()"
            />
        </div>
    </div>
</template>

<script>
import * as d3 from "d3";
export default {
    name: 'DifExpMenu',
    props: ['active_decoloumn','gephi_data'],
    components:{
        
    },
    data() {
        return {
            active_section: '',
            links: null,
            hide: true,
            dcoloumns: this.$store.state.dcoloumns,
            category: "Selection",
            category_filtering: false,
            dboundary: {
                value: 1,
                min: 1,
                max: 10,
                step: 1
            },
            expand_selected: true,
        }
    },
    watch:{
        active_decoloumn(){
            console.log(this.active_decoloumn)
        }
    },
    methods: {
        active_categories(category){
            if (!category) {
                this.reset_categories()
                return
            }
            this.category = category
            this.emitter.emit("decoloumn", category);
        },
        reset_categories() {
            this.category = "Selection";
            this.emitter.emit("decoloumn", null);
        },
        change_section(bool, val){
            var com = this;
            if(com.active_section == val) {
                com.active_section = ''
                com.$emit('tool_active_changed',bool)
            }else
            {
                if(com.active_section == '') com.$emit('tool_active_changed',bool)
                com.active_section = val
            } 
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
        handling_filter_menu() {
            var com = this;
            if (!com.category_filtering) {
                com.category_filtering = true;

                // Add the event listener
                document.addEventListener('mouseup', com.handleMouseUp);
            }
            else{
                com.category_filtering = false;
                document.removeEventListener('mouseup', com.handleMouseUp);
            }

        },
        handleMouseUp(e) {
            var com = this;

            var container = document.getElementById('pathway-filter-categories');
            var container_button = document.getElementById('pathway-filter');
            if (!container.contains(e.target) && !container_button.contains(e.target)) {
                com.category_filtering = false;

                // Remove the event listener
                document.removeEventListener('mouseup', com.handleMouseUp);
            }
        }
    },
    mounted(){
        console.log(this.active_decoloumn)
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
        width: 100%;
        height: 100%;
        position: absolute;
        flex-shrink: 0;
        z-index: 999;
        
    }
    #colorbar-difexp .colorbar-text{
        width: 100%;
        background: rgb(74,45,255);
        background: linear-gradient(90deg, rgba(74,45,255,1) 0%, rgba(255,0,0,1) 100%);
        border-radius: 5px;
    }

    #legend{
        position: absolute;
        top: 7%;
        left: 30%;
        appearance: none;
        outline: none;
        width: 40%;
        height: 0.3vw;
        border-radius: 5px;
        background-color: #ccc;
    }
    
    #legend::-webkit-slider-thumb {
        background: #fafafa;
        appearance: none;
        box-shadow: 1px 2px 26px 1px #bdbdbd;
        width: 0.8vw;
        height: 0.8vw;
        border-radius: 50%;
    }

    #demo1 {
        position: absolute;
        display: block;
        width: 70%;
        height: 20%;
        left: 21%;
    }

    #colorbar-difexp .filter-section{
        width: 80%;
    }

    #colorbar-difexp #pathway-filter-categories{
        width: 80%;
    }

    #colorbar-difexp #pathway-filter-categories .element{
        padding: 0;
    }

</style>