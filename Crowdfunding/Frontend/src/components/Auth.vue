<template>
  <div class="auth-wrapper">
    <div class="auth-card">
      <h2 class="auth-title">{{ isLogin ? 'Iniciar Sesión' : 'Registrarse' }}</h2>

      <form @submit.prevent="handleSubmit" novalidate>
        <!-- Usuario -->
        <div class="mb-3">
          <label for="username" class="auth-label">Usuario</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            class="auth-input"
            required
            aria-required="true"
          />
        </div>

        <!-- Email (solo en registro) -->
        <div v-if="!isLogin" class="mb-3">
          <label for="email" class="auth-label">Email</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            class="auth-input"
            required
            aria-required="true"
          />
        </div>

        <!-- Contraseña -->
        <div class="mb-3">
          <label for="password" class="auth-label">Contraseña</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            class="auth-input"
            required
            aria-required="true"
            minlength="8"
          />
        </div>

        <!-- Confirmar contraseña -->
        <div v-if="!isLogin" class="mb-3">
          <label for="confirmPassword" class="auth-label">Confirmar Contraseña</label>
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            type="password"
            class="auth-input"
            required
            aria-required="true"
            minlength="8"
          />
        </div>

        <!-- Fundador checkbox -->
        <div v-if="!isLogin" class="form-check mb-3">
          <input
            id="isFounder"
            v-model="form.isFounder"
            type="checkbox"
            class="form-check-input"
          />
          <label for="isFounder" class="form-check-label small text-secondary">
            Quiero crear proyectos
          </label>
        </div>

        <!-- Mensajes de error -->
        <div v-if="errorMessage" class="auth-alert">
          {{ errorMessage }}
        </div>
        <div v-if="messageStore.message" class="auth-alert">
          {{ messageStore.message }}
        </div>

        <button type="submit" class="btn-gradient w-100">
          {{ isLogin ? 'Entrar' : 'Registrarse' }}
        </button>
      </form>

      <p class="text-center mt-3">
        <button @click="openResetPasswordDialog" class="auth-toggle-link">
          ¿Olvidaste tu contraseña?
        </button>
        <button @click="toggleMode" class="auth-toggle-link">
          {{ isLogin ? '¿No tienes cuenta? Regístrate' : '¿Ya tienes cuenta? Inicia sesión' }}
        </button>
      </p>
    </div>
  </div>
  <ResetPasswordDialog v-if="showResetPasswordDialog" @close="showResetPasswordDialog = false"/>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useMessageStore } from '@/stores/message';
import type { AuthData } from '@/interfaces/Auth.ts';
import ResetPasswordDialog from './ResetPasswordDialog.vue';

const router = useRouter();
const messageStore = useMessageStore();
const isLogin = ref(true);
const errorMessage = ref('');
const showResetPasswordDialog = ref(false)

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
      await auth.login(form.value.username, form.value.password);
      router.push({ name: 'Home' });
    } else {
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

function openResetPasswordDialog() {
  showResetPasswordDialog.value = true;
}
</script>

<style scoped>
.auth-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f9fafb;
  font-family: 'Inter', sans-serif;
}

.auth-card {
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  padding: 2rem;
  width: 100%;
  max-width: 400px;
}

.auth-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  text-align: center;
  margin-bottom: 1.5rem;
}

.auth-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.25rem;
  display: block;
}

.auth-input {
  width: 100%;
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  transition: border-color 0.2s;
}

.auth-input:focus {
  border-color: #7c3aed;
  outline: none;
  box-shadow: 0 0 0 1px #7c3aed33;
}

.auth-alert {
  background-color: #fee2e2;
  color: #b91c1c;
  font-size: 0.875rem;
  padding: 0.75rem;
  border-radius: 0.375rem;
  margin-bottom: 1rem;
  text-align: center;
}

.btn-gradient {
  background: linear-gradient(90deg, #7c3aed 0%, #a78bfa 100%);
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
  padding: 0.625rem 1.25rem;
  border-radius: 0.5rem;
  border: none;
  box-shadow: 0 4px 6px rgba(124, 58, 237, 0.2);
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.btn-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(124, 58, 237, 0.3);
}

.auth-toggle-link {
  font-size: 0.875rem;
  color: #7c3aed;
  background: none;
  border: none;
  cursor: pointer;
  text-decoration: underline;
  padding: 0;
}
</style>
