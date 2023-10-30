<template>
    <div id="chatbot">
        <div v-if="await_answer==true" class="loading_pane" ></div>
        <div v-if="await_answer==false">
            <div class="text">{{ protein_information }}</div>
            <div id="search-1" v-if="protein_information" v-on:click="ask_question(protein_questions[0])">
                <img class="search-field-icon" src="@/assets/toolbar/search.png">
                <span>{{ protein_questions[0] }}</span>
            </div>
            <div id="search-2" v-if="protein_information" v-on:click="ask_question(protein_questions[1])">
                <img class="search-field-icon" src="@/assets/toolbar/search.png">
                <span>{{ protein_questions[1] }}</span>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'ChatbotInformation',
    props: ['active_node'],
    data() {
        return {
            protein_information: "",
            protein_questions:"",
            await_answer:false,
            protein_name:''
        }
    },
    watch:{
        active_node(){
            this.protein_name = this.active_node.attributes["Name"]
            this.protein_information = ""
            this.generate_informations(`What is Gene/Protein ${this.protein_name} in 2 Sentences?`, false)
            this.generate_informations(`Give me 2 common corrolated questions to Gene ${this.protein_name} with maximum 7 Words!`, true)
            
        }
    },
    methods:{
        generate_informations(message, question){
            var com = this
            //Adding proteins and species to formdata 
            var formData = new FormData()
            formData.append('message', message)

            this.await_answer = true

            //POST request for generating pathways
            com.sourceToken = this.axios.CancelToken.source();
            com.axios
            .post("api/subgraph/chatbot", formData, { cancelToken: com.sourceToken.token })
            .then((response) => {
                if(!question) {
                    this.protein_information = response.data
                    this.await_answer = false
                }
                else this.protein_questions = response.data.split(/\d+\.\s+/).filter(question => question !== '');
            })
        },
        ask_question(message){
            this.generate_informations(`${message} in correlation with Gene ${this.protein_name}. Do a short answer` , false)
            this.generate_informations(`Give me 2 question with maximal 7 words correlated to your previous answer: ${this.protein_information}` , true)
        }
    }
}
</script>

<style>

#chatbot {
    font-family: 'ABeeZee', sans-serif;
    font-size: 0.7vw;
    width: 100%;
    height: 100%;
    position: absolute;
    padding: 0% 2% 2% 2%;
}

#chatbot .loading_pane {
    margin-top: 40%;
    
}

#chatbot .text {
    width: 100%;
    top: 16%;
    height: 50%;
    overflow-y: scroll;
    position: absolute;
    padding: 0 5% 0 2%;
}

.text::-webkit-scrollbar {
  display: none;
}


#chatbot #search-1 {
    position: absolute;
    top: 72%;
    width:100%;
}
#chatbot #search-2 {
    position: absolute;
    top: 84%;
    width:100%;
}

#chatbot #search-1 span,
#chatbot #search-2 span {
    margin-left: 10%;
    font-size: 0.6vw;

}

</style>