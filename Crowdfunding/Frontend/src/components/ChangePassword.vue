<template>
  <div class="auth-wrapper">
    <div class="auth-card">
      <h2 class="auth-title">Recuperar Contraseña</h2>

      <form @submit.prevent="handleReset" novalidate>
        <!-- Nueva contraseña -->
        <div class="mb-3">
          <label for="newPassword" class="auth-label">Nueva Contraseña</label>
          <input
            id="newPassword"
            v-model="form.password"
            type="password"
            class="auth-input"
            required
            aria-required="true"
            minlength="8"
          />
        </div>

        <!-- Confirmar nueva contraseña -->
        <div class="mb-3">
          <label for="confirmNewPassword" class="auth-label">Confirmar Nueva Contraseña</label>
          <input
            id="confirmNewPassword"
            v-model="form.confirmPassword"
            type="password"
            class="auth-input"
            required
            aria-required="true"
            minlength="8"
          />
        </div>

        <!-- Mensaje de error -->
        <div v-if="errorMessage" class="auth-alert">
          {{ errorMessage }}
        </div>

        <button type="submit" class="btn-gradient w-100">
          Restablecer Contraseña
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/services/api';
import router from '@/router';

const form = ref({
  password: '',
  confirmPassword: '',
});
const route = useRoute();

const errorMessage = ref('');

async function handleReset() {
  errorMessage.value = '';

  if (!form.value.password || !form.value.confirmPassword) {
    errorMessage.value = 'Por favor completa ambos campos.';
    return;
  }

  if (form.value.password !== form.value.confirmPassword) {
    errorMessage.value = 'Las contraseñas no coinciden.';
    return;
  }

  try {
		await api.post('/users/password-reset-confirm/', {
			uid: route.query.uid,
			token: route.query.token,
			new_password: form.value.confirmPassword,
		});

    errorMessage.value = 'Contraseña restablecida con éxito.';
    form.value.password = '';
    form.value.confirmPassword = '';
		router.push({ name: 'Auth' })
  } catch (err) {
    errorMessage.value = 'Hubo un error al restablecer la contraseña.';
  }
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
</style>
