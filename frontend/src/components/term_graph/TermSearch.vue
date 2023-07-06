<template>
    <div id="enrichment" class="term-graph-pane">
            <div class="main-section">
                <div class="enrichment-filtering">
                    <input type="text" v-model="search_raw" class="empty"/>
                    <v-select id="vsel" placeholder="..." v-model="category" :options="filter_terms" :reduce="label => label.value" label="value" ></v-select>
                </div>
            <div class="results" v-if="term_data.nodes !== null">
                <select id ="result_select" size="11" @change="select_term($event.target.value)" @click="select_term($event.target.value)">
                <option v-for="entry in filtered_terms" :key="entry" :value="entry.id">{{ entry.label }}</option>
                </select>
                <div v-if="term_data.nodes == 0">
                    <i>No terms available.</i>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default{
        name: 'EnrichmentTool',
        props: ['term_data'],
        data() {
            return {
                terms: null,
                search_raw: "",
                filter_terms: this.$store.state.filter_terms,
                category: ""
            }
        },
        methods: {
            select_term(term) {
                var com = this;

                this.filtered_terms.forEach(entry => { if (entry.id === term) com.emitter.emit("searchTermNode", entry); });

            },
        },
        computed: {
            regex() {
                var com = this;
                return RegExp(com.search_raw.toLowerCase());
            },
            filtered_terms() {
                var com = this;
                var filtered = com.term_data.nodes;
                
                if (com.category) {
                // If category is set, filter by category
                filtered = filtered.filter(function(term) {
                    return term.attributes["Category"] === com.category;
                });
                }

                if (com.search_raw !== "") {
                // If search term is not empty, filter by search term
                var regex = new RegExp(com.regex, 'i');
                filtered = filtered.filter(function(term) {
                    return regex.test(term.label);
                });
                }

                filtered.sort((t1, t2) => t1.attributes['FDR'] - t2.attributes['FDR'] )

                return filtered;
            },

    },
}
</script>

<style >
.term-graph-pane {
	position: absolute;
	height: 90%;
	width: 300px;
	overflow: hidden;
	border-radius: 20px;
	word-wrap: break-word;
	padding: 2px;
	z-index: 1;
	color: white;
	transition: transform ease 500ms;
}

</style>