<template>
    <div class="pathways" :class="{ show_pathways_menu: pane_hidden === true }">
        <div class="minimize-bar" v-on:click="pane_hidden = !pane_hidden" >
            <img src="@/assets/pathwaybar/arrows.png" :style="{ transform: pane_hidden ? 'rotate(-90deg)' : 'rotate(90deg)' }">
        </div>
        <div class="pathwaybar" v-show="pane_hidden === false">
            <PathwayList
            :gephi_data='gephi_data'
            :terms='terms'
            :await_load = 'await_load'
            @favourite_pathways_changed = 'favourite_pathways = $event'
            @filtered_terms_changed = 'filtered_terms = $event'
            ></PathwayList>
            <PathwayTools
            :filtered_terms='filtered_terms'
            :favourite_pathways='favourite_pathways'
            ></PathwayTools>
            <img id="pathway-bg" src="@/assets/pathwaybar/background-dna.png">
        </div>
    </div>
</template>

<script>
import PathwayList from '@/components/enrichment/PathwayList.vue'
import PathwayTools from '@/components/enrichment/PathwayTools.vue'

export default {
    name: 'PathwayMenu',
    props: ['gephi_data','active_term'],
    components: {
        PathwayList,
        PathwayTools,
    },
    data() {
        return {
            api: {
                subgraph: "api/subgraph/enrichment",
            },
            terms: null,
            pane_hidden: false,
            await_load: false,
            terms_list: [],
            favourite_pathways: [],
            filtered_terms: []
        }
    },
    mounted() {
        var com = this
        com.generatePathways(com.gephi_data.nodes[0].species, com.gephi_data.nodes.map(node => node.id))

    },
    methods: {
        generatePathways(species, proteins){
            var com = this

            //Adding proteins and species to formdata 
            var formData = new FormData()
            formData.append('proteins', proteins)
            formData.append('species_id', species);
                
            this.await_load = true

            //POST request for generating pathways
            com.sourceToken = this.axios.CancelToken.source();
            com.axios
            .post(com.api.subgraph, formData, { cancelToken: com.sourceToken.token })
            .then((response) => {
                com.terms = response.data.sort((t1, t2) => t1.fdr_rate - t2.fdr_rate)
                com.terms_list.push(com.terms)
                com.await_load = false
            })

        },
        apply_layer(subset) {
            var com = this;
            com.generatePathways(com.gephi_data.nodes[0].species, subset)
        },
        revert_layer() {
            var com = this;

            if(com.await_load){
                com.abort_enrichment()
                return
            }

            if(com.terms_list.length > 1) {
                com.terms_list.pop()
                com.terms = com.terms_list[com.terms_list.length - 1 ];
            }

        },
        abort_enrichment() {
                this.sourceToken.cancel('Request canceled');
                this.await_load = false 
            },
    },
    created() {

        this.emitter.on("enrichTerms", (subset) => {
            if(subset != null) this.apply_layer(subset);
            else this.revert_layer();
        });

    }
}
</script>


<style>
    .pathways {
        z-index: 999;
        position: fixed;
        width: 92.97%;
        height: 27.2%;
        top: 70.7%;
        left: 50%;
        transform: translateX(-50%);
        transition: transform 330ms ease-in-out;
    }
    .minimize-bar {
        width: 100%;
        height: 9.41%;
        position: fixed;
        flex-shrink: 0;
        border-radius: 5px 5px 0px 0px;
        backdrop-filter: blur(7.5px);
        background: #D9D9D9;
        text-align: center;
    }
    .minimize-bar img {
        width: 0.7vw;
        height: 0.7vw;
        flex-shrink: 0;
        transition: transform 330ms ease-in-out;
    }
    .pathwaybar {
        width: 100%;
        height: 90.59%;
        position: fixed;
        top: 9.41%;
        flex-shrink: 0;
        border-radius: 0px 0px 5px 5px;
        background: rgba(222, 222, 222, 0.61);
        backdrop-filter: blur(7.5px);
    }
    .pathwaybar #pathway-bg {
        width: 20%;
        height: 100%;
        margin-left: 30.87%;
        position: absolute;
        top:50%;
        transform: translateY(-50%);
    }
    .show_pathways_menu {
        transform: translate(-50%,98%);
        width: 20%;
        transition: transform 330ms ease-in-out;
        transition: width 900ms ease-in-out;
    }

</style>