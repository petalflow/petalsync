<template>
  <div class="mt-8 flex flex-col items-center">
    <h1 class="text-2xl font-bold mb-6">Logs</h1>
    <div class="container mx-auto">
      <table class="min-w-full bg-white border border-gray-200">
        <thead>
          <tr>
            <th class="py-2 px-4 border-b">Data de Execução</th>
            <th class="py-2 px-4 border-b">Status</th>
            <th class="py-2 px-4 border-b">Descrição do Log</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in logs" :key="log.id_log" class="border-b">
            <td class="py-2 px-4">{{ log.dt_execution }}</td>
            <td class="py-2 px-4">
              <span :class="log.fl_error ? 'text-red-500' : 'text-green-500'">
                {{ log.fl_error ? 'Error' : 'Success' }}
              </span>
            </td>
            <td class="py-2 px-4">{{ log.ds_log }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

  
<script setup>
import { ref, onMounted } from 'vue'

const logs = ref([])

onMounted(async () => {
  // Fazer a requisição para a rota "/GetAlllog" para obter os logs
  // e atribuir a resposta à variável "logs"
  try {
    const response = await fetch('http://localhost:8000/GetAlllog')
    logs.value = await response.json()
  } catch (error) {
    console.error(error)
  }
})
</script>
