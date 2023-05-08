<template>
    <div class="text" v-if="active_subset !== null">
        <div class="headertext">
            <span>Subset</span>
        </div>
        <div class="nodeattributes">
            <div class="p">
                <span>Connections:</span>
                <button v-on:click="copyclipboard()" id="copy-btn">Copy</button>
                <button v-on:click="expand_proteins=!expand_proteins" id="expand-btn">Expand</button>
            </div>
            <div class="link" id="link" v-show="expand_proteins === true">
                <ul>
                    <li class="membership" v-for="link in active_subset" :key="link" >
                        <a href="#" v-on:click="select_node(link)">{{link.label}}</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'TermSubsetPane',
    props: ['active_subset'],
    emits: ['active_item_changed', 'highlight_subset_changed'],
    data() {
        return {
            hide: true,
            expand_proteins: false,
            subset_item: {
                value: null,
                imageSrc: require('@/assets/pane/cluster-icon.png')
            }
        }
    },
    watch: {
        active_subset() {
            var com = this;
            
            if (com.active_subset == null) {

                return;
            }

            com.subset_item.value = com.active_subset

            com.$emit('active_item_changed',{ "subset": com.subset_item })
            
        }
    },
    methods: {
        copyclipboard(){
            var com = this;

            var textToCopy = [];
            for(var link of com.links) textToCopy.push(link.label);
            navigator.clipboard.writeText(textToCopy.join("\n"));
        },
        select_node(value) {
            this.emitter.emit("searchTermNode", value);
        }
    },
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

</style>