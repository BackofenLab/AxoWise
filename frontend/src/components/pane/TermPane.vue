<template>
    <div class="text" v-if="active_term !== null">
        <div class="headertext">
            <span>{{active_term.name}}</span>
        </div>
        <div class="nodeattributes">
            <div class="change-level-menu">
                <button id="down_level" v-on:click="change_level()">Apply</button>
                <button id="up_level" v-on:click="revert_level()">Revert</button>
            </div>
            <button class="go-button" v-on:click="to_term()">Go Term</button>
            <div class="p">
                <span>Statistics:</span>
                <button v-on:click="expand_stats = !expand_stats" id="expand-btn">Expand</button>
            </div>
                <div class="statistics" id="statistics" v-show="expand_stats === true">
                    <ul>
                        <li class="membership" v-for="(value, key) in statistics" :key="key" >
                            <span><strong>{{key}}: </strong>{{value}}</span>
                        </li>
                    </ul>
                </div>
            <div class="p">
            <span>Connections:</span>
            <button v-on:click="copyclipboard()" id="copy-btn">Copy</button>
            <button v-on:click="expand_proteins=!expand_proteins" id="expand-btn">Expand</button>
            </div>
            <div class="link" id="link" v-show="expand_proteins === true">
                <ul>
                    <li class="membership" v-for="link in links" :key="link" >
                        <a href="#" v-on:click="select_node(link)">{{link.label}}</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'TermPane',
    props: ['active_term','gephi_data'],
    emits: ['active_item_changed', 'highlight_subset_changed'],
    data() {
        return {
            links: null,
            term_history: [],
            statistics: {},
            expand_stats: false,
            expand_proteins: false,
            term_item: {
                value: null,
                imageSrc: require('@/assets/pane/enrichment-icon.png')
            }
        }
    },
    watch: {
        active_term() {
            var com = this
            if (com.active_term == null) {

                return;
            }
            const { category, id, fdr_rate, p_value } = com.active_term;
            com.statistics = { category, id, fdr_rate, p_value }

            com.term_item.value = com.active_term
            com.$emit('active_item_changed',{ "term": com.term_item })

            const activeTermProteins = new Set(com.active_term.proteins);
            com.links = com.gephi_data.nodes.filter(node => activeTermProteins.has(node.id));

        }
    },
    methods: {
        copyclipboard(){
            var com = this;

            var textToCopy = [];
            for(var link of com.links) textToCopy.push(link.label); 
            navigator.clipboard.writeText(textToCopy.join("\n"));
        },
        change_level() {
            var com = this;

            this.emitter.emit("enrichTerms", com.active_term.proteins);
        },
        revert_level() {

            this.emitter.emit("enrichTerms", null);

        },
        to_term(){
            var com = this;
            this.$store.commit('assign_active_enrichment_node', com.active_term)
            this.$router.push("terms")
        },
        select_node(value) {
            this.emitter.emit("searchNode", value);
        },
    }
}
</script>

<style>
    #termpane {
        visibility: hidden;
    }
    .pane-show {
        transform: translateX(326px);
    }
    .change-level-menu button{
        color: #fff;
        border-style: outset;
        border-width: 1px;
        border-radius: 20px;
        padding: 3px;
        background-color: rgba(0, 0, 0, 0.7);
        margin-bottom: 5px;
    }
    .go-button {
        color: #fff;
        border-style: outset;
        border-width: 1px;
        border-radius: 20px;
        padding: 3px;
        background-color: rgba(0, 0, 0, 0.7);
        margin-bottom: 5px;
    }

</style>