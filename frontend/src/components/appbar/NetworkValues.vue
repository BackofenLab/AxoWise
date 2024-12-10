<template>
  <ul class="flex flex-col text-xs">
    <li class="flex"><span class="w-[40px]">Nodes</span> {{ data.nodes.length }}</li>
    <li class="flex"><span class="w-[40px]">Edges</span> {{ data.edges.length }}</li>
  </ul>
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

