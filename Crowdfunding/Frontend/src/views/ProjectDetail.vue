<template>
  <div>
    <section class="container py-5" style="max-width: 960px;">
      <GoBackBtn />

      <div v-if="loading" class="text-center text-muted">Cargando proyecto...</div>
      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

      <div v-else class="row">
        <!-- Imágenes -->
        <div class="col-md-6 mb-5">
          <div
            class="carousel-container rounded shadow-sm overflow-hidden"
            @mouseenter="stopAutoRotation"
            @mouseleave="startAutoRotation"
          >
            <transition name="fade" mode="out-in">
              <img
                :src="mainImage"
                :key="mainImage"
                class="img-fluid w-100"
                :alt="`Imagen de ${project.name}`"
                style="object-fit: cover; height: 400px;"
              />
            </transition>
          </div>
          <div v-if="images.length > 1" class="carousel-controls d-flex justify-content-center align-items-center mt-2">
            <!-- Flecha anterior -->
            <button
              class="carousel-btn"
              @click="prevImage"
              aria-label="Imagen anterior"
            >‹</button>
              
            <!-- Indicadores -->
            <div class="d-flex gap-2 mx-3">
              <span
                v-for="(img, idx) in images"
                :key="idx"
                class="indicator"
                :class="{ active: idx === currentImageIndex }"
                @click="currentImageIndex = idx"
                aria-label="'Ir a imagen ' + (idx + 1)"
              ></span>
            </div>
          
            <!-- Flecha siguiente -->
            <button
              class="carousel-btn"
              @click="nextImage"
              aria-label="Imagen siguiente"
            >›</button>
          </div>

          <!-- Contribuciones -->
          <section class="mt-5">
            <h3 class="fs-5 fw-semibold text-dark mb-3">Contribuciones al proyecto</h3>

            <div v-if="contributions.length">
              <ul>
                <li
                  v-for="contribution in contributions"
                  :key="contribution.id"
                  class="p-3 mb-3 bg-white rounded shadow-sm border text-secondary"
                >
                  <p class="mb-1"><strong>Contribuidor:</strong> {{ contribution.contributor?.username || 'Anónimo' }}</p>
                  <p class="mb-1 message-text"><strong>Mensaje:</strong> {{ contribution.message || 'Sin mensaje' }}</p>
                  <div class="d-flex justify-content-between mt-2 align-items-center">
                    <small class="text-muted">Fecha: {{ formatDate(contribution.date) }}</small>
                    <span class="badge bg-gradient-lila text-white fs-6">+{{ contribution.amount }} €</span>
                  </div>
                </li>
              </ul>
            </div>
            <p v-else class="text-muted">Aún no hay contribuciones.</p>
          </section>
        </div>

        <!-- Detalles del proyecto -->
        <div class="col-md-6">
          <h1 class="mb-3 fs-3 fw-semibold text-dark">{{ project.name }}</h1>
          <p class="text-muted mb-1">Categoría: {{ projectCategory.category }}</p>
          <p class="text-muted mb-3">Propietario: {{ owner.username }}</p>

          <p class="mb-4 text-secondary">
            {{ truncatedDescription }}<span v-if="isTruncated">...</span>
          </p>
          <button
            v-if="isTruncated"
            class="btn btn-link p-0 text-lila"
            data-bs-toggle="modal"
            data-bs-target="#descriptionModal"
          >
            Ver más
          </button>

          <!-- Modal de descripción -->
          <div class="modal fade" id="descriptionModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-lg">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title">Descripción completa</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button>
                </div>
                <div class="modal-body">{{ project.description }}</div>
                <div class="modal-footer">
                  <button class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                </div>
              </div>
            </div>
          </div>

          <ul class="list-unstyled mt-4 text-secondary">
            <li><strong>Meta:</strong> {{ project.goal }} €</li>
            <li><strong>Fecha de inicio:</strong> {{ formattedDate }}</li>
            <li>
              <strong>Estado: </strong>
              <span :class="project.is_active ? 'text-lila' : 'text-danger'">
                {{ project.is_active ? 'Activo' : 'Cerrado' }}
              </span>
            </li>
          </ul>

          <div class="my-4">
            <label for="progress" class="form-label">Progreso</label>
            <div class="progress rounded">
              <div
                class="progress-bar bg-lila"
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
              v-if="isAuthenticated && !isOwner && project.is_active"
              class="btn btn-outline-secondary-custom mt-3"
              :to="`/projects/${project.id}/contribute`"
            >
              Contribuir
            </router-link>

            <div v-else-if="isAuthenticated && isOwner">
              <router-link
                :to="`/projects/${project.id}/contributions`"
                class="btn btn-outline-secondary-custom mt-3"
              >
                Ver contribuciones
              </router-link>
              <button
                v-if="project.is_active"
                class="btn btn-outline-danger mt-3 ms-2"
                data-bs-toggle="modal"
                data-bs-target="#closeModal"
              >
                Cerrar proyecto
              </button>
              <router-link
                :to="`/projects/edit/${project.id}`"
                class="btn btn-outline-secondary mt-3 ms-2"
              >
                Editar
              </router-link>
            </div>

            <router-link
              v-else-if="!isAuthenticated && project.is_active"
              to="/auth"
              class="btn btn-outline-secondary-custom mt-3"
            >
              Inicia sesión para contribuir
            </router-link>

            <p v-else class="text-muted mt-3">El proyecto ya no está disponible. ¡Gracias por el apoyo!</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Modal para cerrar proyecto -->
    <div class="modal fade" id="closeModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Cerrar Proyecto</h5>
            <button class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button>
          </div>
          <div class="modal-body">
            <p>¿Estás seguro de que deseas cerrar este proyecto? Esta acción no se puede deshacer.</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button class="btn btn-danger" @click="closeProject">Cerrar proyecto</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted, computed, onUnmounted } from 'vue';
  import { useRoute } from 'vue-router';
  import api from '@/services/api';
  import { useAuthStore } from '@/stores/auth';
  import type { ProjectCategory, Project } from '@/interfaces/Project';
  import type { User } from '@/interfaces/Account';
  import type { Contribution } from '@/interfaces/Contribution';
  import GoBackBtn from '@/components/GoBackBtn.vue';

  const route = useRoute();
  const auth = useAuthStore();
  defineProps<{ id: string | number }>();
  
  const project = ref<Project>({} as Project);
  const projectCategory = ref<ProjectCategory>({} as ProjectCategory);
  const owner = ref<User>({} as User);
  const contributions = ref<Contribution[]>([] as Contribution[]);
  const loading = ref(true);
  const error = ref('');
  const showConfirmDialog = ref(false);

  const currentUser = auth.user
  const isAuthenticated = computed(() => auth.isAuthenticated);
  const isOwner = computed(() => !!currentUser && currentUser.id === project.value.owner);

  const formattedDate = computed(() => {
    if (!project.value.start_date) return '';
    return new Date(project.value.start_date).toLocaleDateString();
  });
  const currentImageIndex = ref(0);
  let imageInterval: ReturnType<typeof setInterval>;

  const images = computed(() => project.value.project_images || []);
  const mainImage = computed(() => {
    return images.value[currentImageIndex.value]?.image || '';
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
      const contributionsData = await api.get<Contribution[]>(`/contributions/simple/`, {
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

  async function closeProject() {
    try {
      showConfirmDialog.value = false;
      await api.patch(`/projects/list/${project.value.id}/`, {
        is_active: false,
      });
      window.location.reload();
    } catch (err: any) {
      error.value = 'Error al cerrar el proyecto.';
    }
  }
  
  function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  return date.toLocaleDateString('es-ES', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  });
}

  function nextImage() {
    currentImageIndex.value = (currentImageIndex.value + 1) % images.value.length;
  }
  function prevImage() {
    currentImageIndex.value =
      (currentImageIndex.value - 1 + images.value.length) % images.value.length;
  }
  function startAutoRotation() {
    imageInterval = setInterval(() => {
      nextImage();
    }, 5000);
  }
  function stopAutoRotation() {
    clearInterval(imageInterval);
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


  onMounted(() => {
    fetchProject();
    startAutoRotation();
  });

  onUnmounted(() => {
    stopAutoRotation();
  })
</script>

<style scoped>
.text-lila {
  color: #7c3aed;
}

.bg-lila {
  background-color: #7c3aed !important;
}

.bg-gradient-lila {
  background: linear-gradient(90deg, #7c3aed, #a78bfa);
  color: white;
}

.btn-outline-secondary-custom {
  background: linear-gradient(90deg, #7c3aed, #a78bfa);
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
  padding: 0.5rem 1.25rem;
  border-radius: 0.5rem;
  border: none;
  box-shadow: 0 4px 8px rgba(124, 58, 237, 0.3);
  transition: all 0.2s ease;
  text-decoration: none;
}

.btn-outline-secondary-custom:hover {
  box-shadow: 0 6px 12px rgba(124, 58, 237, 0.5);
  transform: translateY(-2px);
}

.message-text {
  white-space: pre-wrap;
  word-wrap: break-word;
}
.carousel-container {
  position: relative;
}

.carousel-btn {
  background: rgba(124, 58, 237, 0.8);
  color: white;
  border: none;
  font-size: 1.5rem;
  padding: 0.25rem 0.75rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s;
}

.carousel-btn:hover {
  background: rgba(124, 58, 237, 1);
}

.indicator {
  width: 10px;
  height: 10px;
  background: #d1d5db;
  border-radius: 50%;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
}

.indicator:hover {
  transform: scale(1.2);
}

.indicator.active {
  background: #7c3aed;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
