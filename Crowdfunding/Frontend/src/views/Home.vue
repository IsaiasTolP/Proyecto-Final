<template>
  <div>
    <section class="py-5">
      <div class="container">
        <h2 class="text-center mb-4" id="projects-heading">Proyectos Actuales</h2>
        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4" aria-labelledby="projects-heading">
          <div class="col" v-for="project in projects" :key="project.id">
            <div class="card h-100 border-success">
              <img
                v-if="project.project_images.length"
                :src="project.project_images[0].image"
                class="card-img-top"
                :alt="`Imagen del proyecto ${project.name}`"
              />
              <div class="card-body d-flex flex-column">
                <h3 class="card-title h5">{{ project.name }}</h3>
                <p class="text-muted mb-1">Categoría: {{ projectCategories.find(cat => cat.id === project.category)?.category }}</p>
                <p class="card-text flex-grow-1">{{ project.description }}</p>
                <router-link
                  :to="`/projects/${project.id}`"
                  class="btn btn-success mt-3"
                  :aria-label="`Ver más sobre ${project.name}`"
                >Ver más</router-link>
              </div>
            </div>
          </div>
        </div>
        <div class="my-4 text-center" v-if="auth.user?.is_founder">
          <router-link to="/project/create" class="btn btn-outline-success"><h2>Crear un nuevo proyecto +</h2></router-link>
        </div>
        
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import api from '@/services/api';
import { useAuthStore } from '@/stores/auth';
import type { Project, ProjectCategory } from '@/interfaces/Project';

const projects = ref<Project[]>([]);
const projectCategories = ref<ProjectCategory[]>([]);
const auth = useAuthStore();

onMounted(async () => {
  try {
    const projectData = await api.get<Project[]>('/projects/list/');
    projects.value = projectData.data;
    const categoriesData = await api.get<ProjectCategory[]>('/projects/categories/');
    projectCategories.value = categoriesData.data
  } catch (error) {
    console.error('Error al cargar los proyectos:', error);
  }
});
</script>

<style scoped>
#projects-heading {
  color: #155724;
}

.card {
  transition: transform 0.2s;
}

.card:hover,
.card:focus-within {
  transform: translateY(-5px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}
</style>