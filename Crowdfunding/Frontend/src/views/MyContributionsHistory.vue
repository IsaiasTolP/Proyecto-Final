<template>
    <div class="container py-4">
      <GoBackBtn />
      <h3 class="mb-4">Contribuciones al Proyecto</h3>

      <div v-if="contributions.length === 0" class="text-muted">
        Aún no hay contribuciones.
      </div>

      <div v-for="(contribution, index) in contributions" :key="contribution.id" class="card mb-3 p-3 shadow-sm">
        <div class="d-flex align-items-center">
          <div class="flex-grow-1">
              Contribución número {{ contributions.length - index }}
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
  import GoBackBtn from '@/components/GoBackBtn.vue';

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
  .card {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  background-color: #ffffff;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.card .flex-grow-1 {
  font-size: 0.95rem;
  color: #374151;
}

.card .fw-semibold {
  color: #16a34a;
}

.card small.text-muted {
  font-size: 0.8rem;
  color: #6b7280 !important;
}

.card q {
  display: block;
  font-style: italic;
  color: #4b5563;
  font-size: 0.92rem;
  margin-top: 0.5rem;
  white-space: pre-wrap;
  word-break: break-word;
}

h3 {
  color: #111827;
  font-weight: 600;
}

.router-link-active,
a {
  text-decoration: none;
  color: #6366f1;
  font-weight: 500;
}

a:hover {
  text-decoration: underline;
}

</style>