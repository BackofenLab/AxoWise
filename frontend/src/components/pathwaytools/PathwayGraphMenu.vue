<template>
    <div class="pathways" :class="{ show_pathways_menu: pane_hidden === true }">
        <div class="minimize-bar" v-on:click="pane_hidden = !pane_hidden" >
            <img src="@/assets/pathwaybar/arrows.png" :style="{ transform: pane_hidden ? 'rotate(-90deg)' : 'rotate(90deg)' }">
        </div>
        <div class="pathwaybar" v-show="pane_hidden === false">
            <PathwayGraphList
            :term_data='term_data'
            :terms='terms'
            :await_load = 'await_load'
            @favourite_pathways_changed = 'favourite_pathways = $event'
            @filtered_terms_changed = 'filtered_terms = $event'
            ></PathwayGraphList>
            <img id="pathway-bg" src="@/assets/pathwaybar/background-dna.png">
        </div>
    </div>
</template>

<script>
import PathwayGraphList from '@/components/pathwaytools/PathwayGraphList.vue'

export default {
    name: 'PathwayMenu',
    props: ['term_data','active_term'],
    components: {
        PathwayGraphList,
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
        console.log(this.term_data)
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
                this.emitter.emit("generateGraph", com.terms);
            })

        },
        abort_enrichment() {
                this.sourceToken.cancel('Request canceled');
                this.await_load = false 
            },
    },
}
</script>


<style>
</style>