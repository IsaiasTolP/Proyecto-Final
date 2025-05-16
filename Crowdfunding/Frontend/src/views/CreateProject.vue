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
          <label class="form-label">Imágenes (PNG, JPG/JPEG, WEBP)</label>

          <div
            class="border border-success rounded p-3 text-center cursor-pointer"
            style="background-color: #f8f9fa;"
            @click="fileInput?.click()"
          >
            <p class="text-muted mb-0">Haz clic aquí para añadir imágenes</p>
            <small>(Puedes seleccionar varias)</small>
          </div>
        
          <input
            ref="fileInput"
            type="file"
            class="d-none"
            accept="image/*"
            @change="handleImageUpload"
          />
        </div>

        <div v-if="previewImages.length" class="mb-3">
          <h5 class="form-label">Imágenes seleccionadas:</h5>
          <ul class="list-group">
            <li
              v-for="(img, index) in previewImages"
              :key="index"
              class="list-group-item d-flex justify-content-between align-items-center"
            >
              <div class="d-flex align-items-center gap-3">
                <img :src="img.url" alt="Previsualización" style="height: 60px; width: 60px; object-fit: cover;" />
                <span>{{ img.file.name }}</span>
              </div>
              <button class="btn btn-sm btn-outline-danger" @click="removeImage(index)">Quitar</button>
            </li>
          </ul>
        </div>
  
        <div v-if="error" class="alert alert-danger">{{ error }}</div>
  
        <button class="btn btn-success" type="submit">Crear Proyecto</button>
      </form>
    </div>
</template>

<script setup lang="ts">
  import { ref, onMounted, onBeforeUnmount } from 'vue';
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
  const fileInput = ref<HTMLInputElement | null>(null);
  const previewImages = ref<{ file: File; url: string }[]>([]);
  
  onMounted(async () => {
    try {
      const { data } = await api.get('/projects/categories/');
      categories.value = data;
    } catch (e) {
      error.value = 'No se pudieron cargar las categorías.';
    }
  });

  onBeforeUnmount(() => {
    previewImages.value.forEach(img => URL.revokeObjectURL(img.url));
  });
  
  function handleImageUpload(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target.files) {
      const newFiles = Array.from(target.files);

      newFiles.forEach(file => {
        if (!images.value.find(existing => existing.name === file.name)) {
          images.value.push(file);
          previewImages.value.push({
            file,
            url: URL.createObjectURL(file),
          });
        }
      });

      // Limpiar el input para poder volver a seleccionar el mismo archivo si se quiere
      target.value = '';
    }
  }

  function removeImage(index: number) {
    URL.revokeObjectURL(previewImages.value[index].url);
    previewImages.value.splice(index, 1);
    images.value.splice(index, 1);
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
