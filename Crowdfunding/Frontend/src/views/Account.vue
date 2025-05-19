<template>
  <div v-if="loading" class="text-center">
    Cargando perfil...
  </div>
  
<body v-else>
  <main class="container py-5" style="max-width: 768px;">
    <GoBackBtn />
    <h1 v-if="isOwner" class="text-center fw-semibold mb-4 fs-5">Mi Perfil</h1>
    <h1 v-else class="text-center fw-semibold mb-4 fs-5">Perfil de {{ profile.user?.username }}</h1>
    <section class="profile-card">
      <div class="d-flex align-items-center mb-3">
        <img
        :alt="`Foto de perfil de ${profile.user?.username}`"
        class="rounded-circle me-4" 
        :src="typeof profile.pfp === 'string' ? profile.pfp : undefined"
        height="100" 
        width="100"
        style="object-fit: cover;" />
        <div class="flex-grow-1">
          <div class="d-flex align-items-center gap-2">
            <h2 class="fw-semibold mb-0 fs-6 text-dark">{{ profile.user?.username }}</h2>
            <span v-if="profile.is_founder" class="verified-badge">✓ Fundador</span>
            <span v-else class="verified-badge">Patrocinador</span>
          </div>
          <p class="text-secondary small mt-1 mb-2" style="max-width: 480px; line-height: 1.4;">
            {{ profile.bio }}
          </p>
          <div class="d-flex flex-wrap align-items-center text-secondary small gap-3" style="max-width: 480px;">
            <div class="d-flex align-items-center gap-1">
              <i class="fas fa-map-marker-alt"></i>
              <span>{{ profile.location }}</span>
            </div>
            <div class="d-flex align-items-center gap-1">
              <i class="fas fa-link"></i>
              <a href="#" class="text-secondary">{{ profile.website }}</a>
            </div>
            <div class="d-flex align-items-center gap-1">
              <i class="fas fa-envelope"></i>
              <a href="mailto:carlos@ejemplo.com" class="text-secondary">{{ profile.contact_email }}</a>
            </div>
          </div>
        </div>
      </div>
      <div class="d-flex flex-column flex-sm-row align-items-center justify-content-between border-top border-bottom border-2 border-light py-3 mb-3 gap-3">
        <div v-if="profile.is_founder" class="d-flex gap-3 justify-content-center">
          <a v-if="profile.social_media.instagram" :href="profile.social_media.instagram" aria-label="Instagram" class="icon-circle">
            <i class="fab fa-instagram"></i>
          </a>
          <a v-if="profile.social_media.twitter" :href="profile.social_media.twitter" aria-label="Twitter" class="icon-circle">
            <i class="fab fa-twitter"></i>
          </a>
          <a v-if="profile.social_media.linkedin" :href="profile.social_media.linkedin" aria-label="LinkedIn" class="icon-circle">
            <i class="fab fa-linkedin-in"></i>
          </a>
        </div>
        <div v-if="isOwner" class="d-flex flex-wrap justify-content-center justify-content-sm-end gap-3">
          <button type="button" class="btn-outline-secondary-custom" @click="router.push('/user/edit')">
            <i class="fas fa-edit"></i>
            <span>Editar Usuario</span>
          </button>
          <button type="button" class="btn-outline-secondary-custom" @click="router.push('/profile/edit')">
            <i class="fas fa-edit"></i>
            <span>Editar Perfil</span>
          </button>
          <button type="button" class="btn btn-outline-secondary btn-sm text-dark fw-semibold" style="font-size: 0.75rem; padding: 0.375rem 1rem;" @click="router.push('/payment-methods')">
            Métodos de Pago
          </button>
          <button type="button" class="btn btn-outline-secondary btn-sm text-dark fw-semibold" style="font-size: 0.75rem; padding: 0.375rem 1rem;" @click="router.push(`/profile/${auth.user?.id}/contributions`)">
            Transacciones
          </button>
          <button v-if="auth.user?.is_founder" type="button" class="btn btn-outline-secondary btn-sm text-dark fw-semibold" style="font-size: 0.75rem; padding: 0.375rem 1rem;"  @click="router.push('/projects/me')">
            Mis Proyectos
          </button>
        </div>
      </div>
      <div class="d-flex justify-content-around text-center text-secondary small fw-normal">
        <div>
          <p class="stats-number mb-0">12</p>
          <p class="mb-0">Proyectos Creados</p>
        </div>
        <div>
          <p class="stats-number mb-0">47</p>
          <p class="mb-0">Proyectos Apoyados</p>
        </div>
        <div>
          <p class="stats-number mb-0">€15,250</p>
          <p class="mb-0">Fondos Aportados</p>
        </div>
      </div>
    </section>
  </main>
</body>
</template>

<script setup lang="ts">
	import { ref, onMounted, computed } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import api from '@/services/api';
  import { useAuthStore } from '@/stores/auth';
  import type { FounderProfileData, ProfileData } from '@/interfaces/Account';
  import GoBackBtn from '@/components/GoBackBtn.vue';
  
  const route = useRoute();
  const router = useRouter();
  const auth = useAuthStore();
  
  
  const profile = ref<FounderProfileData>({} as FounderProfileData);
  const currentUser = auth.user;
  const loading = ref(true);
  
  const isOwner = computed(() => !!currentUser && currentUser.id === profile.value.user?.id);
  
  async function fetchProfile() {
    loading.value = true;
    try {
      let isFounder: boolean | undefined;
      const userId = route.params.id;
      if (userId !== String(auth.user?.id)) {
        const { data: user } = await api.get<ProfileData>(`/users/${userId}/`)
        isFounder = user.is_founder
      } else {
        isFounder = auth.user?.is_founder;
      }
      const url = isFounder ? `/accounts/founders/user/${userId}/` : `/accounts/profiles/user/${userId}/`
      const { data } = await api.get<FounderProfileData>(url);
      profile.value = data;
    } catch (err: any) {
    } finally {
      loading.value = false;
    }
  }
  
  onMounted(async () => {
    await fetchProfile();
  });
</script>

<style scoped>
    body {
      font-family: 'Inter', sans-serif;
      background-color: #fff;
      color: #1e293b;
    }
    .verified-badge {
      background-color: #7c3aed;
      color: white;
      font-size: 0.75rem;
      font-weight: 600;
      border-radius: 9999px;
      padding: 0.125rem 0.5rem;
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
    }
    .profile-card {
      border: 1px solid #e5e7eb;
      border-radius: 0.5rem;
      box-shadow: 0 1px 2px rgb(0 0 0 / 0.05);
      padding: 1.5rem;
      background-color: white;
    }
    .icon-circle {
      width: 36px;
      height: 36px;
      background-color: #f3f4f6;
      color: #6b7280;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out;
      text-decoration: none;
    }
    .icon-circle:hover {
      color: #374151;
      background-color: #e5e7eb;
      text-decoration: none;
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
    .btn-outline-secondary-custom i {
      font-size: 1rem;
    }
    .btn-outline-secondary-custom:hover,
    .btn-outline-secondary-custom:focus {
      box-shadow: 0 6px 12px rgba(124, 58, 237, 0.5);
      transform: translateY(-2px);
      outline: none;
      color: white;
      text-decoration: none;
    }
    .stats-number {
      color: #7c3aed;
      font-weight: 600;
      font-size: 1.125rem;
      margin-bottom: 0.25rem;
    }
    .text-xs {
      font-size: 0.75rem;
    }
    a, a:hover, a:focus {
      text-decoration: none;
    }
</style>