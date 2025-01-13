<template>
  <main class="relative w-screen h-screen p-5 overflow-hidden 2xl:p-8 bg-gradient-front">
    <img class="w-full h-full absolute top-0 left-0 object-cover z-[-1]" src="../assets/graph-bg-0.webp" />

    <section class="container flex h-full mx-auto 2xl:items-center">
      <div
        class="max-w-full max-h-full 2xl:min-h-[75vh] w-[590px] flex flex-col p-6 rounded-3xl border border-[#074a42] bg-slate-900/75 !backdrop-blur overflow-auto">
        <header class="flex items-center gap-8">
          <img class="w-14" src="@/assets/logo-grad.svg" />
          <h1 class="mt-3 text-2xl font-bold">
            Welcome to <span class="text-primary-500">Protein Graph Database </span>
            <span class="block text-base font-normal text-slate-400">Select a option to get started and generate
              graph</span>
          </h1>
        </header>

        <Tabs class="mt-8 tab-active-grad" v-model:value="activeTab">
          <TabList :pt="{
            tabList: { class: 'w-full!inline-flex !border-none !bg-slate-800/50 !rounded' },
            activeBar: { class: '!h-full !rounded !bg-none border !border-primary-500' },
          }">
            <Tab value="0" class="flex-1 flex justify-center items-center gap-3 !py-1.5 !px-3 !border-none !z-[2]">
              <span :class="`material-symbols-rounded ${activeTab === '0' ? 'text-primary-500' : 'text-slate-400'}`">
                family_history
              </span>
              <span class="font-bold whitespace-nowrap">Input</span>
            </Tab>
            <Tab value="1" class="flex-1 flex justify-center items-center gap-3 !py-1.5 !px-3 !border-none !z-[2]">
              <span :class="`material-symbols-rounded ${activeTab === '1' ? 'text-primary-500' : 'text-slate-400'}`">
                flowsheet </span>
              <span class="font-bold whitespace-nowrap">File</span>
            </Tab>
            <Tab value="2"
              class="flex-1 flex justify-center items-center gap-3 !py-1.5 !px-3 !border-none !z-[2] has:!text-white">
              <span :class="`material-symbols-rounded ${activeTab === '2' ? 'text-primary-500' : 'text-slate-400'}`">
                scatter_plot </span>
              <span class="font-bold whitespace-nowrap">Import</span>
            </Tab>
          </TabList>

          <TabPanels class="mt-4 !p-0 !bg-transparent">
            <TabPanel value="0">
              <InputScreen></InputScreen>
            </TabPanel>
            <TabPanel value="1">
              <FileScreen></FileScreen>
            </TabPanel>
            <TabPanel value="2">
              <ImportScreen></ImportScreen>
            </TabPanel>
          </TabPanels>
        </Tabs>

        <footer class="flex items-center justify-center gap-3 pt-8 mt-auto">
          <Button class="animate__animated animate__bounce" icon="pi pi-youtube" severity="secondary" rounded
            aria-label="Youtube" />
          <Button as="a" href="https://github.com/BackofenLab/AxoWise" target="_blank" rel="noopener"
            class="animate__animated animate__bounce animate__fast" icon="pi pi-github" severity="secondary" rounded
            aria-label="Github" />
          <Button class="animate__animated animate__bounce animate__slow" icon="pi pi-reddit" severity="secondary"
            rounded aria-label="Reddit" />
          <Button class="animate__animated animate__bounce animate__slower" icon="pi pi-linkedin" severity="secondary"
            rounded aria-label="Linkedin" />
        </footer>
      </div>
    </section>
  </main>
</template>

<script>
// @ is an alias to /src
import InputScreen from "@/components/home/InputScreen.vue";
import FileScreen from "@/components/home/FileScreen.vue";
import ImportScreen from "@/components/home/ImportScreen.vue";

export default {
  name: "HomeView",
  components: {
    InputScreen,
    FileScreen,
    ImportScreen,
  },
  data() {
    return {
      activeTab: "0",
      navigation_path: null,
    };
  },
};
</script>
