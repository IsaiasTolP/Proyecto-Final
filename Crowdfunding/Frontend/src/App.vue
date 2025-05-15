<template>
  <div class="d-flex flex-column min-vh-100 bg-light">
    <Header v-if="!$route.meta.hideHeader" />
    <main class="flex-grow-1">
      <div v-if="loading" class="d-flex justify-content-center align-items-center vh-100">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <router-view v-else/>
    </main>
    <Footer />
  </div>
  
</template>

<script setup lang="ts">
import Header from '@/components/Header.vue';
import Footer from './components/Footer.vue';
import { useAuthStore } from '@/stores/auth';
import { onBeforeMount, ref } from 'vue';
const auth = useAuthStore();
const loading = ref(true);

onBeforeMount(async () => {
  if (auth.isAuthenticated && !auth.user) {
    await auth.fetchUser();
    loading.value = false;
  }
})

</script>

