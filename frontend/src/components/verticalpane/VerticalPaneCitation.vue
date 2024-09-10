<template>
  <div id="vertical-pane" :class="{ chatbot: chatbotactive }">
    <div class="upper-block">
      <div class="tab-system">
        <ul>
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
          <li
            class="tab"
            :class="{ tabSelected: active_function_tab1 === 'chatbot' }"
            v-on:click="active_function_tab1 = 'chatbot'"
          >
            <a href="#">chatbot</a>
          </li>
        </ul>
      </div>
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
      <CitationSummary
        v-show="active_function_tab1 === 'chatbot'"
        :citation_data="citation_data"
        :node_index="node_index"
        :await_community="await_community"
        @await_community_changed="await_community = $event"
        :sorted="'top'"
      ></CitationSummary>
    </div>
  </div>
</template>

<script>
import CitationList from "@/components/citation/CitationList.vue";
import CitationCommunities from "@/components/citation/CitationCommunities.vue";
import CitationSummary from "@/components/citation/CitationSummary.vue";

export default {
  name: "VerticalPaneCitation",
  props: ["citation_data", "node_index", "chatbotactive"],
  emits: ["chatbotactive_changed"],
  components: {
    CitationList,
    CitationSummary,
    CitationCommunities,
  },
  data() {
    return {
      active_function_tab1: "list",
      active_function_tab2: "summary",
      await_community: false,
    };
  },
  watch: {
    active_function_tab1() {
      this.active_function_tab1 == "chatbot"
        ? this.$emit("chatbotactive_changed", true)
        : this.$emit("chatbotactive_changed", false);
    },
  },
};
</script>

<style>
.citation-view .upper-block {
  height: 99%;
}

#vertical-pane.chatbot {
  width: 35%;
  transition: width 0.5s ease-in-out;
}

#vertical-pane {
  transition: width 0.5s ease-in-out;
}
</style>
