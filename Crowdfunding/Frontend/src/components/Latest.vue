<template>
	<body v-if="projects.length">
		<main class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-3 flex-wrap">
      <div>
        <h2 class="fw-semibold mb-1" style="font-size: 1.5rem; line-height: 1.25;">Ponte al Día</h2>
        <p class="text-secondary mb-0" style="font-size: 0.875rem; max-width: 320px;">Descubre las innovaciones recién instaladas en nuestra plataforma</p>
      </div>
      <router-link to="/projects" class="view-all mt-2 mt-sm-0">
        Ver todos los proyectos
        <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" >
          <path d="M5 12h14M13 6l6 6-6 6"></path>
        </svg>
      </router-link>
    </div>
    <div class="row g-3">
      <div class="col-12 col-sm-6 col-lg-4" v-for="project in projects" :key="project.id" @click="router.push(`/projects/${project.id}`)">
        <div class="card border border-2 rounded shadow-sm h-100">
          <div class="position-relative">
            <img v-if="project.project_images.length" :src="`${project.project_images[0].image}`" :alt="`Imagen del proyecto ${project.name}`" class="card-img-top" style="height: 20rem; object-fit: cover;" />
            <span class="badge-category">{{ projectCategories.find(cat => cat.id === project.category)?.category }}</span>
          </div>
          <div class="card-body p-3">
            <h3 class="card-title mb-1">{{ project.name }}</h3>
            <p class="card-text mb-3">{{ project.description.length > 140 ? project.description.slice(0, 140) + '...' : project.description }}</p>
            <div class="d-flex align-items-center mb-2 gap-2">
              <div class="progress flex-grow-1" role="progressbar" aria-label="Progress bar 84% filled" aria-valuenow="84" aria-valuemin="0" aria-valuemax="100">
                <div class="progress-bar" :style="{ width: project.percent_completed + '%' }"></div>
              </div>
              <span class="fw-semibold" style="font-size: 0.75rem;">{{ project.total_donated }} € Conseguidos</span>
              <span class="text-secondary fw-semibold" style="font-size: 0.75rem;">{{ project.percent_completed }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
	</body>
	
</template>

<script setup lang="ts">
	import api from '@/services/api';
	import { onMounted, ref } from 'vue';
	import type { ProjectCategory, Project } from '@/interfaces/Project';
	import router from '@/router';

	const projects = ref<Project[]>([]);


  defineProps({
    projectCategories: {
      type: Array as () => ProjectCategory[],
      required: true,
    }
  });


	onMounted(async () => {
		try {
			const { data: projectsData } = await api.get('/projects/list/latest/');
			projects.value = projectsData;
		} catch (error: any) {
			console.log('Error al cargar los proyectos:', error);
		}
	});
</script>

<style scoped>
		body {
      font-family: 'Inter', sans-serif;
      background-color: #fff;
      color: #1f2937;
    }
		.card {
			transition: transform 0.2s;
			cursor: pointer;
		}

		.card:hover,
		.card:focus-within {
			transform: translateY(-5px);
			box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
		}
    .card-title {
      font-weight: 600;
      font-size: 1rem;
      line-height: 1.25rem;
    }
    .card-text {
      color: #4b5563;
      font-size: 0.875rem;
      line-height: 1.25rem;
    }
    .progress {
      height: 4px;
      border-radius: 9999px;
      background-color: #e5e7eb;
    }
    .progress-bar {
      background-color: #111827;
    }
    .badge-category {
      position: absolute;
      top: 0.75rem;
      right: 0.75rem;
      background-color: #fff;
      color: #1f2937;
      font-size: 0.75rem;
      font-weight: 600;
      padding: 0.25rem 0.75rem;
      border-radius: 9999px;
      box-shadow: 0 1px 2px rgb(0 0 0 / 0.1);
      white-space: nowrap;
    }
    a.view-all {
      color: #7c3aed;
      font-weight: 500;
      font-size: 0.875rem;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
    }
    a.view-all:hover {
      text-decoration: underline;
      color: #5b21b6;
    }
    a.view-all svg {
      margin-left: 0.25rem;
      width: 1rem;
      height: 1rem;
      stroke: currentColor;
      stroke-width: 2;
      stroke-linecap: round;
      stroke-linejoin: round;
      fill: none;
    }
</style>
