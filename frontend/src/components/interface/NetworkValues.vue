<template>
    <div id="network-values">
        <div class="value-text">nodes: {{ gephi_data.nodes.length }}</div>
        <div class="value-text">edges: {{ gephi_data.edges.length }}</div>
    </div>
</template>

<script>
export default {
    name: 'NetworkValues',
    props: ['gephi_data'],
    data() {
        return {
        }
    },
}
</script>

<style>
#network-values {
    width: 5%;
    height: 3.98%;
    left: 26%;
    display: flex;
    flex-direction: column; /* Display items in a column */
    justify-content: center; /* Center vertically */
    position: absolute;
    border-radius: 5px;
    backdrop-filter: blur(7.5px);
}

#network-values .value-text {
    font-family: 'ABeeZee', sans-serif;
    font-size: 0.7vw;
    color: #D9D9D9;
    text-align: center; /* Optional: Center text within the container */
}

</style>
