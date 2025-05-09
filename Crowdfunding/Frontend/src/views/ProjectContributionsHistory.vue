<template>
    <div class="container py-4">
      <h3 class="mb-4">Contribuciones al Proyecto</h3>

      <div v-if="contributions.length === 0" class="text-muted">
        Aún no hay contribuciones.
      </div>

      <div v-for="contribution in contributions" :key="contribution.id" class="card mb-3 p-3 shadow-sm">
        <div class="d-flex align-items-center">
          <router-link :to="`/profile/${contribution.contributor.id}`" class="me-3">
            <img
              :src="String(contribution.profile?.pfp)"
              alt="Foto de perfil"
              class="rounded-circle"
              width="50"
              height="50"
            />
          </router-link>

          <div class="flex-grow-1">
            <router-link
              :to="`/profile/${contribution.contributor.id}`"
              class="text-decoration-none fw-bold"
            >
              {{ contribution.contributor.username }}
            </router-link>
            <div>
              <small class="text-muted">{{ formatDate(contribution.date) }}</small>
            </div>
            <div class="mt-1">
              <span class="fw-semibold text-success">Contribuyó con</span>
              {{ contribution.amount }} €
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
  import type { ProfileData } from '@/interfaces/Account';
  import { useRoute } from 'vue-router';
  import type { Contribution } from '@/interfaces/Contribution';

  const route = useRoute();
  const projectId = route.params.id
  const contributions = ref<Contribution[]>([]);
  
  onMounted(() => {
    fetchContributions();
  });
  
  async function fetchContributions() {
    try {
      const { data: contribution } = await api.get<Contribution[]>('/contributions/', {
        params: {
          project: String(projectId),
          ordering: '-date',
        },
      });
      contributions.value = contribution;
      const profiles = await Promise.all(
        contributions.value.map(contribution => fetchProfile(contribution.contributor.id))
      );
      contributions.value.forEach((contribution, index) => {
        if (profiles[index]) {
          contribution.profile = profiles[index];
        }
      });
    } catch (err: any) {
      console.error('Error al obtener contribuciones:', err);
    }
  }

	async function fetchProfile(userId: number) {
		try {
			const { data: profileData } = await api.get<ProfileData>(`/accounts/profiles/user/${userId}/`)
			return profileData;
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