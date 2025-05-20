<template>
  <div class="container py-5">
    <GoBackBtn />
    <h2 class="mb-4 text-primary">Editar Proyecto</h2>

    <form @submit.prevent="submitProject" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="name" class="form-label">Nombre del Proyecto</label>
        <input v-model="form.name" type="text" id="name" class="form-control" required maxlength="75"/>
      </div>

      <div class="mb-3">
        <label for="description" class="form-label">Descripción</label>
        <textarea v-model="form.description" id="description" rows="4" class="form-control" required></textarea>
      </div>

      <div class="mb-3">
        <label for="goal" class="form-label">Objetivo de Recaudación (€)</label>
        <input v-model="form.goal" type="number" id="goal" class="form-control" step="0.01" required />
      </div>

      <div class="mb-3">
        <label for="category" class="form-label">Categoría</label>
        <select v-model="form.category" id="category" class="form-select" required>
          <option value="" disabled>Selecciona una categoría</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.category }}</option>
        </select>
      </div>

      <div class="mb-3">
        <label class="form-label">Añadir Imágenes Nuevas</label>

        <div class="d-flex flex-column gap-2">
          <button type="button" class="btn btn-outline-primary w-fit" @click="fileInput?.click()">
            Seleccionar imágenes
          </button>
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            class="d-none"
            @change="handleImageUpload"
          />
        </div>
      
        <ul class="list-group mt-3" v-if="images.length">
          <li v-for="(img, index) in images" :key="index" class="list-group-item d-flex justify-content-between align-items-center">
            {{ img.name }}
            <button type="button" class="btn btn-sm btn-danger" @click="removeImage(index)">Quitar</button>
          </li>
        </ul>


        <div class="mb-3" v-if="existingImages.length">
          <label class="form-label">Imágenes Actuales</label>
          <ul class="list-group">
            <li v-for="img in existingImages" :key="img.id" class="list-group-item d-flex justify-content-between align-items-center">
              <img :src="img.image" alt="Imagen del proyecto" class="img-thumbnail" style="max-height: 80px;" />
              <button type="button" class="btn btn-sm btn-danger" @click="deleteImage(img.id)">Eliminar</button>
            </li>
          </ul>
        </div>
      </div>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <button class="btn btn-primary" type="submit">Guardar Cambios</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';
import type { ProjectCategory } from '@/interfaces/Project';
import { useMessageStore } from '@/stores/message';
import GoBackBtn from '@/components/GoBackBtn.vue';

const route = useRoute();
const router = useRouter();
const projectId = Number(route.params.id);
const messageStore = useMessageStore();
const fileInput = ref<HTMLInputElement | null>(null);

const form = ref({
  name: '',
  description: '',
  goal: '',
  category: 0,
});

const images = ref<File[]>([]);
const categories = ref<ProjectCategory[]>([]);
const existingImages = ref<{ id: number; image: string }[]>([]);
const error = ref('');

onMounted(async () => {
  try {
    const [{ data: project }, { data: catData }, { data: projectImages }] = await Promise.all([
      api.get(`/projects/list/${projectId}/`),
      api.get('/projects/categories/'),
      api.get(`/projects/project-images/?project=${projectId}`)
    ]);

    form.value = {
      name: project.name,
      description: project.description,
      goal: project.goal,
      category: project.category,
    };

    existingImages.value = projectImages;
    categories.value = catData;
  } catch (e) {
    error.value = 'Error al cargar el proyecto o las categorías.';
    console.error(e);
  }
});

function handleImageUpload(event: Event) {
  const target = event.target as HTMLInputElement;
  if (target.files) {
    // Añadir nuevas imágenes a las ya seleccionadas
    images.value.push(...Array.from(target.files));
    // Reset del input para permitir volver a seleccionar los mismos archivos si se desea
    target.value = '';
  }
}

function removeImage(index: number) {
  images.value.splice(index, 1);
}

async function deleteImage(imageId: number) {
  try {
    await api.delete(`/projects/project-images/${imageId}/`);
    existingImages.value = existingImages.value.filter(img => img.id !== imageId);
  } catch (e) {
    error.value = 'No se pudo eliminar la imagen.';
    console.error(e);
  }
}

async function updateProject() {
  try {
    await api.put(`/projects/list/${projectId}/`, form.value);
  } catch (e) {
    error.value = 'Error al actualizar el proyecto.';
    console.error(e);
    throw e;
  }
}

async function uploadImages() {
  try {
    if (images.value.length > 0) {
      const uploads = images.value.map(img => {
        const formData = new FormData();
        formData.append('project', String(projectId));
        formData.append('image', img);
        return api.post('/projects/project-images/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
      });
      await Promise.all(uploads);
    }
  } catch (e) {
    error.value = 'Error al subir imágenes.';
    console.error(e);
    messageStore.setMessage(error.value, 'error');
  }
}

async function submitProject() {
  error.value = '';
  try {
    await updateProject();
    await uploadImages();
    messageStore.setMessage('Proyecto actualizado correctamente', 'success');
    router.push({ name: 'ProjectDetails', params: { id: projectId } });
  } catch {
    // Error ya manejado
  }
}
</script>
