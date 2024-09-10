<template>
  <div id="network-values">
    <div class="value-text">nodes: {{ data.nodes.length }}</div>
    <div class="value-text">edges: {{ data.edges.length }}</div>
  </div>
</template>

<script>
export default {
  name: "NetworkValues",
  props: ["data"],
  data() {
    return {};
  },
};
</script>

<style>
#network-values {
  width: 5%;
  height: 3.98%;
  left: 25vw;
  bottom: 1vw;
  display: flex;
  flex-direction: column;
  justify-content: center;
  position: absolute;
  /* border-radius: 5px; */
  -webkit-backdrop-filter: blur(7.5px);
  transition: left 0.5s ease-in-out;
}

#network-values .value-text {
  font-family: "ABeeZee", sans-serif;
  font-size: 0.7vw;
  color: #d9d9d9;
  text-align: center; /* Optional: Center text within the container */
}
</style>
