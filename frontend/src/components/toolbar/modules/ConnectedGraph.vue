<template>
    <div class="tool-item">
        <span>Hide unconnected nodes</span>
        <input id="switch" v-on:change="show_whole()" type="checkbox" /><label for="switch"></label>
    </div>
</template>

<script>

export default {
    name: 'ConnectedGraph',
    props: ['mode'],
    data() {
        return {
        }
    },
    methods: {
        show_whole() {
          this.emitter.emit("unconnectedGraph", {check: document.getElementById('switch').checked,mode: this.mode});
                
        }
    }
}
</script>

<style>

#switch {
  margin-left: 5%;
}

[type="checkbox"] {
  display: none;
  z-index: 0;
}

[type="checkbox"] + label {
  display: block;
  cursor: pointer;
  font-family: sans-serif;
  font-size: 24px;
  line-height: 1.3;
  position: absolute;
  right: 15%;
  margin-top: 0.7%;
}
[type="checkbox"] + label:before {
  width: 1.8vw;
  height: 0.9vw;
  border-radius: 30px;
  background-color: #ddd;
  content: "";
  transition: background-color 0.5s linear;
  z-index: 5;
  position: absolute;
}
[type="checkbox"] + label:after {
  width: 0.7vw;
  height: 0.7vw;
  border-radius: 30px;
  background-color: #fff;
  content: "";
  transition: margin 0.1s linear;
  box-shadow: 0px 0px 5px #aaa;
  position: absolute;
  top:10%;
  margin: 0.1vw 0 0 0.1vw;
  z-index: 10;
}
.protein-view [type="checkbox"]:checked + label:before {
  background-color: #0A0A1A;
}
.term-view [type="checkbox"]:checked + label:before {
  background-color: #0a1a0b;
}
[type="checkbox"]:checked + label:after {
  margin: 0.1vw 0 0 1vw;
}
</style>