<template>
    <div class="flex flex-col items-center">
      <h1 class="text-2xl font-bold mb-6">Lista de Projetos</h1>
  
      <div class="flex flex-col items-center w-full max-w-2xl">
        <div
          v-for="projeto in projetos"
          :key="projeto.id"
          :class="[
            'bg-white shadow-lg rounded-lg p-4 mb-4 w-full flex justify-between items-center',
            isError ? 'border-red-500 border-l-2' : 'border-green-500 border-l-2'
          ]"
        >
          <div>
            <h2 class="text-lg font-medium">{{ projeto.name_project }}</h2>
            <p class="text-gray-500">{{ formatDateTime(projeto.dt_last_run) }}</p>
          </div>
          <div class="flex space-x-2">
            <button class="flex items-center justify-center bg-blue-500 text-white px-4 py-2 rounded">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path
                  fill-rule="evenodd"
                  d="M2.707 3.293a1 1 0 010 1.414L1.414 6.707A2 2 0 003 9h2v6a2 2 0 002 2h4a2 2 0 002-2v-4h2a2 2 0 001.293-.465l1.292 1.292a1 1 0 010 1.414l-2.5 2.5a1 1 0 01-1.414 0L12 11.414a1 1 0 01-.293-1.707l1.293-1.293a2 2 0 000-2.828l-1.292-1.292a1 1 0 01-.057-1.638l2.5-2.5a1 1 0 011.414 0l2.5 2.5a1 1 0 01.057 1.638l-1.293 1.293A2 2 0 0017 7H15V3a2 2 0 00-2-2h-4a2 2 0 00-2 2v4H5a2 2 0 00-1.293.465L2.414 3.707a1 1 0 010-1.414zm14.586 13.414a2 2 0 010-2.828L18.586 13H15v3.586l1.707-1.707zM13 17v-2.586l-2.707 2.707a1 1 0 01-1.414 0l-2.5-2.5a1 1 0 010-1.414L8.414 9H11V6.414l-2.707 2.707a2 2 0 01-2.828 0l-2.5-2.5a1 1 0 010-1.414l2.5-2.5a2 2 0 012.828 0L8 3.586V1h4v2.586l2.707-2.707a2 2 0 012.828 0l2.5 2.5a1 1 0 010 1.414l-2.5 2.5a2 2 0 01-2.828 0L17 13.586V17h-4z"
                  clip-rule="evenodd"
                />
              </svg>
              Visualizar
            </button>
            <button class="flex items-center justify-center bg-green-500 text-white px-4 py-2 rounded">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path
                  fill-rule="evenodd"
                  d="M2 5a1 1 0 011-1h1V3a2 2 0 012-2h6a2 2 0 012 2v1h1a1 1 0 110 2H2a1 1 0 01-1-1zm1 4a1 1 0 00-1 1v6a1 1 0 001 1h14a1 1 0 001-1v-6a1 1 0 00-1-1H3zM2 14h16v2H2v-2zm4-7a1 1 0 011 1h6a1 1 0 110 2H7a1 1 0 01-1-1V7a1 1 0 112 0v1z"
                  clip-rule="evenodd"
                />
              </svg>
              Acessar Logs
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
<script>
  
import { ref, onMounted } from 'vue';
import { format } from 'date-fns';

export default {
  setup() {

    const selectedProjectId = ref(null);

    const projetos = ref([]);
    const isError = ref(false);

    onMounted(() => {
      fetchProjetos();
    });

    const fetchProjetos = () => {
      // Fazer a chamada à API para obter os projetos
      // Substitua a URL abaixo pela URL correta da sua API
      fetch('http://localhost:8000/GetAllProjects')
        .then(response => response.json())
        .then(data => {
          projetos.value = data;
        })
        .catch(error => {
          console.error('Erro ao buscar os projetos:', error);
          isError.value = true;
        });
    };

    const formatDateTime = (dateTime) => {
      const formattedDate = format(new Date(dateTime), 'dd/MM/yyyy HH:mm');
      return formattedDate;
    };

    return {
      projetos,
      isError,
      fetchProjetos,
      formatDateTime,
    };
  },
};
</script>

<style>
/* Estilos do componente aqui */
</style>
