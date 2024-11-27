<template>
  <header
    class="flex items-center flex-wrap sticky top-0 gap-2 py-3 bg-[var(--card-bg)] shadow-curve-dark dark:shadow-curve-light z-[2]"
  >
    <h5 v-if="title" class="mb-0 mr-auto">{{ title }}</h5>

    <slot v-if="$slots.default"></slot>
  </header>
</template>

<script>
export default { name: "ListActionHeader", props: ["title"] };
</script>
