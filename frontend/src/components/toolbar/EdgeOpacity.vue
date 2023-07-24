<template>
    <div class="toolbar-connect">
        <span>opacity</span>
        <div class="boundary">
            <input id="opacity-slider"
                type="range"
                v-bind:min="opacity.min"
                v-bind:max="opacity.max"
                v-bind:step="opacity.step"
                v-model="opacity.value"
                v-on:change="change_opacity()"
            />
            <input id="opacity-input"
                type="number"
                v-bind:min="opacity.min"
                v-bind:max="opacity.max"
                v-bind:step="opacity.step"
                v-model="opacity.value"
                v-on:change="change_opacity()"
            />
        </div>
    </div>
</template>

<script>
export default {
    name: 'EdgeOpacity',
    data() {
        return {
			opacity: {
				value: 0.2,
				min: 0,
				max: 1,
				step: 0.1
			},
        }
    },
    methods: {
		change_opacity: function() {
			var com = this;

            this.emitter.emit("changeOpacity", com.opacity.value);
		},
	},
}
</script>

<style>
</style>