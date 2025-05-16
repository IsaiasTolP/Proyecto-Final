<template>
    <div class="container py-4">
      <h3 class="mb-4">Contribuciones al Proyecto</h3>

      <div v-if="contributions.length === 0" class="text-muted">
        Aún no hay contribuciones.
      </div>

      <div v-for="contribution in contributions" :key="contribution.id" class="card mb-3 p-3 shadow-sm">
        <div class="d-flex align-items-center">
          <div class="flex-grow-1">
              Contribución número {{ contribution.id }}
            <div>
              <small class="text-muted">{{ formatDate(contribution.date) }}</small>
            </div>
            <div class="mt-1">
              <span class="fw-semibold text-success">Contribuiste </span>
              con {{ contribution.amount }} € al proyecto 
							<router-link :to="`/projects/${contribution.simpleProject?.id}`">{{ contribution.simpleProject?.name }}</router-link> del fundador 
							<router-link :to="`/profile/${contribution.simpleProject?.owner.id}`">{{ contribution.simpleProject?.owner.username }}</router-link>
            </div>
            <div v-if="contribution.message" class="mt-2">
              <q>{{ contribution.message }}</q>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup lang="ts">
  import { onMounted, ref } from 'vue';
  import api from '@/services/api';
  import { useRoute } from 'vue-router';
	import type { SimpleProject } from '@/interfaces/Project';
	import type { Contribution } from '@/interfaces/Contribution';

  const route = useRoute();
  const userId = route.params.id
  const contributions = ref<Contribution[]>([]);
  
  onMounted(() => {
    fetchContributions();
  });
  
  async function fetchContributions() {
    try {
      const { data: contribution } = await api.get('/contributions/list/', {
        params: {
          contributor: String(userId),
          ordering: '-date',
        },
      });
      contributions.value = contribution;
			const projects = await Promise.all(
				contributions.value.map(contribution => fetchProject(contribution.project))
			);
			contributions.value.forEach((contribution, index) => {
				if (projects[index]) {
					contribution.simpleProject = projects[index];
				}
			});
    } catch (err: any) {
      console.error('Error al obtener contribuciones:', err);
    }
  }

	async function fetchProject(projectId: number) {
		try {
			const { data: simpleProject } = await api.get<SimpleProject>(`/projects/simple-project-list/${projectId}/`)
			return simpleProject
		} catch(err: any) {
			console.error('Error al obtener el perfil', err);
			return null
		}
	}
  
  function formatDate(dateStr: string) {
    const date = new Date(dateStr);
    return date.toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  }
  </script>
  
  <style scoped>
  .card img {
    object-fit: cover;
  }
</style>