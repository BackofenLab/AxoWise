<template>
  <div class="tool-item">
    <span v-on:click="export_edges">Export edges as .csv</span>
  </div>
</template>

<script>
export default {
  name: "ExportEdges",
  props: ["gephi_data", "ensembl_name_index"],
  data() {
    return {};
  },
  methods: {
    export_edges() {
      var com = this;

      // export proteins as csv
      var csvTermsData = com.gephi_data.edges;
      var terms_csv = "source\tsrc_ensembl\ttarget\ttrg_ensembl\tscore\n";

      csvTermsData.forEach(function (row) {
        terms_csv +=
          com.ensembl_name_index[row.source] +
          "\t" +
          row.source +
          '\t"' +
          com.ensembl_name_index[row.target] +
          '"\t"' +
          row.target +
          '"\t"' +
          row.attributes["score"] +
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
