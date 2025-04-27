<template>
  <nav class="navbar navbar-expand-md bg-success navbar-dark px-5" role="navigation" aria-label="Main navigation">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/">CrowdFundMe</router-link>
      <button
        class="navbar-toggler"
        type="button"
        @click="toggleNavbar"
        :aria-expanded="isCollapsed"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div :class="['collapse', 'navbar-collapse', { show: isCollapsed }]" id="navbarNav">
        <ul class="navbar-nav ms-auto align-items-center">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Inicio</router-link>
          </li>
          <li class="nav-link" v-if="auth.isAuthenticated">
            <router-link class="nav-link" :to="`/profile/${auth.user?.id}`">Cuenta</router-link>
          </li>
          <li class="nav-item" v-if="!auth.isAuthenticated">
            <router-link class="nav-link" to="/auth">Login</router-link>
          </li>
          <li class="nav-item" v-else>
            <button class="btn btn-outline-light ms-3" @click="logout">Cerrar Sesión</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

	const isCollapsed = ref(false);
	const router = useRouter();

	function toggleNavbar() {
		isCollapsed.value = !isCollapsed.value;
	}

	const auth = useAuthStore();

	function logout() {
	  // Clean up tokens and headers
		auth.logout();
	  // Redirect to login page
		router.push({ name: 'Auth' });
	}
</script>

<style scoped>
	.navbar-brand {
		font-weight: bold;
	}

	.nav-link {
		color: #ffffff;
	}

	.nav-link:hover,
	.nav-link:focus {
		color: #cce5cc;
	}
</style>
