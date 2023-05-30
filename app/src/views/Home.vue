<script>
import Navbar from '@/components/Navbar.vue';
import Projetos from '../components/Projetos.vue';

export default {
  components: {
    Navbar,
    Projetos
  },
  // Resto da lógica da sua view
}

</script>


<template>
  <div>
    <Navbar/>
    <Projetos />
  </div>
</template>
