<template>
  <div class="flex flex-col items-center justify-center text-center gap-4 px-4 py-7 text-slate-300">
    <span class="material-symbols-rounded text-slate-300 text-4xl"> event_list </span>
    <h6 class="text-base font-medium">{{ message }}</h6>

    <slot v-if="$slots.default"></slot>
  </div>
</template>

<script>
export default { name: "EmptyState", props: ["message"] };
</script>
