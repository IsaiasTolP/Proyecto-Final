<template>
  <div class="container py-4">
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
      <div class="modal-dialog modal-dialog-centered">
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
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'

interface Project {
  id: number
  name: string
  description: string
  goal: number
  total_donated: number
  percent_completed: number
  is_active: boolean
  start_date: string
}

const projects = ref<Project[]>([])
const authStore = useAuthStore()
const userId = authStore.user?.id

// Para eliminar
const showModal = ref(false)
const projectToDelete = ref<number | null>(null)

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
</script>

<style scoped>
.card {
  transition: all 0.2s ease-in-out;
}
.card:hover {
  transform: scale(1.01);
}
.modal {
  background-color: rgba(0, 0, 0, 0.5);
}
.modal .modal-dialog {
  max-width: 400px;
}
</style>
