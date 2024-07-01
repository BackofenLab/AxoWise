<template>
  <div id="statistics">
    <div class="pane-sorting">
      <a class="pane_attributes">source</a>
      <a class="pane_values">target</a>
    </div>

    <div class="network-results" tabindex="0" @keydown="handleKeyDown">
      <table>
        <tbody>
          <tr
            v-for="(key, entry, index) in contained_edges"
            :key="index"
            class="option"
          >
            <td>
              <div class="statistics-attr">
                <a href="#">{{ key.source[1] }}</a>
              </div>
            </td>
            <td>
              <a class="statistics-val">{{ key.target[1] }}</a>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: "SubsetLinks",
  props: ["contained_edges"],
  data() {
    return {};
  },
  watch: {},
};
</script>

<style></style>
