<template>
  <div class="container py-5">
    <h2 class="mb-4 text-success">Resultados de búsqueda</h2>

    <div v-if="loading" class="text-center">Buscando proyectos...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-else-if="projects.length === 0" class="alert alert-info">
      No se encontraron proyectos para "{{ query }}".
    </div>

    <div class="row" v-else>
      <div v-for="project in projects" :key="project.id" class="col-12 mb-3">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ project.name }}</h5>
            <p class="card-text">{{ project.description.slice(0, 100) }}...</p>
            <router-link :to="`/projects/${project.id}`" class="btn btn-success">
              Ver más
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup lang="ts">
import { ref, watchEffect } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/services/api';
import type { Project } from '@/interfaces/Project';

	const route = useRoute();
	const query = ref<string>(route.query.query as string || '');
	const projects = ref<Project[]>([]);
	const loading = ref(false);
	const error = ref('');
	
	watchEffect(async () => {
	  if (!query.value) return;
	
	  loading.value = true;
	  error.value = '';
	  try {
	    const { data } = await api.get(`/projects/list/?search=${encodeURIComponent(query.value)}`);
	    projects.value = data;
	  } catch (e) {
	    error.value = 'Error al buscar proyectos.';
	    console.error(e);
	  } finally {
	    loading.value = false;
	  }
	});
</script>
