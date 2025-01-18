<template>
  <ul class="flex items-center gap-2 p-0 m-0 list-none">
    <li>
      <Button type="button" plain text @click="onThemeToggler">
        <span :class="`material-symbols-rounded dark:text-white`">{{ iconClass }}</span>
      </Button>
    </li>
  </ul>
</template>

<script>
export default {
  data() {
    return {
      iconClass: "dark_mode",

    };
  },
  methods: {
    onThemeToggler() {
      const root = document.getElementsByTagName("html")[0];
      root.classList.toggle("p-dark");
      this.iconClass = this.iconClass === "dark_mode" ? "light_mode" : "dark_mode";
    },
  }
};
</script>
