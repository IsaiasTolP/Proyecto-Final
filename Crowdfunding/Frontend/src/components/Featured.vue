<template>
  <body v-if="projects.length">
    <main class="container py-4">
      <!-- Cabecera idéntica -->
      <div class="d-flex justify-content-between align-items-center mb-3 flex-wrap">
        <div>
          <h2 class="fw-semibold mb-1" style="font-size: 1.5rem; line-height: 1.25;">Proyectos Destacados</h2>
          <p class="text-secondary mb-0" style="font-size: 0.875rem; max-width: 320px;">
            Descubre las innovaciones que están causando sensación en este momento
          </p>
        </div>
        <router-link to="/projects" class="view-all mt-2 mt-sm-0">
          Ver todos los proyectos
        </router-link>
      </div>

      <!-- SWITCH: slider si hay más de 3, si no la grid normal -->
      <template v-if="projects.length > 3">
        <div class="projects-slider-wrapper position-relative">
          <!-- Botones fuera del slider -->
          <button class="custom-swiper-button-prev" ref="prevEl">
            ‹
          </button>
          <button class="custom-swiper-button-next" ref="nextEl">
            ›
          </button>
        
          <!-- Slider -->
          <Swiper
            :modules="[Navigation]"
            :slides-per-view="3"
            :space-between="16"
            :navigation="{ prevEl: prevEl, nextEl: nextEl }"
            class="projects-swiper"
          >
            <SwiperSlide
              v-for="project in projects"
              :key="project.id"
              @click="goTo(project.id)"
            >
              <FeaturedProjectCard :project="project" :categories="projectCategories" />
            </SwiperSlide>
          </Swiper>
        </div>
      </template>
      <template v-else>
        <div class="row g-3">
          <div
            class="col-12 col-sm-6 col-lg-4"
            v-for="project in projects"
            :key="project.id"
            @click="goTo(project.id)"
          >
            <FeaturedProjectCard :project="project" :categories="projectCategories" />
          </div>
        </div>
      </template>
    </main>
  </body>
</template>

<script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import api from '@/services/api';
  import { Swiper, SwiperSlide } from 'swiper/vue';
  import 'swiper/swiper-bundle.css';
  import { Navigation } from 'swiper/modules';
  import type { Project, ProjectCategory } from '@/interfaces/Project';
  import FeaturedProjectCard from './FeaturedProjectCard.vue';

  const projects = ref<Project[]>([]);
  const router = useRouter();

  const prevEl = ref<HTMLElement | null>(null);
  const nextEl = ref<HTMLElement | null>(null);

  defineProps<{
    projectCategories: ProjectCategory[];
  }>();

  onMounted(async () => {
    try {
      const { data } = await api.get('/projects/list/featured/');
      projects.value = data;
    } catch (e) {
      console.error('Error al cargar los proyectos:', e);
    }
  });

  function goTo(id: number) {
    router.push(`/projects/${id}`);
  }
</script>

<style scoped>
		body {
      font-family: 'Inter', sans-serif;
      background-color: #fff;
      color: #1f2937;
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
    .projects-slider-wrapper {
    position: relative;
    padding: 0 2rem;
  }

  .projects-swiper {
    overflow: hidden;
  }

  .custom-swiper-button-prev,
  .custom-swiper-button-next {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    z-index: 10;
    background: white;
    border: 1px solid #ccc;
    border-radius: 50%;
    width: 2.5rem;
    height: 2.5rem;
    font-size: 1.5rem;
    font-weight: bold;
    color: #333;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: background 0.3s;
  }

  .custom-swiper-button-prev:hover,
  .custom-swiper-button-next:hover {
    background: #f3f4f6;
  }

  .custom-swiper-button-prev {
    left: -1.5rem;
  }

  .custom-swiper-button-next {
    right: -1.5rem;
  }

  @media (max-width: 768px) {
    .custom-swiper-button-prev,
    .custom-swiper-button-next {
      display: none;
    }
  }
</style>
