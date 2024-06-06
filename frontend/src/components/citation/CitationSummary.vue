<template>
    <div id="citation-tools" class="pathways">
        <div class="pathwaybar">
                <div class="summary-input">
                    <div class="window-label">gene search</div>
                    <textarea v-model="raw_text" rows="10" cols="30" autofocus></textarea>
                    <button v-on:click="summarize_abstracts(raw_text)">apply</button>
                </div>
                <div class="summarized">
                    <div class="window-label">summary</div>
                    <div class="summarized-abstracts">
                        <div v-if="await_load == true" class="loading_pane" ></div>
                        <div class="text" v-if="await_load == false">
                            {{ summary }}
                        </div>
                    </div>
                  
                </div>
        
        </div>
    </div>
</template>

<script>

export default {
    name: 'CitationSummary',
    props:['active_function','sorted','citation_data','node_index'],
    data() {
        return{
            raw_text:"",
            summary:"",
            api: {
                summary: "api/subgraph/summary",
            },
            abstractList: null,
            await_load: false
        }
    },
    methods:{
        add_abstract(id){
            this.raw_text = this.raw_text + `${this.raw_text.length != 0 ? "\n": ""}` + id
        },
        summarize_abstracts(abstracts){
            var com = this

            com.abstractList = {}
            for (var node of abstracts.split("\n")) {
                if(com.node_index[node]) com.abstractList[node]= com.node_index[node]
            }

            com.await_load = true
            var formData = new FormData()
            formData.append('abstracts', JSON.stringify(com.abstractList) )
        

            //POST request for generating pathways
            com.axios
            .post(com.api.summary, formData)
            .then((response) => {
                com.summary = response.data
                com.await_load = false
            })
        }

    },
    mounted(){
        this.emitter.on("addNodeToSummary", (id) => {
            this.add_abstract(id)
        });
    }
}
</script>


<style>

.summary-input{
    position: relative;
    padding: 1vw;
    width: 100%;
    height: 30%;
}
.summary-input textarea{
    margin-top: 3%;
    font-size: 0.9vw;
    width: 100%;
    color: white;
    background-color: rgba(255, 255, 255, 0.05);
    text-align: center;
    border: none;
    padding-top: 5%;
    resize: none;
    outline: none;
    height: 100%;
}
.summarized{
    position: relative;
    padding: 1vw;
    width: 100%;
    height: 70%;
}
.summarized-abstracts{
    color: white;
    font-family: 'ABeeZee', sans-serif;
    background-color: rgba(255, 255, 255, 0.05);
    font-size: 0.7vw;
    width: 100%;
    height: 90%;
    margin-top: 3%;
    overflow-y: scroll;
    padding: 1.3vw 1.3vw 0 1.3vw;
}
.summary-input button {
    position: absolute;
    right: 2vw;
    top: 0.8vw;
    position: absolute;
    display: block;
    cursor: pointer;
    border: none;
    color: white;
    border-style: solid;
    border-width: 1px;
    background: #0A0A1A;
    border-color: white;
    width: 3vw;
    font-size: 0.7vw;
}

</style>