<template>
  <li class="flex flex-col gap-2 py-2 dark:text-[#c3c3c3]">
    <div class="flex items-center justify-between gap-2">
      Background edge opacity
      <InputNumber :min="opacityBackground.min" :max="opacityBackground.max" :step="opacityBackground.step"
        v-model="opacityBackground.value" @value-change="change_opacity('background')"
        inputClass="w-12 h-8 text-center" />
    </div>
    <Slider class="mx-1 mt-3 mb-3" :min="opacityBackground.min" :max="opacityBackground.max"
      :step="opacityBackground.step" v-model="opacityBackground.value" />
  </li>
  <li class="flex flex-col gap-2 py-2 dark:text-[#c3c3c3]">
    <div class="flex items-center justify-between gap-2">
      Highlighted edge opacity
      <InputNumber :min="opacityHighlight.min" :max="opacityHighlight.max" :step="opacityHighlight.step"
        v-model="opacityHighlight.value" @value-change="change_opacity('highlight')" inputClass="w-12 h-8 text-center" />
    </div>
    <Slider class="mx-1 mt-3 mb-3" :min="opacityHighlight.min" :max="opacityHighlight.max" :step="opacityHighlight.step"
      v-model="opacityHighlight.value" />
  </li>
</template>

<script>
export default {
  name: "EdgeOpacity",
  props: ["mode"],
  data() {
    return {
      opacityBackground: {
        value: 0.2,
        min: 0,
        max: 1,
        step: 0.1,
      },
      opacityHighlight: {
        value: 0.2,
        min: 0,
        max: 1,
        step: 0.1,
      },
    };
  },
  methods: {
    change_opacity(layer) {
      var com = this;
      var edgeOpacity =
        layer === "highlight"
          ? com.opacityHighlight.value
          : com.opacityBackground.value;
      this.emitter.emit("changeOpacity", {
        value: { opacity: edgeOpacity, layers: layer },
        mode: this.mode,
      });
    },
  },
};
</script>
