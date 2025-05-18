<template>
	<body class="bg-white text-dark font-sans">
  <div class="container py-5">
    <h2 class="text-center fw-bold mb-2" style="font-size: 1.25rem;">
      Descubre proyectos por categorías
    </h2>
    <p class="text-center text-secondary mb-4" style="font-size: 1rem;">
      Explora una variedad de proyectos en diferentes categorías y encuentra el que más te inspire.
    </p>
    <div class="row g-3">
      <div class="col-12 col-sm-6 col-md-3" v-for="category in projectCategories" :key="category.id" @click="router.push(`/projects?category=${category.id}`)">
        <div class="border card rounded-3 p-4 d-flex flex-column align-items-center">
          <div class="bg-purple icon-circle text-purple rounded-circle p-3 mb-2" :style="{color: `${category.color}`, backgroundColor: `${category.color}30`}">
            <i :class="category.icon"></i>
          </div>
          <p class="fw-semibold mb-0" style="font-size: 0.875rem;">{{ category.category }}</p>
          <p class="text-secondary mb-0" style="font-size: 0.75rem;">{{ category.num_projects }} Proyectos</p>
        </div>
      </div>
    </div>
  </div>
</body>
</template>

<script setup lang="ts">
  import type { ProjectCategory } from '@/interfaces/Project';
  import router from '@/router';
  

  defineProps({
    projectCategories: {
      type: Array as () => ProjectCategory[],
      required: true,
    }
  });

</script>

<style scoped>
  .card {
		transition: transform 0.2s;
		cursor: pointer;
	}
	.card:hover,
	.card:focus-within {
		transform: translateY(-5px);
		box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
	}
  .icon-circle {
    background-color: #ddd6fe;
    color: #7c3aed;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
    font-size: 1.25rem;
  }
</style>