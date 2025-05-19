<template>
  <div class="project-form container py-5 my-5">
    <h2 class="mb-4 title">Crear Nuevo Proyecto</h2>

    <form @submit.prevent="submitProject" enctype="multipart/form-data" class="form">
      <div class="form-group">
        <label for="name" class="form-label">Nombre del Proyecto</label>
        <input v-model="form.name" type="text" id="name" class="form-control" required maxlength="75" />
      </div>

      <div class="form-group">
        <label for="description" class="form-label">Descripción</label>
        <textarea v-model="form.description" id="description" rows="4" class="form-control" required></textarea>
      </div>

      <div class="form-group">
        <label for="goal" class="form-label">Objetivo de Recaudación (€)</label>
        <input v-model="form.goal" type="number" id="goal" class="form-control" step="0.01" required />
      </div>

      <div class="form-group">
        <label for="category" class="form-label">Categoría</label>
        <select v-model="form.category" id="category" class="form-select" required>
          <option value="" disabled>Selecciona una categoría</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.category }}</option>
        </select>
      </div>

      <div class="form-group">
        <label class="form-label">Imágenes (PNG, JPG/JPEG, WEBP)</label>

        <div
          class="image-upload-area"
          @click="fileInput?.click()"
          role="button"
          tabindex="0"
          @keydown.enter="fileInput?.click()"
        >
          <p class="text-muted mb-0">Haz clic aquí para añadir imágenes</p>
          <small>(Puedes seleccionar varias)</small>
        </div>

        <input
          ref="fileInput"
          type="file"
          class="d-none"
          accept="image/png, image/jpg, image/jpeg, image/webp"
          multiple
          @change="handleImageUpload"
        />
      </div>

      <div v-if="previewImages.length" class="form-group">
        <h5 class="form-label">Imágenes seleccionadas:</h5>
        <ul class="image-list">
          <li
            v-for="(img, index) in previewImages"
            :key="index"
            class="image-list-item"
          >
            <div class="image-preview-info">
              <img :src="img.url" alt="Previsualización" class="image-preview" />
              <span class="image-name">{{ img.file.name }}</span>
            </div>
            <button class="btn btn-sm btn-danger btn-remove" @click="removeImage(index)" type="button">Quitar</button>
          </li>
        </ul>
      </div>

      <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>

      <button class="btn btn-submit" type="submit">Crear Proyecto</button>
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
