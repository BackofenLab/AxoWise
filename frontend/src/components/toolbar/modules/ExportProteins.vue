<template>
  <Button text plain severity="secondary" type="button" label="Export proteins as .csv" class="!justify-start !py-1"
    @click="export_proteins" />
</template>

<script>
export default {
  name: "ExportProteins",
  props: ["gephi_data"],
  data() {
    return {};
  },
  methods: {
    export_proteins() {
      var com = this;

      // export proteins as csv
      var csvTermsData = com.gephi_data.nodes;
      var terms_csv =
        "name\tensembl_gene\tensembl_protein\tcluster\tdescription\tBetweenness Centrality\tPageRank\tAlias\n";

      csvTermsData.forEach(function (row) {
        terms_csv +=
          row.attributes["Name"] +
          "\t" +
          row.attributes["Ensembl Gene ID"] +
          "\t" +
          row.attributes["Ensembl ID"] +
          '\t"' +
          row.attributes["Modularity Class"] +
          '"\t"' +
          row.attributes["Description"] +
          '"\t"' +
          row.attributes["Betweenness Centrality"] +
          '"\t"' +
          row.attributes["PageRank"] +
          '"\t"' +
          row.attributes["Alias"] +
          '"';
        terms_csv += "\n";
      });

      //Create html element to hidden download csv file
      var hiddenElement = document.createElement("a");
      hiddenElement.target = "_blank";
      hiddenElement.href =
        "data:text/csv;charset=utf-8," + encodeURI(terms_csv);
      hiddenElement.download = "Proteins.csv";
      hiddenElement.click();
    },
  },
};
</script>
