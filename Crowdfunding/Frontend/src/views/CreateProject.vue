<template>
    <div class="container py-5">
      <h2 class="mb-4 text-success">Crear Nuevo Proyecto</h2>
  
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
          <label for="images" class="form-label">Imágenes (PNG, JPG/JPEG, WEBP)</label>
          <input type="file" id="images" class="form-control" multiple @change="handleImageUpload" />
        </div>
  
        <div v-if="error" class="alert alert-danger">{{ error }}</div>
  
        <button class="btn btn-success" type="submit">Crear Proyecto</button>
      </form>
    </div>
</template>

<script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import api from '@/services/api';
  import type { ProjectCategory } from '@/interfaces/Project';
  import { useMessageStore } from '@/stores/message';
  
  const router = useRouter();
  const form = ref({
    name: '',
    description: '',
    goal: '',
    category: 0,
  });
  const images = ref<File[]>([]);
  const categories = ref<ProjectCategory[]>([]);
  const error = ref('');
  const messageStore = useMessageStore();
  
  onMounted(async () => {
    try {
      const { data } = await api.get('/projects/categories/');
      categories.value = data;
    } catch (e) {
      error.value = 'No se pudieron cargar las categorías.';
    }
  });
  
  function handleImageUpload(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target.files) {
      images.value = Array.from(target.files);
    }
  }
  
  async function createProject() {
    error.value = '';
    try {
      const { data } = await api.post('/projects/list/', form.value);
      return data;
    } catch (e: any) {
      error.value = `Error al crear el proyecto. Comprueba el formulario`;
      console.error(e);
      return null;
    }
  }

  async function uploadImages(projectId: number) {
    try {
      // Si hay imágenes, las subimos asociándolas al ID del proyecto creado
      if (images.value.length > 0) {
        const uploads = images.value.map(img => {
          const imgData = new FormData();
          imgData.append('project', String(projectId));
          imgData.append('image', img);
          return api.post('/projects/project-images/', imgData, {
            headers: { 'Content-Type': 'multipart/form-data' },
          });
        });
        await Promise.all(uploads);
      } else {
        const imgData = new FormData();
        imgData.append('project', String(projectId));
        return api.post('/projects/project-images/', imgData, {
            headers: { 'Content-Type': 'multipart/form-data' },
          });
      }
    } catch (e: any) {
      error.value = `Error al subir imágenes. Revisa tu proyecto y los formatos de las imágenes`;
      console.error(e);
      messageStore.setMessage(error.value, 'error');
    }
  }

  async function submitProject() {
    error.value = '';
    const project = await createProject();
    if (!project) return;
    await uploadImages(project.id);
    router.push({ name: 'ProjectDetails', params: { id: Number(project.id) } });
  }
</script>
