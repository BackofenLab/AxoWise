<template>
    <div :class="{ 'pathwaybar-small': pane_hidden === true, 'pathways': pane_hidden === false }">
        <div class="minimize-bar" v-on:click="pane_hidden = !pane_hidden" >
            <img src="@/assets/pathwaybar/fullscreen.png">
        </div>
        <div class="pathwaybar">
            <PathwayList
            :gephi_data='gephi_data'
            :terms='terms'
            :await_load = 'await_load'
            @favourite_pathways_changed = 'favourite_pathways = $event'
            @filtered_terms_changed = 'filtered_terms = $event'
            ></PathwayList>
            <PathwaySet v-show="pane_hidden === false"
            :gephi_data='gephi_data'
            :api='api'
            ></PathwaySet>
            <PathwayTools v-show="pane_hidden === false"
            :gephi_data='gephi_data'
            :filtered_terms='filtered_terms'
            :favourite_pathways='favourite_pathways'
            ></PathwayTools>
            <img v-show="pane_hidden === false" id="pathway-bg" src="@/assets/pathwaybar/background-dna.png">
        </div>
    </div>
</template>

<script>
import PathwayList from '@/components/enrichment/PathwayList.vue'
import PathwayTools from '@/components/enrichment/PathwayTools.vue'
import PathwaySet from '@/components/enrichment/PathwaySet.vue'

export default {
    name: 'PathwayMenu',
    props: ['gephi_data','active_term'],
    components: {
        PathwayList,
        PathwayTools,
        PathwaySet
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
    watch:{
        favourite_pathways: {
            handler(newList){
                this.emitter.emit('updateFavouriteList', newList)
            },
            deep: true
        },
    },
    mounted() {
        var com = this
        com.generatePathways(com.gephi_data.nodes[0].species, com.gephi_data.nodes.map(node => node.attributes["Name"]))

    },
    methods: {
        generatePathways(species, genes){
            var com = this

            //Adding proteins and species to formdata 
            var formData = new FormData()
            formData.append('genes', genes)
            formData.append('species_id', species);
                
            this.await_load = true

            //POST request for generating pathways
            com.sourceToken = this.axios.CancelToken.source();
            com.axios
            .post(com.api.subgraph, formData, { cancelToken: com.sourceToken.token })
            .then((response) => {
                com.terms = response.data.sort((t1, t2) => t1.fdr_rate - t2.fdr_rate)
                if (com.terms_list.length == 0) this.$store.commit('assign_current_enrichment_terms', com.terms)
                com.terms_list.push(com.terms)
                com.await_load = false
            })

        },
        abort_enrichment() {
                this.sourceToken.cancel('Request canceled');
                this.await_load = false 
            },
    },
    created() {

        this.emitter.on("enrichTerms", (terms) => {
            if(terms != null) this.terms = terms;
            else this.terms = this.terms_list[0];
            this.$store.commit('assign_current_enrichment_terms', this.terms)
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
        position: absolute;
        flex-shrink: 0;
        border-radius: 5px 5px 0px 0px;
        backdrop-filter: blur(7.5px);
        background: #D9D9D9;
        transition: transform 330ms ease-in-out;
    }

    .minimize-bar img{
        position: absolute;
        top: 35%;
        right: 0.7vw;
        width: 0.7vw;
        height: 0.7vw;
        flex-shrink: 0;
        transition: transform 330ms ease-in-out;
    }
    .pathwaybar {
        width: 100%;
        height: 90.59%;
        position: absolute;
        top: 9.41%;
        flex-shrink: 0;
        border-radius: 0px 0px 5px 5px;
        background: rgba(222, 222, 222, 0.61);
        backdrop-filter: blur(7.5px);
    }
    .pathwaybar-small{
        z-index: 999;
        position: absolute;
        width: 32.83%;
        height: 27.2%;
        top: 70.7%;
        left: 3.515%;
        transition: transform 330ms ease-in-out;
    }
    .pathwaybar #pathway-bg {
        width: 20%;
        height: 100%;
        margin-left: 30.87%;
        position: absolute;
        top:50%;
        transform: translateY(-50%);
    }

</style>