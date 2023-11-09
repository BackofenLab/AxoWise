<template>
    <div id="pathway-layer-connect">
        <div class="pane-sorting">
            <a class="pane_attributes" >pathway</a>
            <a class="pane_values">pathway</a>
        </div>

        <div class="network-results" tabindex="0" @keydown="handleKeyDown">
            <table >
                <tbody>
                    <tr v-for="entry in intersectingDicts" :key="entry" class="option">
                        <td>
                            <div class="statistics-attr">
                                <a href="#">{{entry[0].name}}</a>
                            </div>
                        </td>
                        <td>
                            <a class="statistics-val">{{entry[1].name}}</a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>

export default {
    name: 'EnrichmentConnections',
    props: ['active_termlayers','gephi_data'],
    components: {

    },
    data() {
        return {
            intersectingDicts: null
        }
    },
    watch: {
        active_termlayers: {
            handler(newList) {
            var com = this;

            if (newList == null) {
                return;
            }

            // Find intersecting dictionaries
            com.intersectingDicts = this.findIntersectingDictionaries(com.active_termlayers.main);

        },
        deep: true,
    },

    },
    methods: {

        findIntersectingDictionaries(mySet) {
            const result = [];
            const arr = Array.from(mySet);
            for (let i = 0; i < arr.length; i++) {
                for (let j = i + 1; j < arr.length; j++) {
                const dict1 = arr[i];
                const dict2 = arr[j];
                if (this.intersectingElements(dict1.proteins, dict2.proteins)) {
                    result.push([dict1, dict2]);
                }
                }
            }
            return result;
            },

            // Helper function to check if arrays have intersecting elements
            intersectingElements(arr1, arr2) {
            for (let i = 0; i < arr1.length; i++) {
                if (arr2.includes(arr1[i])) {
                return true;
                }
            }
            return false;
            }

    },
    
}
</script>

<style>
#pathway-layer-connect {
    width: 100%;
    height: 100%;
    top: 9.35%;
    position: absolute;
    font-family: 'ABeeZee', sans-serif;
    padding: 0% 2% 2% 2%;
}
#pathway-layer-connect .network-results {
    margin-top: 2%;
    height: 78%;
    overflow: scroll;
}
#pathway-layer-connect .pane_values{
    position: absolute;
    left: 50.5%;
}
#pathway-layer-connect .statistics-val{
    left: 50.6%;
}
#pathway-layer-connect .statistics-attr a{
    align-self: center;
    white-space: nowrap;
    overflow: hidden;    /* Hide overflow content */
    text-overflow: ellipsis;

}
#pathway-layer-connect .network-results td:first-child {
    margin-left: 0.5%;
    font-size: 0.7vw;
    margin-bottom: 1%;
    color: white;
    width:  50%;
    align-self: center;
    white-space: nowrap;
    overflow: hidden;    /* Hide overflow content */
    text-overflow: ellipsis;
}
#pathway-layer-connect .network-results td:last-child {
    font-size: 0.7vw;
    margin-bottom: 1%;
    color: white;
    width:  50%;
    align-self: center;
    white-space: nowrap;
    overflow: hidden;    /* Hide overflow content */
    text-overflow: ellipsis;
}
</style>