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
            <button id="go-button" v-on:click="to_term()">Go Term</button>
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
            expand_proteins: false
        }
    },
    watch: {
        active_term() {
            var com = this
            if (com.active_term == null) {

                return;
            }

            com.$emit('active_item_changed',{ "term": com.active_term })

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

            com.term_history.push(com.active_term.proteins)
            com.$emit('highlight_subset_changed', com.active_term.proteins)
        },
        revert_level() {
            var com = this;

            com.term_history.pop()
            let last_term = com.term_history[com.term_history.length - 1];

            if(last_term == null) {
                com.$emit('highlight_subset_changed', null)
                return
            }

            com.$emit('highlight_subset_changed', last_term)
        },
        to_term(){
            var com = this;
            this.$store.commit('assign_active_enrichment_node', com.active_term)
            this.$router.push("terms")
        },
        select_node(value) {
            this.emitter.emit("searchNode", value);
        }
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
    #go-button {
        color: #fff;
        border-style: outset;
        border-width: 1px;
        border-radius: 20px;
        padding: 3px;
        background-color: rgba(0, 0, 0, 0.7);
        margin-bottom: 5px;
    }

</style>