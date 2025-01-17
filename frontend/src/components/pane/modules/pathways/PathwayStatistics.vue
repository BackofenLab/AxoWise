<template>
  <ul class="list-none p-0 m-0 flex flex-col divide-y dark:divide-[#343b4c]">
    <li class="flex gap-1.5 py-1 dark:text-[#c3c3c3]" v-for="(key, entry, index) in statistics" :key="index">
      <strong class="flex-shrink-0 text-sm font-normal w-[20%] dark:text-slate-400">{{ entry }}</strong>
      <span class="flex-shrink-0 text-sm break-all w-[80%]">{{ key }}</span>
    </li>
  </ul>
</template>

<script>
export default {
  name: "PathwayStatistics",
  props: ["active_term"],
  data() {
    return {
      statistics: {},
    };
  },
  watch: {
    active_term() {
      var com = this;
      if (com.active_term == null) {
        return;
      }
      const { name, category, clean, fdr_rate, p_value } = com.active_term;
      com.statistics = { name, category, clean, fdr_rate, p_value };
    },
  },
};
</script>
