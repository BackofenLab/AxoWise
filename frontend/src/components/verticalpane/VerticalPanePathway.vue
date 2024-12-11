<!-- <template>
  <div id="vertical-pane">
    <SearchField :data="term_data" :mode="mode"></SearchField>
    <div class="upper-block">
      <div class="tab-system">
        <ul>
          <li
            class="tab"
            :class="{ tabSelected: active_function_tab1 === 'set' }"
            v-on:click="active_function_tab1 = 'set'"
          >
            <a href="#">subset</a>
          </li>
        </ul>
      </div>
      <PathwayMenu
        v-show="active_function_tab1 == 'set'"
        :gephi_data="term_data"
        :sorted="'top'"
        :mode="mode"
        :active_function="active_function_tab1"
      ></PathwayMenu>
    </div>
    <div class="lower-block">
      <div class="tab-system">
        <ul>
          <li
            class="tab"
            :class="{ tabSelected: active_function_tab2 === 'list' }"
            v-on:click="active_function_tab2 = 'list'"
          >
            <a href="#">list</a>
          </li>
          <li
            class="tab"
            :class="{ tabSelected: active_function_tab2 === 'graph' }"
            v-on:click="active_function_tab2 = 'graph'"
          >
            <a href="#">enrichment</a>
          </li>
        </ul>
      </div>
      <PathwayGraphMenu
        :sorted="'bottom'"
        :term_data="term_data"
        :active_function="active_function_tab2"
      ></PathwayGraphMenu>
    </div>
  </div>
</template>

<script>
import PathwayGraphMenu from "@/components/pathwaytools/PathwayGraphMenu.vue";
import PathwayMenu from "@/components/enrichment/PathwayMenu.vue";
import SearchField from "@/components/interface/SearchField.vue";

export default {
  name: "VerticalPanePathway",
  props: ["term_data"],
  components: {
    PathwayGraphMenu,
    PathwayMenu,
    SearchField,
  },
  data() {
    return {
      active_function_tab1: "set",
      active_function_tab2: "list",
      mode: "term",
    };
  },
  mounted() {},
};
</script>

<style></style> -->
