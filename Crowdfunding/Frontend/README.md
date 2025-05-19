# Documentación: Bannerlord Commander (CrowdFundMe) 🚀

Frontend en Vue 3 para una plataforma de crowdfunding con accesibilidad, responsividad y gestión de estado global.

---

## **1. Introducción**
- **Propósito**: Plataforma de crowdfunding para financiar proyectos.
- **Tecnologías clave**:
  - Vue 3 (Composition API + `<script setup>`)
  - TypeScript
  - Pinia (gestión de estado + persistencia)
  - Vue Router
  - Axios (HTTP requests)
  - Swiper (sliders interactivos)
  - Bootstrap 5 + CSS personalizado

---

## **2. Configuración**
### **Requisitos**
- Node.js v18+
- npm/yarn/pnpm

### **Instalación**
```bash
git clone [repo-url]
cd Crowdfunding/Frontend
npm install
```

### Variables de Entorno
Para desarrollo: `VITE_API_BASE_URL=http://localhost:8000/api`

### Scripts útiles
```bash
npm run dev     # Inicia servidor de desarrollo (Vite)
npm run build   # Compila para producción
npm run preview # Previsualiza build
```

## **3. Estructura del Proyecto**
```
src/
├── assets/           # Imágenes, fuentes, estilos globales
├── components/       # Componentes reutilizables (ej. Modal.vue)
├── composables/      # Lógica reusable (Vue 3)
├── interfaces/       # Tipos TypeScript
├── router/           # Configuración de rutas
├── services/         # Llamadas API (axios)
├── stores/           # Estado global (Pinia)
├── views/            # Vistas/páginas (ej. Home.vue)
├── App.vue           # Componente raíz
└── main.ts           # Punto de entrada
```

## **4. Ejemplo de componente, CloseProjectDialog.vue**

### Props
- `visible` (Boolean): Controla la visibilidad del modal.

### Events
- `@confirm`: Se emite al confirmar acción.
- `@cancel`: Se emite al cancelar.

### Uso
```vue
<Modal :visible="isModalOpen" @confirm="handleConfirm" @cancel="closeModal" />
```

## **5. Estado global (Pinia)**

Store de mensajes globales
```ts
import router from "@/router";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useMessageStore = defineStore("message", () => {
    const message = ref<string>();
    const type = ref<string>();

    function setMessage(msg: string, t: string, persist: boolean = false) {
        message.value = msg;
        type.value = t;
        if (!persist) {
            router.beforeEach((to, from, next) => {
                clearMessage();
                next();
            })
        }
    }

    function clearMessage() {
        message.value = '';
        type.value = '';
    }

    return { message, type, setMessage, clearMessage };
} 
);
```

## **6. Routing --> vue-router**

Código de ejemplo
```ts
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/projects/:id',
    name: 'Project',
    component: () => import('@/views/Projects.vue'),
  },
];
```

## **7. Estilos y diseño**

- **Bootstrap 5**: Componentes como modales, grids, botones.
- **CSS personalizado**:
    - **Fuente**: Poppins + Inter (Google Fonts) + Fuentes por defecto de Bootstrap 5.
    - **Color**: (ej. ##7c3aed).
- **Responsividad**: Breakpoints de Bootstrap + media queries.

## **8. Servicios y API**

Ejemplo codigo de la conexión mediante axios a la api, sencillo.
```ts
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

export default api;
```

Ejemplo codigo de servicios de peticiones
```ts
import type { ProjectStats, Project } from "@/interfaces/Project";
import api from "./api";

async function getProjects() {
    const { data } = await api.get<Project>("/projects/list/")
    return data;
}
```

## **9. Tests de prueba**

Unitarias: Vue Test Utils + Vitest.

## **10. Despliegue**

### Build para producción

```bash
npm run build
```

- Output: Carpeta dist/ lista para servir

## **11. Convenciones**
**TypeScript**: Interfaces para props/API responses.
**Linting**: ESLint + Prettier (configuración recomendada).

### **Notas adicionales**
- **Accesibilidad**: Uso de `aria-label` en botones y modales.
- **Easter Egg**: El nombre "Bannerlord Commander" en el package.json es un guiño oculto 🎮.


¡Listo para financiar proyectos! 💰  
**Equipo de desarrollo**, es decir, Isaías - 2025