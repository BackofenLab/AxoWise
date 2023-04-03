<template>
  <InputScreen></InputScreen>
</template>

<script>
// @ is an alias to /src
import InputScreen from '@/components/home/InputScreen.vue'

export default {
  name: 'HomeView',
  components: {
    InputScreen
  },
  data(){
    return{
      navigation_path: null

    }
  },
  mounted() {
    if (this.$store.state.gephi_json != null) { 
      window.location.reload();
    }
  }
}
</script>
