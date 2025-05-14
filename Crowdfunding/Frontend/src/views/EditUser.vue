<template>
  <div class="container py-5">
    <h2 class="mb-4">Configuración de Cuenta</h2>

    <div class="mb-3">
      <strong>Usuario:</strong> {{ user.username }}
    </div>

    <div class="mb-3">
      <strong>Email:</strong> {{ user.email }}
      <button class="btn btn-link" @click="showEmailDialog = true">Modificar Email</button>
    </div>

    <div class="mb-3">
      <strong>Contraseña:</strong> ********
      <button class="btn btn-link" @click="showPasswordDialog = true">Cambiar Contraseña</button>
    </div>

		<!-- Diálogo para cambiar Email -->
		<div class="modal fade show d-block" tabindex="-1" role="dialog" aria-modal="true" v-if="showEmailDialog">
			<div class="modal-dialog modal-dialog-centered" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title" id="changeEmailModalLabel">Cambiar Email</h5>
						<button type="button" class="btn-close" aria-label="Cerrar" @click="showEmailDialog = false"></button>
					</div>
					<div class="modal-body">
						<label for="emailInput" class="form-label">Nuevo email</label>
						<input
							id="emailInput"
							v-model="emailForm.email"
							type="email"
							class="form-control"
							placeholder="ejemplo@correo.com"
							required
						/>
					</div>
					<div class="modal-footer">
						<button class="btn btn-secondary" @click="showEmailDialog = false">Cancelar</button>
						<button class="btn btn-primary" @click="updateEmail">Guardar</button>
					</div>
				</div>
			</div>
		</div>

    <!-- Diálogo para cambiar Contraseña -->
		<div class="modal fade show d-block" tabindex="-1" role="dialog" aria-modal="true" v-if="showPasswordDialog">
			<div class="modal-dialog modal-dialog-centered" role="document">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title" id="changePasswordModalLabel">Cambiar Contraseña</h5>
						<button type="button" class="btn-close" aria-label="Cerrar" @click="showPasswordDialog = false"></button>
					</div>
					<div class="modal-body">
						<label for="passwordInput" class="form-label">Nueva contraseña</label>
						<input
							id="passwordInput"
							v-model="passwordForm.password"
							type="password"
							class="form-control mb-3"
							placeholder="Nueva contraseña"
							required
						/>
						<label for="confirmPasswordInput" class="form-label">Confirmar contraseña</label>
						<input
							id="confirmPasswordInput"
							v-model="passwordForm.confirmPassword"
							type="password"
							class="form-control"
							placeholder="Repetir contraseña"
							required
						/>
					</div>
					<div class="modal-footer">
						<button class="btn btn-secondary" @click="showPasswordDialog = false">Cancelar</button>
						<button class="btn btn-primary" @click="updatePassword">Guardar</button>
					</div>
				</div>
			</div>
		</div>

    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
    <div v-if="success" class="alert alert-success mt-3">{{ success }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '@/services/api';

const user = ref({
  id: null,
  username: '',
  email: '',
});

const emailForm = ref({ email: '' });
const passwordForm = ref({
  password: '',
  confirmPassword: '',
});

const showEmailDialog = ref(false);
const showPasswordDialog = ref(false);
const error = ref('');
const success = ref('');

onMounted(async () => {
  try {
    const { data } = await api.get('/users/me/');
    user.value = data;
    emailForm.value.email = data.email;
  } catch (e) {
    error.value = 'Error al cargar los datos del usuario.';
  }
});

async function updateEmail() {
  error.value = '';
  success.value = '';
  try {
    await api.patch(`/users/${user.value.id}/`, { email: emailForm.value.email });
    user.value.email = emailForm.value.email;
    success.value = 'Email actualizado correctamente.';
    showEmailDialog.value = false;
  } catch (e) {
    error.value = 'No se pudo actualizar el email.';
  }
}

async function updatePassword() {
  error.value = '';
  success.value = '';
  const { password, confirmPassword } = passwordForm.value;

  if (password !== confirmPassword) {
    error.value = 'Las contraseñas no coinciden.';
    return;
  }

  try {
    await api.patch(`/users/${user.value.id}/`, { password });
    success.value = 'Contraseña actualizada correctamente.';
    passwordForm.value.password = '';
    passwordForm.value.confirmPassword = '';
    showPasswordDialog.value = false;
  } catch (e) {
    error.value = 'No se pudo actualizar la contraseña.';
  }
}
</script>
