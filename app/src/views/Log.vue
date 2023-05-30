<script>
import Navbar from '@/components/Navbar.vue';
import Projetos from '../components/Projetos.vue';
import TableLog from '../components/TableLog.vue';

export default {
  components: {
    Navbar,
    Projetos,
    TableLog,
  },
  // Resto da lógica da sua view
}

</script>


<template>
  <div>
    <Navbar/>
    <TableLog />
  </div>
</template>
