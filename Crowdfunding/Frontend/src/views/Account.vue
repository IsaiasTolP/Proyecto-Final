<template>
    <div>
      <section class="container py-5">
        <button class="btn btn-link text-success mb-3" @click="goBack">← Volver</button>
  
        <div v-if="loading" class="text-center">
          Cargando perfil...
        </div>
        <div v-else-if="error" class="alert alert-danger">
          {{ error }}
        </div>
        <div v-else class="row align-items-center">
          <!-- Avatar -->
          <div class="col-md-4 text-center mb-4 mb-md-0">
            <img
              :src="profile.pfp"
              :alt="`Foto de perfil de ${profile.user.username}`"
              class="rounded-circle img-fluid"
              style="width: 150px; height: 150px; object-fit: cover;"
            />
          </div>
  
          <!-- Datos de perfil -->
          <div class="col-md-8">
            <h1 class="mb-2">{{ profile.user.username }}</h1>
            <p class="text-muted mb-1" v-if="profile.is_founder">Fundador</p>
            <p class="mb-3">{{ profile.bio || 'Este usuario no ha añadido una biografía.' }}</p>
            <p class="mb-3" v-if="profile.location"><strong>Ubicación:</strong> {{ profile.location }}</p>
  
            <!-- Opciones para el dueño -->
            <div v-if="isOwner" class="mt-4">
              <router-link to="/profile/edit" class="btn btn-success me-2">Editar Perfil</router-link>
              <router-link to="/payment-methods" class="btn btn-outline-success">Métodos de Pago</router-link>
            </div>
          </div>
        </div>
      </section>
    </div>
  </template>
  
<script setup lang="ts">
  import { ref, onMounted, computed } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import api from '@/services/api';
  import { useAuthStore } from '@/stores/auth';
  
  // Interfaces
  interface User {
    id: number;
    username: string;
  }
  
  interface ProfileData {
    user: User;
    bio: string;
    pfp: string;
    location: string;
    is_founder: boolean;
  }
  
  const route = useRoute();
  const router = useRouter();
  const auth = useAuthStore();
  
  const profile = ref<ProfileData>({} as ProfileData);
  const currentUser = auth.user;
  const loading = ref(true);
  const error = ref('');
  
  const isOwner = computed(() => !!currentUser && currentUser.id === profile.value.user.id);
  
  function goBack() {
    router.back();
  }
  
  async function fetchProfile() {
    loading.value = true;
    error.value = '';
    try {
      const userId = route.params.id;
      const { data } = await api.get<ProfileData>(`/accounts/profiles/user/${userId}/`);
      profile.value = data;
    } catch (err: any) {
      error.value = 'Error al cargar el perfil.';
    } finally {
      loading.value = false;
    }
  }
  
  onMounted(async () => {
    await fetchProfile();
  });
</script>

<style scoped>
  .btn-link:hover {
    text-decoration: underline;
  }
</style>