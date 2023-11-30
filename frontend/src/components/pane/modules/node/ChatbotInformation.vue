<template>
    <div id="chatbot">
        <div class="text">{{ protein_information }}</div>
    </div>
</template>

<script>

export default {
    name: 'ChatbotInformation',
    props: ['active_node'],
    data() {
        return {
            protein_information: "",
        }
    },
    watch:{
        active_node(){
            if (this.active_node == null) return
            this.protein_information = this.active_node.attributes['Description']
        },
    },
    methods:{

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

#chatbot .text {
    width: 100%;
    top: 16%;
    height: 80%;
    overflow-y: scroll;
    position: absolute;
    padding: 0 5% 0 2%;
}

.text::-webkit-scrollbar {
  display: none;
}

#chatbot #search-1 span,
#chatbot #search-2 span {
    margin-left: 10%;
    font-size: 0.6vw;

}

</style>