<template>
    <div class="toolbar-connect">
        <span>opacity</span>
        <div class="boundary">
            <span>BG</span>
            <input id="opacity-b-slider"
                type="range"
                v-bind:min="opacityBackground.min"
                v-bind:max="opacityBackground.max"
                v-bind:step="opacityBackground.step"
                v-model="opacityBackground.value"
                v-on:change="change_opacity('background')"
            />
            <input id="opacity-b-input"
                type="number"
                v-bind:min="opacityBackground.min"
                v-bind:max="opacityBackground.max"
                v-bind:step="opacityBackground.step"
                v-model="opacityBackground.value"
                v-on:change="change_opacity('background')"
            /><br>
            <span>HS</span>
            <input id="opacity-h-slider"
                type="range"
                v-bind:min="opacityHighlight.min"
                v-bind:max="opacityHighlight.max"
                v-bind:step="opacityHighlight.step"
                v-model="opacityHighlight.value"
                v-on:change="change_opacity('highlight')"
            >
            <input id="opacity-h-input"
                type="number"
                v-bind:min="opacityHighlight.min"
                v-bind:max="opacityHighlight.max"
                v-bind:step="opacityHighlight.step"
                v-model="opacityHighlight.value"
                v-on:change="change_opacity('highlight')"
            />
        </div>
    </div>
</template>

<script>
export default {
    name: 'EdgeOpacity',
    data() {
        return {
			opacityBackground: {
				value: 0.2,
				min: 0,
				max: 1,
				step: 0.1
			},
			opacityHighlight: {
				value: 0.2,
				min: 0,
				max: 1,
				step: 0.1
			},
        }
    },
    methods: {
		change_opacity(layer) {
			var com = this;
            var edgeOpacity = layer === 'highlight' ? com.opacityHighlight.value : com.opacityBackground.value;
            
            this.emitter.emit("changeOpacity", {'opacity': edgeOpacity, 'layers': layer});
		},
	},
}
</script>

<style>
</style>