

<template>
<body>
  <section class="py-5 text-center">
    <div class="container">
      <h2 class="fw-bold mb-2">Nuestro Impacto</h2>
      <p class="mb-5">Juntos, creamos un mundo donde las ideas cobran vida</p>
      <div class="row justify-content-center mb-5">
        <div class="col-8 col-sm-4 d-flex flex-column align-items-center">
          <div class="icon-circle">
            <i class="fas fa-users fa-lg"></i>
          </div>
          <div class="fw-bold fs-3">{{ projectStats?.users }}</div>
          <div>Usuarios</div>
        </div>
        <div class="col-8 col-sm-4 d-flex flex-column align-items-center">
          <div class="icon-circle">
            <i class="fas fa-gift fa-lg"></i>
          </div>
          <div class="fw-bold fs-3">{{ projectStats?.total_donated }} €</div>
          <div>En financiación otorgada</div>
        </div>
        <div class="col-8 col-sm-4 d-flex flex-column align-items-center">
          <div class="icon-circle">
            <i class="fas fa-award fa-lg"></i>
          </div>
          <div class="fw-bold fs-3">{{ projectStats?.completed_projects }}</div>
          <div v-if="projectStats?.completed_projects === 1">Proyecto Exitoso</div>
          <div v-else>Proyectos Exitosos</div>
        </div>
      </div>
      <button v-if="!auth.isAuthenticated" type="button" class="btn btn-purple" @click="router.push('/auth')">Únete a nuestra comunidad</button>
    </div>
  </section>
</body>
</template>

<script setup lang="ts">
import router from '@/router';
import { useAuthStore } from '@/stores/auth';
import { getProjectStats } from '@/services/sProject';
import { onBeforeMount, ref } from 'vue';
import type { ProjectStats } from '@/interfaces/Project';

const auth = useAuthStore();
const projectStats = ref<ProjectStats>()

onBeforeMount(async () => {
  projectStats.value = await getProjectStats();
})


</script>

<style scoped>
    body {
      background-color: #8b5cf6;
      color: white;
    }
    .icon-circle {
      background-color: rgba(167, 139, 250, 0.4);
      border-radius: 50%;
      padding: 1rem;
      display: inline-flex;
      justify-content: center;
      align-items: center;
      width: 3rem;
      height: 3rem;
      margin-bottom: 1rem;
    }
    .btn-purple {
      background-color: white;
      color: #8b5cf6;
      font-weight: 600;
      border-radius: 0.375rem;
      padding: 0.5rem 1.5rem;
      border: none;
    }
    .btn-purple:hover {
      background-color: #f3f4f6;
      color: #7c3aed;
    }
</style>