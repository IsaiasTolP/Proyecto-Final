<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100 bg-light">
    <div class="card shadow-sm p-4" style="max-width: 400px; width: 100%;">
      <h2 class="text-center mb-4 text-success">{{ isLogin ? 'Iniciar Sesión' : 'Registrarse' }}</h2>

      <form @submit.prevent="handleSubmit" novalidate>
        <!-- User -->
        <div class="mb-3">
          <label for="username" class="form-label">Usuario</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            class="form-control"
            required
            aria-required="true"
          />
        </div>

        <!-- Email (only register) -->
        <div v-if="!isLogin" class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            class="form-control"
            required
            aria-required="true"
          />
        </div>

        <!-- Password -->
        <div class="mb-3">
          <label for="password" class="form-label">Contraseña</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            class="form-control"
            required
            aria-required="true"
            minlength="8"
          />
        </div>

        <!-- Confirm password (only register) -->
        <div v-if="!isLogin" class="mb-3">
          <label for="confirmPassword" class="form-label">Confirmar Contraseña</label>
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            type="password"
            class="form-control"
            required
            aria-required="true"
            minlength="8"
          />
        </div>

				<!-- Founder checkbox (only register) -->
        <div v-if="!isLogin" class="form-check mb-3">
          <input
            id="isFounder"
            v-model="form.isFounder"
            type="checkbox"
            class="form-check-input"
          />
          <label for="isFounder" class="form-check-label">
            ¿Eres fundador?
          </label>
        </div>

        <!-- Error message -->
        <div v-if="errorMessage" class="alert alert-danger" role="alert">
          {{ errorMessage }}
        </div>

        <button type="submit" class="btn btn-success w-100">
          {{ isLogin ? 'Entrar' : 'Registrarse' }}
        </button>
      </form>

      <p class="text-center mt-3">
        <button @click="toggleMode" class="btn btn-link text-success">
          {{ isLogin ? '¿No tienes cuenta? Regístrate' : '¿Ya tienes cuenta? Inicia sesión' }}
        </button>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import type { AuthData } from '@/interfaces/Auth.ts';

const router = useRouter();
const isLogin = ref(true);
const errorMessage = ref('');

const form = ref<AuthData>({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
	isFounder: false,
});

const auth = useAuthStore();

function toggleMode() {
  isLogin.value = !isLogin.value;
  errorMessage.value = '';
  form.value.password = '';
  form.value.confirmPassword = '';
}

const isFormComplete = computed(() => {
  if (isLogin.value) {
    return form.value.username && form.value.password;
  } else {
    return (
      form.value.username &&
      form.value.email &&
      form.value.password &&
      form.value.confirmPassword
    );
  }
});

async function handleSubmit() {
  errorMessage.value = '';
  if (!isFormComplete.value) {
    errorMessage.value = 'Por favor completa todos los campos.';
    return;
  }
  try {
    if (isLogin.value) {
      // Login
      await auth.login(form.value.username, form.value.password);
			// Redirect to home page after login
			router.push({ name: 'Home' });
    } else {
      // Register, cambiar a auth.ts
      if (form.value.password !== form.value.confirmPassword) {
        errorMessage.value = 'Las contraseñas no coinciden.';
        return;
      }
      await auth.register(
        form.value.username,
        form.value.email,
        form.value.password,
        form.value.isFounder
      );
      // After register, change to login
      isLogin.value = true;
      errorMessage.value = 'Registro exitoso, por favor inicia sesión.';
      form.value.password = '';
      form.value.confirmPassword = '';
    }
  } catch (err: any) {
    if (err.response && err.response.data) {
      errorMessage.value = JSON.stringify(err.response.data);
    } else {
      errorMessage.value = 'Error de conexión';
    }
  }
}
</script>

<style scoped>
	.card {
		border-radius: 0.5rem;
	}
	.btn-link {
		text-decoration: none;
	}
	.btn-link:hover {
		text-decoration: underline;
	}
</style>