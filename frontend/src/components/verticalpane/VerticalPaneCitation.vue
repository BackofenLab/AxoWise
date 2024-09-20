<template>
  <div id="vertical-pane">
    <SearchField 
    :data="citation_data"
    :mode="mode"
    ></SearchField>
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
          <li
            class="tab"
            :class="{ tabSelected: active_function_tab1 === 'list' }"
            v-on:click="active_function_tab1 = 'list'"
          >
            <a href="#">list</a>
          </li>
          <li
            class="tab"
            :class="{ tabSelected: active_function_tab1 === 'clist' }"
            v-on:click="active_function_tab1 = 'clist'"
          >
            <a href="#">communities</a>
          </li>
        </ul>
      </div>
      <PathwayMenu
        v-show="active_function_tab1 == 'set'"
        :gephi_data="citation_data"
        :mode="mode"
        :sorted="'top'"
        :active_function="active_function_tab1"
      ></PathwayMenu>
      <CitationList
        v-show="active_function_tab1 === 'list'"
        :citation_data="citation_data"
        :sorted="'top'"
      ></CitationList>
      <CitationCommunities
        v-show="active_function_tab1 === 'clist'"
        :citation_data="citation_data"
        :sorted="'top'"
        :await_community="await_community"
      ></CitationCommunities>
    </div>
    <div class="lower-block">
      <div class="tab-system">
        <ul>
          <li
            class="tab"
            :class="{ tabSelected: active_function_tab2 === 'summary' }"
            v-on:click="active_function_tab2 = 'summary'"
          >
            <a href="#">summary</a>
          </li>
        </ul>
      </div>
      <CitationSummary
        :citation_data="citation_data"
        :node_index="node_index"
        :await_community="await_community"
        @await_community_changed="await_community = $event"
        :sorted="'bottom'"
      ></CitationSummary>
    </div>
  </div>
</template>

<script>
import CitationList from "@/components/citation/CitationList.vue";
import CitationCommunities from "@/components/citation/CitationCommunities.vue";
import CitationSummary from "@/components/citation/CitationSummary.vue";
import PathwayMenu from "@/components/enrichment/PathwayMenu.vue";
import SearchField from "@/components/interface/SearchField.vue";

export default {
  name: "VerticalPaneCitation",
  props: ["citation_data", "node_index"],
  components: {
    CitationList,
    CitationSummary,
    CitationCommunities,
    PathwayMenu,
    SearchField
  },
  data() {
    return {
      active_function_tab1: "set",
      active_function_tab2: "summary",
      await_community: false,
      mode: "citation",
    };
  },
};
</script>

<style></style>
