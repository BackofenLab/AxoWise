Vue.component("theme-toggle",{
    data: function() {
        return {
            isActive: true
        }
    },
    methods: {
        toggleTheme: function () {
         var com = this;
         //change the theme property at root so children get it
         com.$parent.dark_theme_root = !com.isActive;
         com.isActive = !com.isActive
        },
        toggleClass: function () {
            this.isActive = !this.isActive;
        }
    },
    template: `
    <div id ="theme">
    <button @click="toggleTheme" style="height:50px;width:100px">Toggle</button>
    </div>
    `
});