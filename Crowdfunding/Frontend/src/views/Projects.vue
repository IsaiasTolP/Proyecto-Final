<template>
  <div>
    <section class="py-5">
      <div class="container">

        <!-- Select para filtrar por categoría -->
        <div class="mb-4 text-end">
          <label for="category-filter" class="me-2">Filtrar por categoría:</label>
          <select
            id="category-filter"
            v-model="selectedCategory"
            @change="updateCategoryInURL"
            class="form-select d-inline-block w-auto"
          >
            <option value="">Todas las categorías</option>
            <option v-for="cat in projectCategories" :key="cat.id" :value="cat.id">
              {{ cat.category }}
            </option>
          </select>
        </div>

        <h2 class="text-center mb-4" id="projects-heading">Proyectos Actuales</h2>

        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4" aria-labelledby="projects-heading">
          <div class="col" v-for="project in filteredProjects" :key="project.id">
            <div class="card h-100 border-success">
              <img
                v-if="project.project_images.length"
                :src="project.project_images[0].image"
                class="card-img-top"
                :alt="`Imagen del proyecto ${project.name}`"
              />
              <div class="card-body d-flex flex-column">
                <h3 class="card-title h5">{{ project.name }}</h3>
                <p class="text-muted mb-1">
                  Categoría: {{ projectCategories.find(cat => cat.id === project.category)?.category }}
                </p>
                <p class="card-text flex-grow-1">
                  {{ project.description.length > 140 ? project.description.slice(0, 140) + '...' : project.description }}
                </p>
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
          <router-link to="/project/create" class="btn btn-outline-success">
            <h2>Crear un nuevo proyecto +</h2>
          </router-link>
        </div>

      </div>
    </section>
  </div>
</template>


<script setup lang="ts">
import { onMounted, ref, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';
import { useAuthStore } from '@/stores/auth';
import type { Project, ProjectCategory } from '@/interfaces/Project';

const projects = ref<Project[]>([]);
const projectCategories = ref<ProjectCategory[]>([]);
const selectedCategory = ref<string | null>(null);

const auth = useAuthStore();
const route = useRoute();
const router = useRouter();

onMounted(async () => {
  try {
    const [projectData, categoriesData] = await Promise.all([
      api.get<Project[]>('/projects/list/', {
        params: {
          ordering: '-start_date'
        }
      }),
      api.get<ProjectCategory[]>('/projects/categories/')
    ]);

    projects.value = projectData.data;
    projectCategories.value = categoriesData.data;

    // Si la URL ya tiene un filtro al cargar
    const initialCategory = route.query.category as string;
    if (initialCategory) {
      selectedCategory.value = initialCategory;
    }
  } catch (error) {
    console.error('Error al cargar los proyectos:', error);
  }
});

// Reacciona a cambios en la URL (por navegación, back, etc.)
watch(() => route.query.category, (newCategory) => {
  selectedCategory.value = newCategory as string || '';
});

// Reacciona a cambios en el select y actualiza la URL sin recargar
watch(selectedCategory, (newVal) => {
  const query = { ...route.query };

  if (newVal) {
    query.category = newVal;
  } else {
    delete query.category;
  }

  router.replace({ query }); // Usamos replace para no agregar al historial
});

// Computed para filtrar proyectos por categoría seleccionada
const filteredProjects = computed(() => {
  if (!selectedCategory.value) {
    return projects.value;
  }
  return projects.value.filter(
    (p) => String(p.category) === selectedCategory.value
  );
});

// Función para actualizar el parámetro en la URL
function updateCategoryInURL() {
  const query = { ...route.query };

  if (selectedCategory.value) {
    query.category = selectedCategory.value;
  } else {
    delete query.category;
  }

  router.push({ query });
}
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