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
            <!-- Lista de contribuciones -->
            <section v-if="contributions && contributions.length" class="container pb-5">
              <h3 class="mt-5 mb-4 text-success">Contribuciones al proyecto</h3>
              <ul class="list-group">
                <li
                  v-for="contribution in contributions"
                  :key="contribution.id"
                  class="list-group-item d-flex justify-content-between align-items-start flex-column flex-md-row mb-2"
                >
                  <div class="flex-grow-1">
                    <p class="mb-1">
                      <strong>Contribuidor:</strong>
                      {{ contribution.contributor?.username || 'Anónimo' }}
                    </p>
                    <p class="mb-1"><strong>Mensaje:</strong> {{ contribution.message || 'Sin mensaje' }}</p>
                    <p class="mb-0 text-muted"><small>Fecha: {{ formatDate(contribution.date) }}</small></p>
                  </div>
                  <div class="text-md-end">
                    <span class="badge bg-success fs-5">
                      +{{ contribution.amount }} €
                    </span>
                  </div>
                </li>
              </ul>
            </section>
            <section v-else class="container pb-5">
              <h3 class="mt-5 mb-4 text-success">Contribuciones al proyecto</h3>
              <p class="text-muted">Aún no hay contribuciones.</p>
            </section>
          </div>
  
          <!-- Detalles -->
          <div class="col-md-6">
            <h1 class="mb-3">{{ project.name }}</h1>
            <p class="text-muted mb-1">Categoría: {{ projectCategory.category }}</p>
            <p class="text-muted mb-3">Propietario: {{ owner.username }}</p>
            <p class="mb-4">
              {{ truncatedDescription }}
              <span v-if="isTruncated">...</span>
            </p>
            <button
              v-if="isTruncated"
              class="btn btn-link p-0"
              data-bs-toggle="modal"
              data-bs-target="#descriptionModal"
            >
              Ver más
            </button>
            <!-- Modal para la descripción completa -->
            <div
              class="modal fade"
              id="descriptionModal"
              tabindex="-1"
              aria-labelledby="descriptionModalLabel"
              aria-hidden="true"
              >
              <div class="modal-dialog modal-lg">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 class="modal-title" id="descriptionModalLabel">Descripción completa</h5>
                    <button
                      type="button"
                      class="btn-close"
                      data-bs-dismiss="modal"
                      aria-label="Cerrar"
                    ></button>
                  </div>
                  <div class="modal-body">
                    {{ project.description }}
                  </div>
                  <div class="modal-footer">
                    <button
                      type="button"
                      class="btn btn-secondary"
                      data-bs-dismiss="modal"
                    >
                      Cerrar
                    </button>
                  </div>
                </div>
              </div>
            </div>
  
            <ul class="list-unstyled">
              <li><strong>Meta:</strong> {{ project.goal }} €</li>
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
                {{ project.total_donated }} € recaudados de {{ project.goal }} €
              </small>
            </div>
            <div>
              <router-link
                v-if="isAuthenticated && !isOwner"
                class="btn btn-success mt-3"
                :to="`/projects/${project.id}/contribute`"
              >Contribuir</router-link>
              <div v-else-if="isAuthenticated && isOwner">
                <router-link
                  :to="`/projects/${project.id}/contributions`"
                  class="btn btn-outline-success mt-3"
                >Comprueba las contribuciones recibidas
                </router-link>
                <router-link
        	          :to="`/projects/edit/${project.id}`"
        	          class="btn btn-outline-secondary mt-3 ms-2"
      	          >
        	        Editar
      	        </router-link>
              </div>
              
              <router-link 
                v-else
                to="/auth"
                class="btn btn-outline-success mt-3"
                >Inicia sesión para contribuir
              </router-link>
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
  import type { ProjectCategory, Project } from '@/interfaces/Project';
  import type { User } from '@/interfaces/Account';
  import type { Contribution } from '@/interfaces/Contribution';

  const route = useRoute();
  const router = useRouter();
  const auth = useAuthStore();
  
  const project = ref<Project>({} as Project);
  const projectCategory = ref<ProjectCategory>({} as ProjectCategory);
  const owner = ref<User>({} as User);
  const contributions = ref<Contribution[]>([] as Contribution[]);
  const loading = ref(true);
  const error = ref('');

  const currentUser = auth.user
  const isAuthenticated = computed(() => auth.isAuthenticated);
  const isOwner = computed(() => !!currentUser && currentUser.id === project.value.owner);

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
      const projectData = await api.get<Project>(`/projects/list/${id}/`);
      project.value = projectData.data;
      const categoryData = await api.get<ProjectCategory>(`/projects/categories/${project.value.category}/`);
      projectCategory.value = categoryData.data;
    } catch (err: any) {
      error.value = 'Error al cargar el proyecto.';
    } finally {
      await fetchOwner();
      await fetchContributions();
      loading.value = false;
    }
  }

  async function fetchOwner() {
    try {
      const ownerId = project.value.owner
      const { data } = await api.get(`/users/${ownerId}/`);
      owner.value = data
    } catch (err: any) {
      error.value = 'Error al cargar al creador del proyecto'
    }
  }

  async function fetchContributions() {
    try {
      const contributionsData = await api.get<Contribution[]>(`/contributions/`, {
        params: {
          project: project.value.id,
          ordering: '-date',
        }
      });
      contributions.value = contributionsData.data;
    } catch (err: any) {
      error.value = 'Error al cargar las contribuciones del proyecto.';
    }
  }

  function goBack() {
    router.back();
  }

  function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  return date.toLocaleDateString('es-ES', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  });
}

  const limit = 2000
  const isTruncated = computed(() => {
    return project.value.description.length > limit
  })

  const truncatedDescription = computed(() => {
    return isTruncated.value
      ? project.value.description.slice(0, limit)
      : project.value.description
  });


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
