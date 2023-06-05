<template>
    <div class="graph-switch">
        <input id="switch" v-on:change="show_whole()" type="checkbox" /><label for="switch"></label>
    </div>
</template>

<script>

export default {
    name: 'ConnectedGraph',
    props: ['type'],
    data() {
        return {
        }
    },
    methods: {
        show_whole() {
            if(this.type == 'protein') this.emitter.emit("unconnectedGraph", document.getElementById('switch').checked);
            else this.emitter.emit("unconnectedTermGraph", document.getElementById('switch').checked)
                
        }
    }
}
</script>

<style>
.graph-switch {
  position: absolute;
  bottom: 40px;
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