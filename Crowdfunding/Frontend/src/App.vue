<template>
  <div class="d-flex flex-column min-vh-100 bg-light">
    <Header v-if="!$route.meta.hideHeader" />
    <main class="flex-grow-1">
      <router-view/>
    </main>
    <Footer />
  </div>
  
</template>

<script setup lang="ts">
import Header from '@/components/Header.vue';
import Footer from './components/Footer.vue';
import { useAuthStore } from '@/stores/auth';
const auth = useAuthStore();
if (auth.isAuthenticated && !auth.user) {
  auth.fetchUser();
}
</script>

