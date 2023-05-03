<template>
    <div class="label-switch">
        <input id="confirm" v-on:change="check()" type="checkbox" /><label for="confirm"></label>
    </div>
</template>

<script>
export default {
    name: 'ToggleLabel',
    data() {
        return {
        }
    },
    methods: {
      check() {
        this.emitter.emit("hideLabels", document.getElementById('confirm').checked);
      }

    }
}
</script>

<style>
.label-switch {
  position: absolute;
  bottom: 10px;
  right: 0px;
}


[type="checkbox"] {
  display: none;
  z-index: 0;
}
[type="checkbox"] + label {
  position: relative;
  display: block;
  cursor: pointer;
  font-family: sans-serif;
  font-size: 24px;
  line-height: 1.3;
  padding-left:70px;
  position: relative;
  margin-top: -30px;
}
[type="checkbox"] + label:before {
  width: 40px;
  height: 20px;
  border-radius: 30px;
  border: 2px solid #ddd;
  background-color: rgba(255, 255, 255, 0.2);
  content: "";
  margin-right: 15px;
  transition: background-color 0.5s linear;
  z-index: 5;
  position: absolute;
  left: 0px;
}
[type="checkbox"] + label:after {
  width: 20px;
  height: 20px;
  border-radius: 30px;
  background-color: #fff;
  content: "";
  transition: margin 0.1s linear;
  box-shadow: 0px 0px 5px #aaa;
  position: absolute;
  left: 2px;
  z-index: 10;
}
[type="checkbox"]:checked + label:before {
  background-color: #2b8718;
}
[type="checkbox"]:checked + label:after {
  margin: 0 0 0 20px;
}
</style>