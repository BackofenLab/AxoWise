<template>
    <div id="search" class="toolbar-search">
        <div class="search-field">
        <input type="text" value="Search nodes by name" class="search_empty"/>
        </div>
        <div class="results">
            <i v-if="message.length > 0">{{message}}</i>
            <div v-for="entry in matches" :key="entry">
                <a href="#" v-on:click="select_node(entry)">{{entry.attributes['Name']}}</a>
            </div>
            <div v-if="matches.length == 0">
                <i>No results found.</i>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'SearchBar',
    props: ['gephi_data'],
    emits: ['active_node_changed'],
    data() {
        return {
            input: null,
            state: null,
            results: null,
            exactMatch: false,
            lastSearch: "",
            searching: false,
            matches: [],
            message: "",
            search_check: false
        }
    },
    methods: {

        select_node(node) {

            this.emitter.emit("searchNode", node);
        },
        close() {
            var com = this

            com.results.style.display = "none";
            com.searching = false;
            com.input.value = "";
            com.select_node(null);
        },
        clean() {
            var com = this;

            com.results.style.display = "none";
            com.input.value = "";
        },
        search(query) {
            var com = this;

                com.matches = [];
                com.message = "";
                com.searching = true;
                com.lastSearch = query;
                com.results.style.display = "block";

                const regex = new RegExp(com.exactMatch ? ("^" + query + "$").toLowerCase() : query.toLowerCase());

                if (query.length < 3) {
                    com.message = "Minimum 3 letters required.";
                    return;
                }

                com.gephi_data.nodes.forEach((n) => {
                    if (regex.test(n.attributes['Name'].toLowerCase())) {
                        com.matches.push(n);
                    }
                });

                if (com.matches.length == 1) {
                    this.emitter.emit("searchNode", com.matches[0]);
                }
            }

    },
    mounted() {
        var com = this;

        var a = document.querySelector("#search");
        com.input = a.querySelector("input");
        com.state = a.querySelector(".state");
        com.results = a.querySelector(".results");

        var debounceTimer;

        com.input.addEventListener('focus', function () {
            var a = this;
            a.dataset.focus || (a.dataset.focus = true, a.classList.remove("empty"));
            com.clean()
        });

        com.input.addEventListener('keydown', function (a) {
            if (13 == a.which) {
                clearTimeout(debounceTimer);
                debounceTimer = setTimeout(function() {
                    com.search(com.input.value);
                }, 500);
                return false;
            }
        });


    },
}
</script>

<style>

</style>
