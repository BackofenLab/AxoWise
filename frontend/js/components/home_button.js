Vue.component("home_button",  {
    props: ["gephi_json"],
    mounted: function() {
        var com = this;
        $("#home_button").click(() => com.select_node());
    },
    methods: {
        select_node: function() {
            var com = this;
            location.reload();
            com.$emit("gephi-json-changed", null);
            
        },
    },
    template: `
        <div class="home-button" id="home_button">
            <img src="images/logo-white.png" alt="logo">
        </div>
    `
});