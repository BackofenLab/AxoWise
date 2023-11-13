<template>
    <div id="pathways-set">
        <div class="generate-set-button">
            <div class="export-text" v-on:click="apply_enrichment()">Generate pathway set</div>
        </div>
        <div class="pathway-apply-section">

            <div class="sorting">
                <a class="enrichment_filter" >pathway layers </a>
            </div>

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
                                    <a href="#">{{entry.name}}</a>
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
            layer: 0
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

            //POST request for generating pathways
            com.sourceToken = this.axios.CancelToken.source();
            com.axios
            .post(com.api.subgraph, formData, { cancelToken: com.sourceToken.token })
            .then((response) => {
                com.set_dict.add({"name": `layer ${com.layer}`, "genes": genes, "terms": response.data.sort((t1, t2) => t1.fdr_rate - t2.fdr_rate), "status": false})
                com.layer += 1
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
            if(!entry.status) this.emitter.emit('enrichTerms', entry.terms)
            else this.emitter.emit('enrichTerms', null)
            entry.status = !entry.status
        }
    }, 
}
</script>


<style>
    #pathways-set {
        width: 11.8%;
        height: 96.92%;
        position: absolute;
        top:50%;
        transform: translateY(-50%);
        margin-left: 35%;
        border-radius: 10px;
        z-index: 1;
        font-family: 'ABeeZee', sans-serif;

    }

    .pathway-apply-section {
        width: 100%;
        height: 87.65%;
        top: 12.35%;
        border-radius: 5px;
        background: #0A0A1A;
        position: absolute;
        padding: 0% 2% 2% 2%;
    }

    .generate-set-button {
        width: 100%;
        height: 10.00%;
        left: 0%;
        bottom: 0;
        position: absolute;
        border-radius: 0 0 5px 5px;
        background: #D9D9D9;
        cursor: default;
        z-index: 100;

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
        height: 9.5vw;
        overflow: scroll;
    }
    .pathway-apply-section .sorting {
        width: 7.9vw;
    }
    .pathway-apply-section .sorting a{
        color: rgba(255, 255, 255, 0.7);
    }

    .option {
        display: -webkit-flex;
    }

    .pathway-text{
        width: 92%;
        display: flex;
        align-items: center;
        white-space: nowrap;
        overflow: hidden;    /* Hide overflow content */
        text-overflow: ellipsis;
        margin-left: 2%;
    }
    .pathway-text span{
        font-size: 0.7vw;
        margin-left: 4%;
        color: rgba(255, 255, 255, 0.7);
    }

    .pathway-text a {
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