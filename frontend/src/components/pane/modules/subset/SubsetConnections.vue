<template>
    <div id="subset-connect" class="connect">
        <div class="sorting">
            <a class="node_filter" v-on:click="sort_node = (sort_node === 'asc') ? 'dsc' : 'asc'; sort_cluster = ''; sort_degree = '' " >nodes</a>
            <a class="cluster_filter" v-on:click="sort_cluster = (sort_cluster === 'asc') ? 'dsc' : 'asc'; sort_node = ''; sort_degree = '' " >cluster</a>
            <a class="degree_filter" v-on:click="sort_degree = (sort_degree === 'asc') ? 'dsc' : 'asc'; sort_cluster = ''; sort_node = '' " >degree</a>

        </div>

        <div class="network-results" tabindex="0" @keydown="handleKeyDown">
            <table >
                <tbody>
                    <tr v-for="(entry, index) in filt_links" :key="index" class="option">
                        <td>
                            <div class="statistics-attr">
                                <a href="#">{{entry.attributes["Name"]}}</a>
                            </div>
                        </td>
                        <td>
                            <a class="statistics-val">{{entry.attributes["Modularity Class"]}}</a>
                        </td>
                        <td>
                            <a class="statistics-val">{{entry.attributes["Degree"]}}</a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>

export default {
    name: 'SubsetConnections',
    props: ['active_subset'],
    data() {
        return {
            links: [],
            sort_node: "",
            sort_cluster: "",
            sort_degree: "",
        }
    },
    watch: {
        active_subset(){
            var com = this

            if (com.active_subset == null) {
                return;
            }

            com.links = com.active_subset

        }
    },
    computed: {
        filt_links() {
            var com = this;
            var filtered = com.links;

            if(com.sort_node == "asc"){
                filtered.sort(function(t1, t2) { 
                    return (t1.attributes["Name"].toLowerCase() > t2.attributes["Name"].toLowerCase() 
                    ? 1 : (t1.attributes["Name"].toLowerCase() === t2.attributes["Name"].toLowerCase() ? 0 : -1)) })
            }else if(com.sort_node == "dsc"){
                filtered.sort(function(t1, t2) { 
                    return (t2.attributes["Name"].toLowerCase() > t1.attributes["Name"].toLowerCase() 
                    ? 1 : (t1.attributes["Name"].toLowerCase() === t2.attributes["Name"].toLowerCase() ? 0 : -1)) })
            }

            if(com.sort_cluster == "asc"){
                filtered.sort((t1, t2) => t2.attributes["Modularity Class"] - t1.attributes["Modularity Class"])
            }else if (com.sort_cluster == "dsc"){
                filtered.sort((t1, t2) => t1.attributes["Modularity Class"] - t2.attributes["Modularity Class"])
            }

            if(com.sort_degree == "asc"){
                filtered.sort((t1, t2) => t2.attributes["Degree"] - t1.attributes["Degree"] )
            }else if (com.sort_degree == "dsc"){
                filtered.sort((t1, t2) => t1.attributes["Degree"]  - t2.attributes["Degree"] )
            }

            return new Set(filtered);
        },
    }
}
</script>

<style>
#subset-connect {
    width: 100%;
    height: 100%;
    font-family: 'ABeeZee', sans-serif;
    padding: 1.3vw 1.3vw 1vw 1.3vw;
}
</style>