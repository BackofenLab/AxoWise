<template>
    <div class="text" v-if="active_decoloumn !== null">
        <div class="headertext">
            <span>{{ active_decoloumn.toUpperCase() }}</span>
        </div>
        <div class="nodeattributes">
            <div class="p">
                <span>Statistics:</span>
                <button v-on:click="expand_proteins()" id="expand-btn">Expand</button>
            </div>
            <div class="p">
                <span>Connections:</span>
                <button v-on:click="copyclipboard()" id="copy-btn">Copy</button>
                <button v-on:click="expand_proteins()" id="expand-btn">Expand</button>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'DEValuePane',
    props: ['active_decoloumn','gephi_data'],
    emits: ['active_item_changed'],
    data() {
        return {
            links: null,
            hide: true,
            d_item: {
                value: null,
                imageSrc: require('@/assets/pane/d-icon.png')
            }
        }
    },
    watch: {
        active_decoloumn() {
            var com = this;

            
            if (com.active_decoloumn == null) {

                return;
            }

            this.d_item.value = com.active_decoloumn

            com.$emit('active_item_changed',{ "devalue": this.d_item })
            
        }
    },
    methods: {
        copyclipboard(){
            var com = this;

            var textToCopy = [];
            for(var link of com.links) textToCopy.push(link.label);
            navigator.clipboard.writeText(textToCopy.join("\n"));
        },
        expand_proteins() {
            
            const div = document.getElementById("link")

            if(div.style.visibility == "visible"){
                div.style.visibility = "hidden";
            }else{
                div.style.visibility = "visible";
            }
            
        }
    }
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