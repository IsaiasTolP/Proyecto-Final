<template>
  <div class="project-wrapper">
    <section class="py-5">
      <div class="container">

        <!-- Filtro -->
        <div class="d-flex justify-content-end mb-4 align-items-center gap-2">
          <label for="category-filter" class="mb-0 text-secondary fw-semibold small">Filtrar por categoría:</label>
          <select
            id="category-filter"
            v-model="selectedCategory"
            @change="updateCategoryInURL"
            class="form-select w-auto form-select-sm"
          >
            <option value="">Todas</option>
            <option v-for="cat in projectCategories" :key="cat.id" :value="cat.id">
              {{ cat.category }}
            </option>
          </select>
        </div>
        
        <!-- Crear nuevo proyecto -->
        <div class="my-5 text-center" v-if="auth.user?.is_founder">
          <router-link to="/project/create" class="btn-outline-secondary-custom text-decoration-none">
            <i class="fas fa-plus"></i>
            <span>Crear nuevo proyecto</span>
          </router-link>
        </div>

        <h2 class="text-center fw-semibold mb-5 fs-2 text-dark">Proyectos Actuales</h2>

        <!-- Lista de proyectos -->
        <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
          <div class="col" v-for="project in filteredProjects" :key="project.id">
            <div class="card h-100 project-card">
              <img
                v-if="project.project_images.length"
                :src="project.project_images[0].image"
                class="card-img-top"
                :alt="`Imagen del proyecto ${project.name}`"
                style="object-fit: cover; height: 20rem;"
              />
              <div class="card-body d-flex flex-column">
                <h3 class="card-title fs-6 fw-semibold text-dark mb-1">{{ project.name }}</h3>
                <p class="text-secondary small mb-2">
                  Categoría: {{ projectCategories.find(cat => cat.id === project.category)?.category }}
                </p>
                <router-link
                  :to="`/projects/${project.id}`"
                  class="btn-outline-secondary-custom mt-3 text-decoration-none text-center"
                  :aria-label="`Ver más sobre ${project.name}`"
                >
                  Ver más
                </router-link>
              </div>
            </div>
          </div>
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
.project-wrapper {
  font-family: 'Inter', sans-serif;
  background-color: #fff;
  color: #1e293b;
}

.project-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  box-shadow: 0 1px 2px rgb(0 0 0 / 0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 12px rgba(124, 58, 237, 0.1);
}

.btn-outline-secondary-custom {
  background: linear-gradient(90deg, #7c3aed 0%, #a78bfa 100%);
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
  padding: 0.5rem 1.25rem;
  border-radius: 0.5rem;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 8px rgba(124, 58, 237, 0.3);
  transition: box-shadow 0.3s ease, transform 0.2s ease;
  cursor: pointer;
}

.btn-outline-secondary-custom:hover,
.btn-outline-secondary-custom:focus {
  box-shadow: 0 6px 12px rgba(124, 58, 237, 0.5);
  transform: translateY(-2px);
  text-decoration: none;
  color: white;
}

.text-secondary {
  color: #6b7280 !important;
}
</style>
