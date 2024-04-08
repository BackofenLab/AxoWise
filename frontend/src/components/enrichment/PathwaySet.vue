<template>
    <div id="pathways-set">
        <div class="tool-section-graph">
            <div class="coloumn-button">
                <button class="tool-buttons" v-on:click="apply_enrichment()">generate set</button>
            </div>
            <div class="coloumn-button">
                <button class="tool-buttons" >placeholder</button>
            </div>
        </div>
        <div class="pathway-apply-section">
            
            <div class="sorting">
                <a class="enrichment_filter" >pathway layers </a>
            </div>
            
            <div v-if="await_load == true" class="loading_pane" ></div>
            <div class="results" tabindex="0" @keydown="handleKeyDown" ref="resultsContainer">
                <table >
                    <tbody>
                        <tr v-for="(entry) in set_dict" :key="entry" class="option">
                            <td>
                                <div class="favourite-symbol"  v-on:click="set_active(entry)">
                                <label class="custom-checkbox">
                                    <div class="active-image" :class="{ checked: entry.status}" ></div>
                                </label>
                                </div>
                            </td>
                            <td>
                                <div class="pathway-text">
                                    <input type="text" v-model="entry.name" class="empty"/>
                                    <span>({{entry.terms.length}})</span>
                                </div>
                            </td>
                            <td>
                                <div class="favourite-symbol">
                                <label class="custom-checkbox">
                                    <div class="delete-image"  v-on:click="remove_set(entry)"></div>
                                </label>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

    </div>
</template>

<script>

export default {
    name: 'PathwaySet',
    props: ['gephi_data','api'],
    emits: ['term_set_changed'],
    data() {
        return{
            set_dict: new Set(),
            layer: 0,
            await_load: false,
        }
    },
    methods: {
        apply_enrichment(){
            var com = this
            var genes = com.$store.state.active_subset

            if (!genes) return

            //Adding proteins and species to formdata 
            var formData = new FormData()
            formData.append('genes', genes)
            formData.append('species_id', com.gephi_data.nodes[0].species);

            this.await_load = true
            //POST request for generating pathways
            com.sourceToken = this.axios.CancelToken.source();
            com.axios
            .post(com.api.subgraph, formData, { cancelToken: com.sourceToken.token })
            .then((response) => {
                com.set_dict.add({"name": `layer ${com.layer}`, "genes": genes, "terms": response.data.sort((t1, t2) => t1.fdr_rate - t2.fdr_rate), "status": false})
                com.layer += 1
                this.await_load = false
            })
        },
        remove_set(entry){
            if(entry.status) this.emitter.emit('enrichTerms', null)
            this.set_dict.delete(entry)
        },
        set_active(entry){

            for (var layer of this.set_dict) { 
                if (layer != entry) layer.status = false;
            }
            
            if(!entry.status) {
                this.emitter.emit("searchSubset", {subset: this.activate_genes(entry.genes), mode: "protein"});
                this.emitter.emit('enrichTerms', entry.terms)
            }
            else {
                this.emitter.emit("searchSubset", {subset: null, mode: "protein"});
                this.emitter.emit('enrichTerms', null)
            }
            entry.status = !entry.status
        },
        activate_genes(genes){
            var com = this;
            var subset = []
            var genes_set = new Set(genes)

            com.gephi_data.nodes.forEach(node => {
                if(genes_set.has(node.attributes['Name'] )){
                    subset.push(node)
                }
            });

            return subset
        }
    }, 
}
</script>


<style>
    #pathways-set {
        width: 100%;
        height: 100%;
        cursor: default;
        font-family: 'ABeeZee', sans-serif;

    }

    .pathway-apply-section {
        width: 100%;
        height: 87.65%;
        border-radius: 5px;
        position: absolute;
    }

    .generate-set-button {
        display: inline-flex;
        margin: 1vw 0 1vw 0;
        height: 1vw;
        width: 100%;
        padding: 0 2vw 0 2vw;

    }

    .generate-set-button .export-text {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #0A0A1A;
        font-size: 0.7vw;
    }

    .pathway-apply-section a {
        color: white;
        text-decoration:none;
    }

    .pathway-apply-section .results {
        height: 100%;
        overflow: scroll;
    }
    .pathway-apply-section .sorting a{
        color: rgba(255, 255, 255, 0.7);
    }

    .option {
        display: -webkit-flex;
    }

    #pathways-set .pathway-text{
        width: 80%;
        display: flex;
        align-items: center;
        white-space: nowrap;
        overflow: hidden;    /* Hide overflow content */
        text-overflow: ellipsis;
        margin-left: 2%;
    }
    #pathways-set .pathway-text input[type=text] {
        width: 100%;
        font-size: 0.85vw;
        background: none;
        color: white;
        cursor: default;
        font-family: 'ABeeZee', sans-serif;
        border: none;
    }
    #pathways-set .pathway-text span{
        font-size: 0.7vw;
        margin-left: 4%;
        color: rgba(255, 255, 255, 0.7);
    }

    #pathways-set .pathway-text a {
        cursor: default;
    }

    /* bookmark styles */

    table {
        display: flex;
        width: 100%;
    }

    :focus {outline:0 !important;}

    table tbody{
        width: 100%;
    }
    .pathway-apply-section td:first-child {
    width: 15.41%;
    align-self: center;
    }
    .pathway-apply-section td:nth-child(2) {
    color: #FFF;
    font-size: 0.9vw;
    width: 88.55%;
    overflow: hidden;
    align-self: center;
    }
    .pathway-apply-section td:last-child {
    font-size: 0.9vw;
    color: white;
    width:  24.04%;
    align-self: center;
    }

    .favourite-symbol{
        width: 100%;
        height: 100%;
        justify-content: center;
        text-align: center;
        position: relative;
        display: flex;
        
    }
    .custom-checkbox {
        position: relative;
        display: inline-block;
        cursor: default;
    }

    .active-image {
        display: block;
        width: 0.9vw;
        height: 0.9vw;
        background-color: white;
        -webkit-mask: url(@/assets/pathwaybar/active.png) no-repeat center;
        mask: url(@/assets/pathwaybar/active.png) no-repeat center;
        mask-size: 0.9vw;
        background-repeat: no-repeat;
    }

    .delete-image {
        display: block;
        width: 0.9vw;
        height: 0.9vw;
        background-color: white;
        -webkit-mask: url(@/assets/pathwaybar/delete.png) no-repeat center;
        mask: url(@/assets/pathwaybar/delete.png) no-repeat center;
        mask-size: 0.9vw;
        background-repeat: no-repeat;
    }

    .checked {
        background-color: #ffa500;
    }

    .selected {
        background-color: rgba(255,0,0,0.7);
    }



</style>