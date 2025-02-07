<template>
  <div class="flex flex-col gap-4 mb-4">
    <fieldset class="flex flex-col gap-1.5 animate__animated animate__fadeInUp">
      <label for="in_label" class="text-slate-400">Species</label>
      <Select v-model="selected_species" :options="species" optionLabel="label" class="w-full !bg-[#1c2132]" />
    </fieldset>

    <fieldset class="flex flex-col gap-1.5 animate__animated animate__fadeInUp">
      <div class="flex items-center justify-between">
        <label for="protein_list" class="text-slate-400">Protein list</label>

        <Button label="Generate samples" icon="pi pi-refresh" size="small" text @click="random_proteins()" />
      </div>
      <Textarea v-model="raw_text" rows="5" cols="30" class="!bg-[#1c2132] text-center" />
    </fieldset>

    <fieldset class="flex flex-wrap items-center gap-2 animate__animated animate__fadeInUp">
      <Checkbox v-model="customEdge" inputId="edgeCheck" name="edgeCheck" binary />
      <label for="edgeCheck" class="text-slate-400"> Use custom protein interactions. </label>
      <FileUpload v-if="customEdge" :pt="{ root: { class: 'w-full !justify-start' } }" mode="basic" accept=".txt"
        @select="load_edge_file" :maxFileSize="25000000"
        :chooseButtonProps="{ severity: 'secondary', class: '!bg-black' }" chooseLabel="Select file"
        chooseIcon="pi pi-folder-open" />
    </fieldset>

    <fieldset class="flex flex-col gap-2 animate__animated animate__fadeInUp">
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
import validator from "validator";
import { useToast } from "primevue/usetoast";
export default {
  name: "InputScreen",
  data() {
    return {
      loading: false,
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
        max: 1,
        step: 0.01,
      },
      edge_thick: {
        value: 0.2,
      },
      raw_text: null,
      selected_species: null,
      customEdge: false,
      edge_file: null,
    };
  },
  mounted() {
    this.toast = useToast();
  },
  methods: {
    submit() {
      /*
      Submit function connects the backend with frontend by supplying the user input and retrieving the graph network.

      Transmitting:
        - species id
        - protein list
        - protein threshold

      Retrieving:
        - gephi_json (data structure of graph network)
      */
      var com = this;
      var formData = new FormData();
      // Detection of empty inputs
      if (com.selected_species == "" || com.selected_species == null) {
        com.toast.add({ severity: 'error', detail: 'Please select a species!', life: 4000 });
        return;
      }

      if (com.raw_text == null || com.raw_text == "") {
        com.toast.add({ severity: 'error', detail: 'Please provide a list of proteins!', life: 4000 });
        return;
      }

      if (com.edge_file !== null) {
        formData.append("edge-file", com.edge_file);
      }

      var cleanData = validator.whitelist(com.raw_text, "a-zA-Z0-9\\s");

      // Creating FormData to send files & parameters with an ajax call

      formData.append("threshold", this.threshold.value);
      formData.append("species_id", this.selected_species.code);
      formData.append("proteins", cleanData.split(/\s+/).join(";"));

      com.loading = true;
      this.axios.post(this.api.subgraph, formData).then((response) => {
        if (response.data.length != 0) {
          response.edge_thick = this.edge_thick.value;
          com.loading = false;
          com.$store.commit("assign", response);
          com.$router.push("protein");
        } else {
          com.toast.add({ severity: 'error', detail: 'No proteins were found.', life: 4000 });
          com.loading = false;
        }
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
    load_edge_file(e) {
      const { originalEvent } = e;
      var com = this;
      com.edge_file = originalEvent.target.files[0];
    },
    async random_proteins() {
      const response = await fetch("./mousedb.csv");
      if (!response.ok) {
        throw new Error("HTTP error " + response.status);
      }
      const text = await response.text();
      var randomProteins = this.getRandomElements(text.split(/[\r\n]+/), 600);

      this.raw_text = randomProteins.join("\n");
    },
    getRandomElements(array, numElements) {
      const randomElements = [];
      const arrayCopy = array.slice(); // Create a copy of the original array

      while (randomElements.length < numElements && arrayCopy.length > 0) {
        const randomIndex = Math.floor(Math.random() * arrayCopy.length);
        const randomElement = arrayCopy.splice(randomIndex, 1)[0];
        randomElements.push(randomElement);
      }

      return randomElements;
    },
  },
};
</script>
