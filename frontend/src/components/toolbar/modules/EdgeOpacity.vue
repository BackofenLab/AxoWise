<template>
    <div>
        <div class="tool-item">
                <span>Background edge opacity</span>
                <input class="opacity-input"
                    type="number"
                    v-bind:min="opacityBackground.min"
                    v-bind:max="opacityBackground.max"
                    v-bind:step="opacityBackground.step"
                    v-model="opacityBackground.value"
                    v-on:change="change_opacity('background')"
                />
        </div>
        <div class="tool-item">
            <span>Highlighted edge opacity</span>
            <input class="opacity-input"
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
input[type=number] { 
    position: absolute;
    margin-top:0.1vw;
    right: 6.3%;
    width: 9%;
    border-radius: 5px;
    border: none;
    height: 6%;
    font-family: 'ABeeZee', sans-serif;
    font-size: 0.7vw;
    color:  #0A0A1A;
    background-color: #ddd;
    -moz-appearance: textfield;
    appearance: textfield;
    text-align: center;
}

input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button { 
      -webkit-appearance: none; 
      margin: 0; 
}

</style>