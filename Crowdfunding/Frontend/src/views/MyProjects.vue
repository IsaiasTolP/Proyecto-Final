<template>
  <div class="container py-4">
    <GoBackBtn />
    <h3 class="mb-4">Mis Proyectos</h3>

    <div v-if="projects.length === 0" class="text-muted">
      Aún no has creado ningún proyecto.
    </div>

    <div
      v-for="project in projects"
      :key="project.id"
      class="card mb-3 shadow-sm p-3 position-relative"
    >
      <h5 class="fw-bold">{{ project.name }}</h5>

      <div class="text-muted mb-1">
        Meta: {{ project.goal }} € |
        Recaudado: {{ project.total_donated }} € ({{ project.percent_completed }}%)
      </div>

			<div>
				<router-link
        	:to="`/projects/${project.id}`"
        	class="btn btn-sm btn-outline-primary mt-2 me-2"
      	>
        	Ver Detalles
      	</router-link>
        <button
        v-if="!project.featured"
        @click="FeatureForm(project.id)"
        class="btn btn-sm btn-outline-primary mt-2 me-2">Patrocinar</button>
				<router-link
        	:to="`/projects/edit/${project.id}`"
        	class="btn btn-sm btn-outline-secondary mt-2 me-2"
      	>
        	Editar
      	</router-link>
				<button
        	class="btn btn-sm btn-outline-danger mt-2"
        	@click="confirmDelete(project.id)"
      	>
        	Eliminar
      	</button>
			</div>
    </div>

    <!-- Modal de confirmación -->
    <div
      class="modal fade"
      tabindex="-1"
      :class="{ show: showModal }"
      style="display: block;"
      v-if="showModal"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">¿Eliminar proyecto?</h5>
            <button type="button" class="btn-close" @click="cancelDelete"></button>
          </div>
          <div class="modal-body">
            <p>Esta acción no se puede deshacer. ¿Seguro que quieres eliminar este proyecto?</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="cancelDelete">Cancelar</button>
            <button class="btn btn-danger" @click="deleteProject">Eliminar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <FeatureProject
    v-if="showFeatureModal && selectedProjectId"
    :project-id="selectedProjectId"
    @close="closeFeatureModal"
    @featured="markAsFeatured"
  />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'
import type { Project } from '@/interfaces/Project'
import FeatureProject from '@/components/FeatureProject.vue'
import GoBackBtn from '@/components/GoBackBtn.vue'

const projects = ref<Project[]>([])
const authStore = useAuthStore()
const userId = authStore.user?.id

// Para eliminar
const showModal = ref(false)
const projectToDelete = ref<number | null>(null)
// Para patrocinar
const showFeatureModal = ref(false)
const selectedProjectId = ref<number | null>(null)

onMounted(() => {
  fetchProjects()
})

async function fetchProjects() {
  try {
    const { data } = await api.get('/projects/list/', {
      params: {
        owner: userId,
        ordering: '-start_date',
      },
    })
    projects.value = data
  } catch (err) {
    console.error('Error al obtener proyectos:', err)
  }
}

function confirmDelete(projectId: number) {
  showModal.value = true
  projectToDelete.value = projectId
}

function cancelDelete() {
  showModal.value = false
  projectToDelete.value = null
}

async function deleteProject() {
  if (!projectToDelete.value) return
  try {
    await api.delete(`/projects/list/${projectToDelete.value}/`)
    projects.value = projects.value.filter(p => p.id !== projectToDelete.value)
  } catch (err) {
    console.error('Error al eliminar el proyecto:', err)
  } finally {
    cancelDelete()
  }
}

function FeatureForm(projectId: number) {
  selectedProjectId.value = projectId
  showFeatureModal.value = true
}

function closeFeatureModal() {
  showFeatureModal.value = false
  selectedProjectId.value = null
}

function markAsFeatured(projectId: number) {
  const project = projects.value.find(p => p.id === projectId)
  if (project) project.featured = true
}
</script>

<style scoped>
.card {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  background-color: #ffffff;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.card h5 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
  margin-bottom: 0.5rem;
}

.text-muted {
  font-size: 0.95rem;
  color: #6b7280 !important;
}

.btn {
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 0.375rem;
}

.btn-outline-primary {
  border-color: #6366f1;
  color: #6366f1;
}

.btn-outline-primary:hover {
  background-color: #6366f1;
  color: white;
}

.btn-outline-secondary {
  border-color: #9ca3af;
  color: #4b5563;
}

.btn-outline-secondary:hover {
  background-color: #9ca3af;
  color: white;
}

.btn-outline-danger {
  border-color: #ef4444;
  color: #ef4444;
}

.btn-outline-danger:hover {
  background-color: #ef4444;
  color: white;
}

.modal {
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}

.modal-dialog {
  max-width: 420px;
  border-radius: 0.75rem;
  background-color: white;
  padding: 1.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.modal-content {
  border: none;
  border-radius: 0.75rem;
}

.modal-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}

.modal-body p {
  font-size: 0.95rem;
  color: #374151;
  margin-bottom: 0;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.25rem;
  color: #6b7280;
}

.btn-close:hover {
  color: #111827;
}

</style>
