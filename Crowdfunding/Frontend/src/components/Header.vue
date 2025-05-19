<template>
  <nav class="navbar d-flex align-items-center justify-content-between px-5 py-3">
    <div class="d-flex align-items-center gap-2">
      <router-link to="/" class="navbar-brand d-flex align-items-center gap-2">
        <div class="logo-circle">CF</div>
        <span class="brand-text">CrowdFundMe</span>
      </router-link>
    </div>

    <!-- CENTRO: búsqueda (solo en escritorio) -->
    <div class="d-none d-md-flex align-items-center search-center">
      <input
        v-model="searchQuery"
        @keyup.enter="submitSearch"
        type="search"
        placeholder="Buscar proyectos..."
        aria-label="Buscar"
        class="form-control"
      />
      <button
        aria-label="Search"
        class="search-btn"
        type="button"
        @click="submitSearch"
      >
        <i class="fas fa-search"></i>
      </button>
    </div>

    <!-- DERECHA: links y auth -->
    <div class="d-flex align-items-center gap-4">
      <!-- links desktop -->
      <ul class="nav d-none d-md-flex gap-4 m-0 p-0">
        <li class="nav-item">
          <router-link to="/" class="nav-link">Inicio</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/projects" class="nav-link">Proyectos</router-link>
        </li>
        <li class="nav-item" v-if="auth.isAuthenticated">
          <a
            :href="`/profile/${auth.user?.id}`"
            class="nav-link"
          >Cuenta</a>
        </li>
        <li class="nav-item" v-if="!auth.isAuthenticated">
          <router-link to="/auth" class="nav-link btn-signup" style="color: white !important;">Login</router-link>
        </li>
      </ul>
      <!-- logout desktop -->
      <button
        v-if="auth.isAuthenticated"
        type="button"
        class="btn-signup d-none d-md-block"
        @click="logout"
      >Cerrar Sesión</button>

      <!-- botón hamburguesa móvil -->
      <button
        class="btn btn-link-custom d-md-none"
        aria-label="Toggle navigation"
        @click="isMobileMenuOpen = !isMobileMenuOpen"
      >
        <i :class="isMobileMenuOpen ? 'fas fa-times' : 'fas fa-bars'"></i>
      </button>
    </div>
  </nav>

  <!-- menú móvil desplegable -->
  <transition name="slide-down">
    <div v-if="isMobileMenuOpen" class="mobile-menu d-md-none px-4 py-3">
      <!-- búsqueda móvil -->
      <div class="mobile-search mb-3">
        <input
          v-model="searchQuery"
          @keyup.enter="submitSearch"
          type="search"
          placeholder="Buscar proyectos..."
          class="form-control w-100 mb-2"
        />
        <button
          class="btn btn-block btn-signup w-100"
          type="button"
          @click="submitSearch"
        >Buscar</button>
      </div>
      <!-- enlaces móviles -->
      <ul class="nav flex-column gap-2 mb-3">
        <li class="nav-item">
          <router-link to="/" class="nav-link">Inicio</router-link>
        </li>
        <li class="nav-item" v-if="auth.isAuthenticated">
          <router-link
            :to="`/profile/${auth.user?.id}`"
            class="nav-link"
          >Cuenta</router-link>
        </li>
        <li class="nav-item" v-if="!auth.isAuthenticated">
          <router-link to="/auth" class="btn-signup nav-link" style="color: white !important;">Login</router-link>
        </li>
      </ul>
      <button
        v-if="auth.isAuthenticated"
        type="button"
        class="btn-signup w-100"
        @click="logout"
      >Cerrar Sesión</button>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const auth = useAuthStore();

const searchQuery = ref('');
function submitSearch() {
  const q = searchQuery.value.trim();
  if (q) {
    window.location.href = `/projects/search?query=${encodeURIComponent(q)}`;
    searchQuery.value = '';
    isMobileMenuOpen.value = false; // cierra menú en móvil tras buscar
  }
}

function logout() {
  auth.logout();
  router.push({ name: 'Auth' });
}

const isMobileMenuOpen = ref(false);
</script>

<style scoped>
/* Transición suave para el menú móvil */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}
.slide-down-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}
.slide-down-enter-to {
  opacity: 1;
  transform: translateY(0);
}
.slide-down-leave-from {
  opacity: 1;
  transform: translateY(0);
}
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* estilos generales */
nav {
  font-family: 'Inter', sans-serif;
  position: relative;
  background: white;
  z-index: 10;
}

.logo-circle {
  width: 32px;
  height: 32px;
  background-color: #7c3aed;
  border-radius: 50%;
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-text {
  color: #7c3aed;
  font-weight: 600;
  font-size: 1.125rem;
}

.nav-link {
  color: black !important;
  font-weight: 400;
  font-size: 0.875rem;
}
.nav-link:hover {
  text-decoration: underline !important;
}

.btn-signup {
  background-color: #7c3aed;
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
  padding: 0.375rem 1rem;
  border-radius: 0.375rem;
  border: none;
  width: auto;
}
.btn-signup:hover {
  background-color: #6d28d9;
}

.btn-link-custom {
  color: black;
  font-size: 1.25rem;
  border: none;
  padding: 0;
}
.btn-link-custom:hover {
  color: #6d28d9;
}

.search-btn {
  background: none;
  border: none;
  color: black;
  font-size: 1rem;
}
.search-btn:hover {
  color: #6d28d9;
}

.form-control {
  font-size: 0.875rem;
  padding: 0.25rem 0.5rem;
  border: 1px solid #ccc;
  border-radius: 0.25rem;
}
.form-control:focus {
  outline: none;
  border-color: #7c3aed;
  box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.2);
}

/* menú móvil */
.mobile-menu {
  background: white;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.mobile-search .btn {
  margin-top: 0.25rem;
}

/* centrar el buscador en desktop */
.search-center {
  flex: 1;
  max-width: 400px;
  justify-content: center;
}

.search-center .form-control {
  width: 100%;
  max-width: 300px;
}

.search-center .search-btn {
  margin-left: 0.5rem;
}
</style>
