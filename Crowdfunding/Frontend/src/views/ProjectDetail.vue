<template>
    <div>
      <section class="container py-5">
        <button class="btn btn-link text-success mb-3" @click="goBack">← Volver</button>
  
        <div v-if="loading" class="text-center">
          Cargando proyecto...
        </div>
        <div v-else-if="error" class="alert alert-danger">
          {{ error }}
        </div>
        <div v-else class="row">
          <!-- Imágenes -->
          <div class="col-md-6 mb-4">
            <img
              :src="mainImage"
              class="img-fluid rounded"
              :alt="`Imagen de ${project.name}`"
            />
            <div v-if="project.project_images.length > 1" class="mt-3 d-flex flex-wrap gap-2">
              <img
                v-for="img in project.project_images.slice(1)"
                :key="img.id"
                :src="img.image"
                class="img-thumbnail"
                style="width: 100px; height: 100px; object-fit: cover;"
                :alt="`Imagen adicional de ${project.name}`"
              />
            </div>
          </div>
  
          <!-- Detalles -->
          <div class="col-md-6">
            <h1 class="mb-3">{{ project.name }}</h1>
            <p class="text-muted mb-1">Categoría: {{ project.category.category }}</p>
            <p class="text-muted mb-3">Propietario: {{ project.owner.username }}</p>
            <p class="mb-4">{{ project.description }}</p>
  
            <ul class="list-unstyled">
              <li><strong>Meta:</strong> €{{ project.goal }}</li>
              <li><strong>Fecha de inicio:</strong> {{ formattedDate }}</li>
              <li>
                <strong>Estado: </strong>
                <span :class="project.is_active ? 'text-success' : 'text-danger'">
                  {{ project.is_active ? 'Activo' : 'No activo' }}
                </span>
              </li>
            </ul>
            <div class="my-4">
              <label for="progress" class="form-label">Progreso</label>
              <div id="progress" class="progress">
                <div
                  class="progress-bar"
                  role="progressbar"
                  :style="{ width: project.percent_completed + '%' }"
                  :aria-valuenow="project.percent_completed.toFixed(0)"
                  aria-valuemin="0"
                  aria-valuemax="100"
                >
                  {{ project.percent_completed.toFixed(0) }}%
                </div>
              </div>
              <small class="text-muted">
                €{{ project.total_donated }} recaudados de €{{ project.goal }}
              </small>
            </div>
            <div>
              <button
                v-if="isAuthenticated"
                class="btn btn-success mt-3"
              >Contribuir</button>
              <router-link
                v-else
                to="/auth"
                class="btn btn-outline-success mt-3"
              >Inicia sesión para contribuir</router-link>
            </div>
          </div>
        </div>
      </section>
    </div>
</template>

<script setup lang="ts">
  import { ref, onMounted, computed } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import api from '@/services/api';
  import { useAuthStore } from '@/stores/auth';
  import type { Project } from '@/interfaces/Project.ts';


  const route = useRoute();
  const router = useRouter();
  const auth = useAuthStore();
  
  const project = ref<Project>({} as Project);
  const loading = ref(true);
  const error = ref('');

  const isAuthenticated = computed(() => auth.isAuthenticated);

  const mainImage = computed(() => project.value.project_images?.[0]?.image || '');
  const formattedDate = computed(() => {
    if (!project.value.start_date) return '';
    return new Date(project.value.start_date).toLocaleDateString();
  });

  async function fetchProject() {
    loading.value = true;
    error.value = '';
    try {
      const id = route.params.id;
      const { data } = await api.get<Project>(`/projects/${id}/`);
      project.value = data;
    } catch (err: any) {
      error.value = 'Error al cargar el proyecto.';
    } finally {
      loading.value = false;
    }
  }

  function goBack() {
    router.push({ name: 'Home' });
  }

  onMounted(fetchProject);
</script>

<style scoped>
  .btn-link {
    text-decoration: none;
  }
  .btn-link:hover {
    text-decoration: underline;
  }
</style>
