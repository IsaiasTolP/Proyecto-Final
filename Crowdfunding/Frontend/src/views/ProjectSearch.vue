<template>
  <div class="container py-5" style="max-width: 768px;">
    <h2 class="mb-4 fw-semibold text-dark fs-5">Resultados de búsqueda</h2>

    <div v-if="loading" class="text-center text-secondary small">Buscando proyectos...</div>

    <div v-else-if="error" class="alert alert-danger text-sm">
      {{ error }}
    </div>

    <div v-else-if="projects.length === 0" class="alert alert-light border text-secondary text-sm">
      No se encontraron proyectos para <strong>"{{ query }}"</strong>.
    </div>

    <div v-else class="d-flex flex-column gap-3">
      <div v-for="project in projects" :key="project.id" class="project-card p-3">
        <h5 class="fw-semibold text-dark mb-1">{{ project.name }}</h5>
        
        <ul class="list-unstyled text-secondary small mb-2">
          <li><strong>Meta:</strong> {{ project.goal }} €</li>
          <li><strong>Fecha de inicio:</strong> {{ formatDate(project.start_date) }}</li>
          <li>
            <strong>Estado: </strong>
            <span :class="project.is_active ? 'text-success' : 'text-danger'">
              {{ project.is_active ? 'Activo' : 'Cerrado' }}
            </span>
          </li>
        </ul>

        <router-link
          :to="`/projects/${project.id}`"
          class="btn-outline-secondary-custom d-inline-flex align-items-center"
          :aria-label="`Ver más sobre ${project.name}`"
        >
          Ver más
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watchEffect } from 'vue';
import { useRoute } from 'vue-router';
import type { Project } from '@/interfaces/Project';
import { getProjectByQuery } from '@/services/sProject';

const route = useRoute();
const query = ref<string>(route.query.query as string || '');
const projects = ref<Project[]>([]);
const loading = ref(false);
const error = ref('');

watchEffect(async () => {
  if (!query.value) return;

  loading.value = true;
  error.value = '';
  try {;
    projects.value = await getProjectByQuery(query.value);
  } catch (e) {
    error.value = 'Error al buscar proyectos.';
    console.error(e);
  } finally {
    loading.value = false;
  }
});

function formatDate(dateStr: string): string {
  const date = new Date(dateStr);
  return date.toLocaleDateString('es-ES', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  });
}
</script>

<style scoped>
.project-card {
  background-color: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.2s ease;
}

.project-card:hover {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
}

.btn-outline-secondary-custom {
  background: linear-gradient(90deg, #7c3aed 0%, #a78bfa 100%);
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
  padding: 0.5rem 1.25rem;
  border-radius: 0.5rem;
  border: none;
  box-shadow: 0 4px 8px rgba(124, 58, 237, 0.3);
  transition: box-shadow 0.3s ease, transform 0.2s ease;
  cursor: pointer;
  text-decoration: none;
}

.btn-outline-secondary-custom:hover,
.btn-outline-secondary-custom:focus {
  box-shadow: 0 6px 12px rgba(124, 58, 237, 0.5);
  transform: translateY(-2px);
  outline: none;
  color: white;
  text-decoration: none;
}

.text-success {
  color: #16a34a; /* verde */
}
.text-danger {
  color: #dc2626; /* rojo */
}
</style>
