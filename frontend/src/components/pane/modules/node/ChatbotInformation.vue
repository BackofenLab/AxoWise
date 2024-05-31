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
}
</script>

<style>

#chatbot {
    color: white;
    font-family: 'ABeeZee', sans-serif;
    font-size: 0.7vw;
    width: 100%;
    height: 100%;
    padding: 1vw 1.3vw 0 1.3vw;
}

#chatbot .text {
    width: 100%;
    height: 100%;
    overflow-y: scroll;
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