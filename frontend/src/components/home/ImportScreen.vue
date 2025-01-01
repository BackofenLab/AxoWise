<template>
  <div class="flex flex-col gap-4 mb-4">
    <fieldset class="flex flex-col gap-1.5 animate__animated animate__fadeInUp">
      <label for="protein_list" class="text-slate-400">Import your graph</label>
      <FileUpload :pt="{ root: { class: 'w-full !justify-start' } }" mode="basic" accept=".json" @select="load_json"
        :maxFileSize="25000000" :chooseButtonProps="{ severity: 'secondary', class: '!bg-black' }"
        chooseLabel="Select Json" chooseIcon="pi pi-folder-open" />
    </fieldset>
  </div>

  <Button fluid label="Submit" size="large" severity="secondary"
    class="!bg-black animate__animated animate__fadeInUp animate__slow" @click="submit()" :loading="loading" />
</template>

<script>
import { useToast } from "primevue/usetoast";
export default {
  name: "ImportScreen",
  data() {
    return {
      gephi_json: null,
      loading: false,
    };
  },
  mounted() {
    this.toast = useToast();
  },
  methods: {
    load_json(e) {
      const { originalEvent } = e;
      var com = this;
      //Load json file and overwrite to gephi_json
      const file = originalEvent.target.files[0];
      const reader = new FileReader();
      reader.onload = function (e) {
        com.gephi_json = JSON.parse(e.target.result);
      };
      reader.readAsText(file);
    },
    submit() {
      var com = this;

      if (com.gephi_json == null) {
        this.toast.add({ severity: 'error', detail: 'Please select a import!', life: 4000 });
        return;
      }
      com.loading = true;

      com.$store.commit("assign", { data: com.gephi_json });
      com.$store.commit("assign_dcoloumn", com.gephi_json.dvalues);
      com.$router.push("protein");

      com.loading = false;
    },
  },
};
</script>
