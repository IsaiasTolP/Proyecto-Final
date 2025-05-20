<template>
  <div class="modal fade show d-block" tabindex="-1" @click.self="close">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content p-4">
        <div class="modal-header border-0 pb-0">
          <h5 class="modal-title">Recuperar Contraseña</h5>
          <button type="button" class="btn-close" @click="close"></button>
        </div>

        <div class="modal-body pt-2">
          <p class="text-muted mb-3">Introduce tu usuario y correo electrónico para recuperar tu contraseña.</p>

          <form @submit.prevent="submitRecovery">
            <!-- Usuario -->
            <div class="mb-3">
              <label for="username" class="form-label fw-medium">Usuario</label>
              <input
                v-model="form.username"
                type="text"
                id="username"
                class="form-control"
                placeholder="Tu nombre de usuario"
                required
              />
            </div>

            <!-- Email -->
            <div class="mb-3">
              <label for="email" class="form-label fw-medium">Correo Electrónico</label>
              <input
                v-model="form.email"
                type="email"
                id="email"
                class="form-control"
                placeholder="correo@ejemplo.com"
                required
              />
            </div>

            <button type="submit" class="btn-outline-secondary-custom w-100" :disabled="loading">
              {{ loading ? 'Correo enviado' : 'Recuperar Contraseña' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '@/services/api'

const emit = defineEmits(['close'])

const loading = ref(false)

const form = ref({
  username: '',
  email: '',
})

async function submitRecovery() {
	try {
		await api.post('/users/password-reset/', {
			username: form.value.username,
			email: form.value.email,
		});
		loading.value = true
		setTimeout(() => {
			loading.value = false
			close()
		}, 2000);
	} catch (err: any) {
		console.error(err)
	}
}

function close() {
  emit('close')
}
</script>

<style scoped>
.modal {
  background-color: rgba(0, 0, 0, 0.4);
  z-index: 1050;
}

.modal-content {
  border-radius: 0.75rem;
  background-color: #ffffff;
}

.btn-outline-secondary-custom {
  background: linear-gradient(90deg, #7c3aed, #a78bfa);
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  box-shadow: 0 4px 8px rgba(124, 58, 237, 0.3);
  transition: box-shadow 0.3s ease, transform 0.2s ease;
  text-decoration: none;
}
</style>
