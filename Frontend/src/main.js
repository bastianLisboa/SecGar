import './assets/main.css'
import '@fortawesome/fontawesome-free/css/all.min.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Crea la aplicacion raiz, conecta el sistema de rutas y monta Vue en el contenedor principal.
createApp(App).use(router).mount('#app')
