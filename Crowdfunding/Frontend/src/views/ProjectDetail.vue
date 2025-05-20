<template>
  <div>
    <section class="container py-5" style="max-width: 1080px;">
      <GoBackBtn />

      <div v-if="loading" class="text-center text-muted">Cargando proyecto...</div>
      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

      <div v-else>
        <!-- Encabezado: imágenes + botones -->
        <div class="project-header d-flex flex-column flex-md-row mb-5 align-items-center">
          <!-- Carousel de imágenes -->
          <div
            class="image-carousel flex-grow-1 rounded overflow-hidden"
            @mouseenter="stopAutoRotation"
            @mouseleave="startAutoRotation"
          >
            <transition name="fade" mode="out-in">
              <img
                :src="mainImage"
                :key="mainImage"
                class="rounded border"
                :alt="`Imagen de ${project.name}`"
              />
            </transition>
            <div
              v-if="images.length > 1"
              class="carousel-controls d-flex justify-content-center align-items-center mt-3"
            >
              <button class="carousel-btn" @click="prevImage" aria-label="Imagen anterior">‹</button>
              <div class="d-flex gap-2 mx-3">
                <span
                  v-for="(img, idx) in images"
                  :key="idx"
                  class="indicator"
                  :class="{ active: idx === currentImageIndex }"
                  @click="currentImageIndex = idx"
                ></span>
              </div>
              <button class="carousel-btn" @click="nextImage" aria-label="Imagen siguiente">›</button>
            </div>
          </div>

          <!-- Botones de acción -->
          <div class="action-buttons d-flex flex-column ms-md-4 mt-4 mt-md-0">
            <h1 class="fs-3 fw-semibold text-dark mb-4">{{ project.name }}</h1>
            <p class="text-muted mb-1">Categoría: {{ projectCategory.category }}</p>
            <p class="text-muted mb-3">Propietario: {{ owner.username }}</p>

            <ul class="list-unstyled text-secondary mb-4">
              <li><strong>Meta:</strong> {{ project.goal }} €</li>
              <li><strong>Fecha de inicio:</strong> {{ formattedDate }}</li>
              <li>
                <strong>Estado: </strong>
                <span :class="project.is_active ? 'text-lila' : 'text-danger'">
                  {{ project.is_active ? 'Activo' : 'Cerrado' }}
                </span>
              </li>
            </ul>

            <div class="my-3">
              <label class="form-label">Progreso</label>
              <div class="progress rounded mb-1">
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

            <!-- Acciones según estado y rol -->
            <div class="d-flex h-100 align-items-center">
              <router-link
                v-if="isAuthenticated && !isOwner && project.is_active"
                class="btn btn-outline-secondary-custom w-100 mb-2"
                :to="`/projects/${project.id}/contribute`"
              >
                Contribuir
              </router-link>

              <div v-else-if="isAuthenticated && isOwner">
                <router-link
                  :to="`/projects/${project.id}/contributions`"
                  class="btn btn-outline-secondary-custom w-100 mb-2"
                >
                  Ver contribuciones
                </router-link>
                <button
                  v-if="project.is_active"
                  class="btn btn-outline-danger-custom w-100 mb-2"
                  data-bs-toggle="modal"
                  data-bs-target="#closeModal"
                >
                  Cerrar proyecto
                </button>
                <router-link
                  :to="`/projects/edit/${project.id}`"
                  class="btn btn-outline-secondary text-dark fw-semibold w-100"
                >
                  Editar
                </router-link>
              </div>

              <router-link
                v-else-if="!isAuthenticated && project.is_active"
                to="/auth"
                class="btn btn-outline-secondary-custom w-100"
              >
                Inicia sesión para contribuir
              </router-link>

              <p v-else class="text-muted">El proyecto ya no está disponible. ¡Gracias por el apoyo!</p>
            </div>
          </div>
        </div>

        <!-- Descripción -->
        <div class="project-description mb-5">
          <div class="markdown-body" v-html="renderedTruncatedDescription"></div>
          <button
            v-if="isTruncated"
            class="btn btn-link p-0 text-lila"
            data-bs-toggle="modal"
            data-bs-target="#descriptionModal"
          >
            Ver más
          </button>
        </div>

        <!-- Contribuciones -->
        <section class="project-contributions">
          <h3 class="fs-5 fw-semibold text-dark mb-3">Contribuciones al proyecto</h3>
          <div v-if="contributions.length">
            <ul class="list-unstyled p-0">
              <li
                v-for="c in contributions"
                :key="c.id"
                class="contrib-item p-3 mb-3 bg-white rounded shadow-sm border text-secondary"
              >
                <p class="mb-1"><strong>Contribuidor:</strong> {{ c.contributor?.username || 'Anónimo' }}</p>
                <p class="mb-1 message-text"><strong>Mensaje:</strong> {{ c.message || 'Sin mensaje' }}</p>
                <div class="d-flex justify-content-between mt-2 align-items-center">
                  <small class="text-muted">Fecha: {{ formatDate(c.date) }}</small>
                  <span class="badge bg-gradient-lila text-white fs-6">+{{ c.amount }} €</span>
                </div>
              </li>
            </ul>
          </div>
          <p v-else class="text-muted">Aún no hay contribuciones.</p>
        </section>
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

    <!-- Modal de descripción -->
    <div class="modal fade" id="descriptionModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Descripción completa</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button>
          </div>
          <div class="modal-body markdown-body" v-html="renderedDescription"></div>
          <div class="modal-footer">
            <button class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
  import { ref, onMounted, computed, onUnmounted } from 'vue';
  import { marked } from 'marked';
  import DOMPurify from 'dompurify';
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

  const renderMarkdown = (markdown: string) => {
    const rawHtml = marked(markdown)
    return DOMPurify.sanitize(String(rawHtml))
  }

  const renderedDescription = computed(() => renderMarkdown(project.value.description || ''))
  const renderedTruncatedDescription = computed(() => {
    const truncated = isTruncated.value
    ? project.value.description.slice(0, limit)
    : project.value.description;
    return renderMarkdown(truncated)
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

  const limit = 1000
  const isTruncated = computed(() => {
    return project.value.description.length > limit
  })

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

.action-buttons {
  max-width: 300px;
}

.action-buttons .btn {
  font-size: 0.875rem;
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

.image-carousel img {
  width: 100%;
  object-fit: contain;
  transition: opacity 0.5s ease;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.project-header {
  gap: 2rem;
}

.btn-outline-danger-custom {
  background: linear-gradient(90deg, #dc2626 0%, #f87171 100%);
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
  padding: 0.5rem 1.25rem;
  border-radius: 0.5rem;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  box-shadow: 0 4px 8px rgba(220, 38, 38, 0.3);
  transition: box-shadow 0.3s ease, transform 0.2s ease;
  text-decoration: none;
}

.btn-outline-danger-custom:hover,
.btn-outline-danger-custom:focus {
  box-shadow: 0 6px 12px rgba(220, 38, 38, 0.5);
  transform: translateY(-2px);
  color: white;
  text-decoration: none;
}

.project-description .markdown-body {
  font-size: 1rem;
  line-height: 1.6;
}

.project-contributions .contrib-item {
  background-color: #fff;
}

.markdown-body {
  font-family: 'Inter', sans-serif;
  color: #374151;
  line-height: 1.7;
  letter-spacing: 0.02em;
}

.markdown-body h1,
.markdown-body h2,
.markdown-body h3 {
  color: #1f2937;
  margin-top: 1.5em;
  margin-bottom: 0.75em;
  font-weight: 600;
  line-height: 1.3;
}
.markdown-body h1 { font-size: 2em; border-bottom: 2px solid #e5e7eb; padding-bottom: 0.3em; }
.markdown-body h2 { font-size: 1.75em; border-bottom: 1px solid #e5e7eb; padding-bottom: 0.2em; }
.markdown-body h3 { font-size: 1.5em; }

.markdown-body p {
  margin-bottom: 1em;
}
.markdown-body strong {
  color: #111827;
  font-weight: 600;
}
.markdown-body em {
  color: #4b5563;
  font-style: italic;
}

.markdown-body a {
  color: #7c3aed;
  text-decoration: none;
  position: relative;
}
.markdown-body a::after {
  content: '';
  position: absolute;
  left: 0; bottom: -2px;
  width: 100%;
  height: 2px;
  background: #7c3aed;
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}
.markdown-body a:hover::after {
  transform: scaleX(1);
}

.markdown-body ul,
.markdown-body ol {
  margin: 1em 0;
  padding-left: 1.5em;
}
.markdown-body li {
  margin-bottom: 0.5em;
}

.markdown-body blockquote {
  border-left: 4px solid #e5e7eb;
  background: #f9fafb;
  padding: 0.5em 1em;
  color: #6b7280;
  margin: 1.5em 0;
  font-style: italic;
}

.markdown-body code {
  background: #f3f4f6;
  padding: 0.2em 0.4em;
  border-radius: 0.3em;
  font-family: Menlo, Consolas, monospace;
  font-size: 0.95em;
}
.markdown-body pre {
  background: #1f2937;
  color: #f9fafb;
  padding: 1em;
  border-radius: 0.5em;
  overflow-x: auto;
  margin: 1em 0;
}
.markdown-body pre code {
  background: transparent;
  padding: 0;
  color: inherit;
  font-size: 0.9em;
}

.markdown-body table {
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0;
}
.markdown-body th,
.markdown-body td {
  border: 1px solid #e5e7eb;
  padding: 0.5em 0.75em;
  text-align: left;
}
.markdown-body th {
  background: #f3f4f6;
  font-weight: 600;
}

.markdown-body img {
  max-width: 100%;
  border-radius: 0.5em;
  margin: 1em 0;
}

</style>
