<template>
    <div class="tool-item">
        <span v-on:click="export_proteins">Export proteins as .csv</span>
    </div>
</template>

<script>

export default {
    name: 'ExportProteins',
    props:['gephi_data'],
    data() {
        return {
        }
    },
    methods: {
        export_proteins() {
            var com = this;

            // export proteins as csv
            var csvTermsData = com.gephi_data.nodes;

            var terms_csv = 'name\tensembl\tcluster\tdescription\n';

            csvTermsData.forEach(function(row) {
                terms_csv += row.attributes['Name'] + '\t' + row.attributes['Ensembl ID'] + '\t"'  + row.attributes['Modularity Class'] + '"\t"' + row.attributes['Description'] +'"';
                terms_csv += '\n';   
            });


            //Create html element to hidden download csv file
            var hiddenElement = document.createElement('a');
            hiddenElement.target = '_blank';
            hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(terms_csv);
            hiddenElement.download = 'Proteins.csv';  
            hiddenElement.click();
        },
    }
}
</script>