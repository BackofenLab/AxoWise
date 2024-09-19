<template>
  <div id="statistics">
    <div class="network-results" tabindex="0" @keydown="handleKeyDown">
      <table>
        <tbody>
          <tr
            v-for="(key, entry, index) in statistics"
            :key="index"
            class="option"
          >
            <td>
              <div class="statistics-attr">
                <a href="#">{{ entry }}</a>
              </div>
            </td>
            <td>
              <a class="statistics-val">{{ key }}</a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
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

<style></style>
