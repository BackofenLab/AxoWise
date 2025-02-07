<template>
  <div class="flex flex-col gap-5 mb-4">
    <fieldset class="flex flex-col gap-1.5 animate__animated animate__fadeInUp">
      <label for="in_label" class="text-slate-400">Species</label>
      <Select v-model="selected_species" :options="species" optionLabel="label" class="w-full !bg-[#1c2132]" />
    </fieldset>

    <fieldset class="flex flex-col gap-1.5 animate__animated animate__fadeInUp">
      <label for="protein_list" class="text-slate-400">Protein file</label>
      <FileUpload :pt="{ root: { class: 'w-full !justify-start' } }" mode="basic" accept=".csv"
        @select="load_protein_file" :maxFileSize="25000000"
        :chooseButtonProps="{ severity: 'secondary', class: '!bg-black' }" chooseLabel="Select file"
        chooseIcon="pi pi-folder-open" />
    </fieldset>

    <fieldset v-if="dcoloumns != null" class="flex flex-col gap-1.5 animate__animated animate__fadeInUp">
      <label for="dcoloumns" class="text-slate-400">De-coloumns:</label>
      <MultiSelect v-model="selected_categories" optionLabel="" placeholder="Select" showClear resetFilterOnClear
        filterPlaceholder="Search De-coloumns" filter class="!w-full" emptyMessage="No De-coloumns available"
        emptyFilterMessage="No De-coloumns available" :selectedItemsLabel="`${selected_categories?.length} De-coloumns`"
        :options="dcoloumns" :maxSelectedLabels="3" />
    </fieldset>

    <fieldset class="flex flex-wrap items-center gap-2 animate__animated animate__fadeInUp">
      <Checkbox v-model="customEdge" inputId="edgeCheck" name="edgeCheck" binary />
      <label for="edgeCheck" class="text-slate-400"> Use custom protein interactions. </label>
      <FileUpload v-if="customEdge" :pt="{ root: { class: 'w-full !justify-start' } }" mode="basic" accept=".txt"
        @select="load_edge_file" :maxFileSize="25000000"
        :chooseButtonProps="{ severity: 'secondary', class: '!bg-black' }" chooseLabel="Select file"
        chooseIcon="pi pi-folder-open" />
    </fieldset>

    <fieldset class="animate__animated animate__fadeInUp">
      <div class="flex items-center justify-between gap-2">
        <label for="" class="text-slate-400">Edge score</label>

        <InputNumber inputClass="w-14 h-8 text-center" :minFractionDigits="2" :maxFractionDigits="2"
          :min="threshold.min" :max="threshold.max" :step="threshold.step" v-model="threshold.value" />
      </div>
      <Slider class="mx-1 mt-3 mb-3" :min="threshold.min" :max="threshold.max" :step="threshold.step"
        v-model="threshold.value" />
    </fieldset>
  </div>

  <Button fluid label="Submit" size="large" severity="secondary"
    class="!bg-black animate__animated animate__fadeInUp animate__slow" @click="submit()" :loading="loading" />
</template>

<script>
import { useToast } from "primevue/usetoast";
export default {
  name: "FileScreen",
  data() {
    return {
      species: [
        {
          label: "Mus musculus (mouse)",
          code: "10090",
        },
        {
          label: "Homo sapiens (human)",
          code: "9606",
        },
      ],
      api: {
        subgraph: "api/subgraph/proteins",
      },
      threshold: {
        value: 0.7,
        min: 0,
        max: 0.9999,
        step: 0.01,
      },
      dcoloumns: null,
      selected_species: null,
      loading: false,
      customEdge: false,
      selected_categories: null,
      edge_file: null,
      protein_file: null
    };
  },
  mounted() {
    this.toast = useToast();
  },
  methods: {
    load_edge_file(e) {
      const { originalEvent } = e;
      var com = this;
      com.edge_file = originalEvent.target.files[0];
    },
    load_protein_file(e) {
      const { originalEvent } = e;
      var com = this;
      com.protein_file = originalEvent.target.files[0];

      //Read csv file to get coloumn information
      const file = originalEvent.target.files[0];

      com.dcoloumns = [];
      const reader = new FileReader();
      reader.onload = function (e) {
        var allTextLines = e.target.result.split(/\n|\n/);
        var save_dcoloumns = allTextLines[0].split(",");
        var type_coloumns = allTextLines[1].split(",");

        //Return only coloumns that contends for d-value
        for (var i = 0; i < save_dcoloumns.length; i++) {
          type_coloumns[i] = type_coloumns[i].trim();
          if (com.onlyNumbers(type_coloumns[i])) {
            save_dcoloumns[i] = save_dcoloumns[i].trim();
            com.dcoloumns.push(save_dcoloumns[i].replace(/^"(.*)"$/, "$1"));
          }
        }
      };
      reader.readAsText(file);
    },
    onlyNumbers(possibleNumber) {
      return /^[0-9.,-]+$/.test(possibleNumber);
    },
    submit() {
      var com = this;
      var formData = new FormData();

      if (com.selected_species == "" || com.selected_species == null) {
        this.toast.add({ severity: 'error', detail: 'Please select a species!', life: 4000 });
        return;
      }

      if (com.protein_file == null) {
        this.toast.add({ severity: 'error', detail: 'Please supply a file!', life: 4000 });
        return;
      }

      if (com.edge_file !== null) {
        formData.append("edge-file", com.edge_file);
      }

      formData.append("threshold", com.threshold.value);
      formData.append("species_id", com.selected_species.code);
      formData.append("file", com.protein_file);
      formData.append("selected_d", com.selected_categories);

      this.$store.commit("assign_dcoloumn", com.selected_categories);

      com.loading = true;
      this.axios.post(this.api.subgraph, formData).then((response) => {
        com.loading = false;
        response.edge_thick = 0.01;
        com.$store.commit("assign", response);
        com.$router.push("protein");
      }).catch(function (error) {
        com.loading = false;
        if (error.response) {
          // The request was made and the server responded with a status code
          console.log(error.response);
          com.toast.add({ severity: 'error', detail: error?.message ? error.message + '. Please check your inputs and try again!' : 'Something went wrong. Please check your inputs and try again!', life: 4000 });
        } else if (error.request) {
          // The request was made but no response was received
          console.log(error.request);
          com.toast.add({ severity: 'error', detail: 'Something went wrong. Please check your inputs and try again!', life: 4000 });
        } else {
          // Something happened in setting up the request that triggered an Error
          console.log(error.message);
          com.toast.add({ severity: 'error', detail: 'Something went wrong. Please check your inputs and try again!', life: 4000 });
        }
      });
    },
  },
};
</script>
