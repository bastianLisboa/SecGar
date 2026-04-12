<script setup>
/*
**************************************************************************
*                                           SECGAR                       *
**************************************************************************
* TITULO DE LA SECCION: LOGIN                                            *
* DESARROLLADOR: BASTIAN LISBOA                                          *
* FECHA: 2026-04-11                                                      *
* NOMBRE ARCHIVO: LoginView.vue                                          *
* DESCRIPCION: Vista de autenticacion mock para ingreso y registro       *
* de usuarios dentro de la plataforma SecGar.                            *
* ************************************************************************
* HISTORIAL DE MODIFICACIONES                                            *
* ************************************************************************
* 2026-04-11 - Limpieza de codigo, reorganizacion de la logica           *
* y documentacion del componente.                                        *
**************************************************************************
*/

import { computed, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

// Define los modos validos del flujo de autenticacion.
const AUTH_MODE = Object.freeze({
  LOGIN: 'login',
  REGISTER: 'register',
})

// Centraliza el texto visible para evitar literales repetidos en la vista.
const MODE_COPY = Object.freeze({
  [AUTH_MODE.LOGIN]: {
    title: 'Iniciar sesion',
    description:
      'Accede para administrar reservas, publicar tu garaje o revisar solicitudes en un solo lugar.',
    submitLabel: 'Ingresar al panel',
    socialLabel: 'Continuar con Google',
    footerPrompt: 'Primera vez?',
    footerAction: 'Crear cuenta',
  },
  [AUTH_MODE.REGISTER]: {
    title: 'Registrar usuario',
    description:
      'Crea tu cuenta para publicar tu garaje, recibir solicitudes y gestionar arriendos con seguridad.',
    submitLabel: 'Crear mi cuenta',
    socialLabel: 'Registrarme con Google',
    footerPrompt: 'Ya tienes cuenta?',
    footerAction: 'Iniciar sesion',
  },
})

// Describe los tabs disponibles para renderizarlos desde una sola estructura.
const AUTH_TABS = Object.freeze([
  { label: 'Iniciar sesion', value: AUTH_MODE.LOGIN },
  { label: 'Crear cuenta', value: AUTH_MODE.REGISTER },
])

// Genera las clases de las particulas del fondo animado.
const PARTICLE_CLASSES = Object.freeze(
  Array.from({ length: 12 }, (_, index) => `particle-${index + 1}`),
)

// Reune mensajes cortos de confianza para reforzar el contexto del producto.
const TRUST_BADGES = Object.freeze([
  'Reservas verificadas',
  'Pagos protegidos',
  'Respuesta rapida',
])

// Obtiene el router para navegar programaticamente al dashboard de ejemplo.
const router = useRouter()

// Mantiene el modo actual del formulario entre login y registro.
const currentMode = ref(AUTH_MODE.LOGIN)

// Agrupa el estado del formulario en un unico objeto reactivo.
const form = reactive({
  fullName: '',
  email: '',
  password: '',
  confirmPassword: '',
})

// Indica si el formulario activo es el de inicio de sesion.
const isLoginMode = computed(() => currentMode.value === AUTH_MODE.LOGIN)

// Expone el bloque de textos correspondiente al modo seleccionado.
const activeCopy = computed(() => MODE_COPY[currentMode.value])

// Cambia el modo al presionar uno de los tabs superiores.
function setMode(mode) {
  currentMode.value = mode
}

// Alterna el modo desde el enlace contextual del pie del formulario.
function toggleMode() {
  currentMode.value = isLoginMode.value ? AUTH_MODE.REGISTER : AUTH_MODE.LOGIN
}

// Simula una autenticacion correcta y redirige al dashboard.
function handleAuthSubmit() {
  router.push('/dashboard')
}
</script>

<template>
  <main class="login-page">
    <div class="background-orb orb-left"></div>
    <div class="background-orb orb-right"></div>

    <div class="particle-layer" aria-hidden="true">
      <span
        v-for="particleClass in PARTICLE_CLASSES"
        :key="particleClass"
        class="particle"
        :class="particleClass"
      ></span>
    </div>

    <div class="login-shell">
      <div class="auth-switch" role="tablist" aria-label="Seleccion de acceso">
        <button
          v-for="tab in AUTH_TABS"
          :key="tab.value"
          class="switch-button"
          :class="{ active: currentMode === tab.value }"
          type="button"
          @click="setMode(tab.value)"
        >
          {{ tab.label }}
        </button>
      </div>

      <section class="login-card">
        <div class="topbar">
          <div class="brand-lockup">
            <div class="brand-head">
              <div class="brand-mark" aria-hidden="true">
                <i class="fa-solid fa-warehouse brand-icon"></i>
              </div>

              <p class="brand-title">SecGar</p>
            </div>

            <p class="brand-kicker">Arrienda tu garaje con seguridad</p>
          </div>
        </div>

        <div class="content-header">
          <h1>{{ activeCopy.title }}</h1>
          <p class="description">{{ activeCopy.description }}</p>

          <div class="trust-badges" aria-label="Beneficios del servicio">
            <span v-for="badge in TRUST_BADGES" :key="badge" class="trust-badge">{{ badge }}</span>
          </div>
        </div>

        <form class="login-form" @submit.prevent="handleAuthSubmit">
          <label v-if="!isLoginMode">
            Nombre completo
            <input
              v-model="form.fullName"
              type="text"
              placeholder="Juan Perez"
              autocomplete="name"
            />
          </label>

          <label>
            <span class="field-label">Correo electronico</span>
            <input
              v-model="form.email"
              type="email"
              placeholder="admin@secgar.cl"
              autocomplete="email"
            />
          </label>

          <label>
            <span class="field-row">
              <span class="field-label">Contrasena</span>
              <button v-if="isLoginMode" class="field-link" type="button">
                Olvidaste tu contrasena?
              </button>
            </span>
            <input
              v-model="form.password"
              type="password"
              placeholder="********"
              :autocomplete="isLoginMode ? 'current-password' : 'new-password'"
            />
          </label>

          <label v-if="!isLoginMode">
            <span class="field-label">Confirmar contrasena</span>
            <input
              v-model="form.confirmPassword"
              type="password"
              placeholder="********"
              autocomplete="new-password"
            />
          </label>

          <button class="submit-button" type="submit">{{ activeCopy.submitLabel }}</button>
        </form>

        <div class="social-divider">
          <span></span>
          <p>o continua con</p>
          <span></span>
        </div>

        <div class="social-actions">
          <button
            class="social-button"
            type="button"
          >
            <span class="social-icon google-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" focusable="false" aria-hidden="true">
                <path
                  fill="#EA4335"
                  d="M12 10.2v3.9h5.4c-.2 1.2-.9 2.2-1.9 2.9l3 2.3c1.8-1.6 2.8-4 2.8-6.8 0-.7-.1-1.5-.2-2.2H12z"
                />
                <path
                  fill="#34A853"
                  d="M12 21c2.6 0 4.8-.9 6.4-2.4l-3-2.3c-.8.6-1.9 1-3.4 1-2.6 0-4.8-1.8-5.6-4.1l-3.1 2.4C4.9 18.8 8.2 21 12 21z"
                />
                <path
                  fill="#4A90E2"
                  d="M6.4 13.2c-.2-.6-.3-1.2-.3-1.8s.1-1.2.3-1.8l-3.1-2.4C2.5 8.6 2 10.2 2 11.9s.5 3.3 1.3 4.7l3.1-2.4z"
                />
                <path
                  fill="#FBBC05"
                  d="M12 6.5c1.4 0 2.7.5 3.7 1.4l2.8-2.8C16.8 3.5 14.6 2.7 12 2.7c-3.8 0-7.1 2.2-8.7 5.5l3.1 2.4C7.2 8.2 9.4 6.5 12 6.5z"
                />
              </svg>
            </span>
            {{ activeCopy.socialLabel }}
          </button>
        </div>

        <div class="card-footer">
          <p class="helper">
            <span>{{ activeCopy.footerPrompt }}</span>
            <button class="footer-link" type="button" @click="toggleMode">
              {{ activeCopy.footerAction }}
            </button>
          </p>

          <RouterLink class="helper-route" to="/dashboard">Ver demo</RouterLink>
        </div>
      </section>
    </div>
  </main>
</template>

<style scoped src="../../styles/login/login.css"></style>
