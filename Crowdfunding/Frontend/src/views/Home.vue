<template>
  <Hero />
  <Featured :projectCategories="projectCategories"/>
  <Latest :projectCategories="projectCategories"/>
  <HowItWorks />
  <SearchByCategories :projectCategories="projectCategories"/>
  <Impact />
</template>

<script setup lang="ts">
import Hero from '@/components/Hero.vue';
import Featured from '@/components/Featured.vue';
import Latest from '@/components/Latest.vue';
import HowItWorks from '@/components/HowItWorks.vue';
import SearchByCategories from '@/components/SearchByCategories.vue';
import Impact from '@/components/Impact.vue';
import { onMounted, ref } from 'vue';
import type { ProjectCategory } from '@/interfaces/Project';
import { getCategories } from '@/services/sProject';

  const projectCategories = ref<ProjectCategory[]>([]);

	onMounted(async () => {
		try {
			projectCategories.value = await getCategories();
		} catch (error: any) {
			console.log('Error al cargar las categorías:', error);
		}
	});
</script>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap');
		body, h1, p, button {
		font-family: 'Poppins', sans-serif;
  }
  .left-side {
    background-color: #E9F97A;
    position: relative;
    min-height: 100vh;
  }
  .header-left {
    font-size: 1em;
    color: #3B3B3B;
    font-weight: 400;
    text-align: center;
    padding: 1rem 0;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    background-color: #E9F97A;
    z-index: 10;
  }
  .main-left {
    padding-top: 4rem;
    text-align: center;
  }
  .main-left h1 {
    font-weight: 600;
    font-size: 2.5em;
    line-height: 34px;
    color: #121212;
    max-width: 320px;
    margin: 0 auto 1rem auto;
  }
  .main-left p {
    font-size: 1.5em;
    color: #3B3B3B;
    margin-bottom: 2rem;
  }
  .btn-explorar {
    background-color: #121212;
    color: white;
    font-weight: 500;
    font-size: 1.2em;
    border-radius: 9999px;
    padding: 0.5rem 2rem;
    border: none;
  }
  .right-side {
    position: relative;
    min-height: 100vh;
  }
  .btn-menu {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background-color: #121212;
    color: #E9F97A;
    font-weight: 600;
    font-size: 1.1rem;
    border-radius: 4rem;
    padding: 0.5rem 1.25rem;
    border: none;
    z-index: 10;
  }
  .img-right {
    width: 100%;
    height: 100vh;
    object-fit: cover;
  }
</style>