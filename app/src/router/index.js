import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Log from '../views/Log.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Home
    },
    {
      path: '/Log',
      component: Log
    }
  ]
})

export default router
