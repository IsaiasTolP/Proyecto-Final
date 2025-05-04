<template>
    <div>
      <section class="container py-5">
        <div v-if="loading" class="text-center">
          Cargando perfil...
        </div>
        <div v-else class="row align-items-center">
          <div v-if="messageStore.message" :class="['alert', alertClass, 'mt-3']">
            {{ messageStore.message }}
            <div class="progress mt-2" style="height: 5px;">
              <div
                class="progress-bar"
                role="progressbar"
                :style="{ width: `${progress}%` }"
                aria-valuenow="progress"
                aria-valuemin="0"
                aria-valuemax="100"
              ></div>
            </div>
          </div>

          <button class="btn btn-link text-success mb-3 go-back" @click="goBack">← Volver</button>
          <!-- Avatar -->
          <div class="col-md-4 text-center mb-4 mb-md-0">
            <img
              :src="typeof profile.pfp === 'string' ? profile.pfp : undefined"
              :alt="`Foto de perfil de ${profile.user?.username}`"
              class="rounded-circle img-fluid"
              style="width: 150px; height: 150px; object-fit: cover;"
            />
          </div>
  
          <!-- Datos de perfil -->
          <div class="col-md-8">
            <h1 class="mb-2">{{ profile.user?.username }}</h1>
            <p class="text-muted mb-1" v-if="profile.is_founder">Fundador</p>
            <p class="mb-3">{{ profile.bio || 'Este usuario no ha añadido una biografía.' }}</p>
            <p class="mb-3" v-if="profile.location"><strong>Ubicación:</strong> {{ profile.location }}</p>
            <div v-if="auth.user?.is_founder">
              <p class="mb-3"><strong>Sitio web: </strong><a :href="profile.website">{{ profile.website }}</a></p>
              <p class="mb-3"><strong>Email de contacto: </strong>{{ profile.contact_email }}</p>
              <div v-for="(url, key) in profile.social_media" :key="key">
                <p><a :href="url">{{ key }}</a></p>
              </div>
            </div>
  
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
  import { useMessageStore } from '@/stores/message';
  import type { FounderProfileData } from '@/interfaces/Account';
  
  const route = useRoute();
  const router = useRouter();
  const auth = useAuthStore();
  const messageStore = useMessageStore();
  
  
  const profile = ref<FounderProfileData>({} as FounderProfileData);
  const currentUser = auth.user;
  const loading = ref(true);
  const alertClass = computed(() => (messageStore.type === 'success' ? 'alert-success' : 'alert-danger'));
  const progress = ref(100);
  const timer = ref(null as any)
  
  const isOwner = computed(() => !!currentUser && currentUser.id === profile.value.user?.id);
  
  function goBack() {
    router.push({ name: 'Home' });
  }
  
  async function fetchProfile() {
    loading.value = true;
    try {
      const userId = route.params.id;
      const url = auth.user?.is_founder
        ? `/accounts/founders/user/${userId}/`
        : `/accounts/profiles/user/${userId}/`;
      const { data } = await api.get<FounderProfileData>(url);
      profile.value = data;
    } catch (err: any) {
      messageStore.setMessage('Error al cargar el perfil.', 'error');
    } finally {
      loading.value = false;
    }
  }

  function startTimer() {
    timer.value = setInterval(() => {
      if (progress.value > 0) {
        progress.value--;
      } else {
        clearInterval(timer.value);
        messageStore.clearMessage();
      }
    }, 50);
  }
  
  onMounted(async () => {
    await fetchProfile();
    if (messageStore.message) {
      startTimer();
    }
  });
</script>

<style scoped>
  .btn-link:hover {
    text-decoration: underline;
  }
  .progress-bar {
    transition: width 0.1s ease-in-out; 
    background-color: green;
  }
  .go-back {
    display: flex;
  }
</style>