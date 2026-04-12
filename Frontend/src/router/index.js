import { createRouter, createWebHistory } from 'vue-router'

import DashboardView from '../views/DashboardView.vue'
import LoginView from '../views/login/LoginView.vue'

// Define el mapa de rutas visibles para las vistas principales del frontend.
const routes = [
  {
    path: '/',
    name: 'login',
    component: LoginView,
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
  },
]

// Construye el router oficial de Vue usando historial HTML para URLs limpias.
const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
