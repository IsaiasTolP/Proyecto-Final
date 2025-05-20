<template>
  <div class="project-form container py-5 my-5">
    <h2 class="mb-4 title">Contacto</h2>

    <form @submit.prevent="submitContact" class="form">
      <div class="form-group">
        <label for="name" class="form-label">Nombre</label>
        <input v-model="form.name" type="text" id="name" class="form-control" required maxlength="75" />
      </div>

      <div class="form-group">
        <label for="email" class="form-label">Correo Electrónico</label>
        <input v-model="form.email" type="email" id="email" class="form-control" required maxlength="100" />
      </div>

      <div class="form-group">
        <label for="message" class="form-label">Mensaje</label>
        <textarea v-model="form.message" id="message" rows="5" class="form-control" required maxlength="1000"></textarea>
      </div>

      <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
      <div v-if="success" class="alert alert-success mt-3">{{ success }}</div>

      <button class="btn btn-submit" type="submit">Enviar Mensaje</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import api from '@/services/api';

const form = ref({
  name: '',
  email: '',
  message: '',
});

const error = ref('');
const success = ref('');

async function submitContact() {
  error.value = '';
  success.value = '';
  try {
    await api.post('/contact/send/', form.value);
    success.value = 'Mensaje enviado correctamente. ¡Gracias por contactarme!';
    form.value = { name: '', email: '', message: '' };
  } catch (e) {
    error.value = 'Error al enviar el mensaje. Por favor, intenta de nuevo más tarde.';
    console.error(e);
  }
}
</script>

<style scoped>
.project-form {
  max-width: 600px;
  margin: 0 auto;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.1);
  padding: 2rem 2.5rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.title {
  color: #7c3aed;
  font-weight: 700;
  font-size: 2rem;
  text-align: center;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.8rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
  user-select: none;
}

.form-control,
.form-select {
  width: 100%;
  padding: 0.65rem 1rem;
  font-size: 1rem;
  border-radius: 8px;
  border: 1.8px solid #cbd5e0;
  transition: border-color 0.25s ease, box-shadow 0.25s ease;
  font-family: inherit;
}

.form-control:focus,
.form-select:focus {
  border-color: #7c3aed;
  box-shadow: 0 0 5px rgba(124, 58, 237, 0.5);
  outline: none;
}

.image-upload-area {
  border: 2px dashed #7c3aed;
  border-radius: 12px;
  padding: 1.5rem;
  background-color: #f7fafc;
  cursor: pointer;
  user-select: none;
  transition: background-color 0.3s ease, border-color 0.3s ease;
  text-align: center;
}

.image-upload-area:hover,
.image-upload-area:focus {
  background-color: #f3e8ff;
  border-color: #6b21a8;
  outline: none;
}

.image-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.image-list-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.7rem 1rem;
  border-radius: 8px;
  background-color: #f9fafb;
  margin-bottom: 0.7rem;
  box-shadow: 0 2px 6px rgba(124, 58, 237, 0.12);
}

.image-preview-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.image-preview {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.image-name {
  font-weight: 500;
  color: #2d3748;
  max-width: 280px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.btn-remove {
  padding: 0.3rem 0.75rem;
  font-size: 0.85rem;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.btn-remove:hover {
  background-color: #9f7aea;
  color: #fff;
}

.btn-submit {
  display: block;
  width: 100%;
  background-color: #7c3aed;
  color: white;
  font-weight: 700;
  font-size: 1.15rem;
  padding: 0.9rem 1.2rem;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  user-select: none;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  margin-top: 1.5rem;
}

.btn-submit:hover {
  background-color: #6b21a8;
  box-shadow: 0 6px 12px rgba(107, 33, 168, 0.45);
  outline: none;
}

.btn-submit:focus {
  outline: 2px solid #d8b4fe;
  outline-offset: 2px;
}

.alert {
  font-weight: 600;
  font-size: 0.95rem;
}
</style>
