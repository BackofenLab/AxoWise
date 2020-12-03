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
         com.isActive = !com.isActive;
         if (com.isActive){
             document.getElementById('pgdb-app').classList.remove('white-theme')
             document.getElementById('pgdb-app').classList.add('black-theme')

             document.getElementById('left-control-panel').classList.remove('white-theme')
             document.getElementById('left-control-panel').classList.add('black-theme')
         }else {
             document.getElementById('pgdb-app').classList.remove('black-theme')
             document.getElementById('pgdb-app').classList.add('white-theme')

             document.getElementById('left-control-panel').classList.remove('black-theme')
             document.getElementById('left-control-panel').classList.add('white-theme')
         }

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