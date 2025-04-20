<template>
  <div class="d-flex flex-column min-vh-100 bg-light">
    <Header />
    <main class="flex-grow-1">
      <router-view/>
    </main>
    <Footer />
  </div>
  
</template>

<script setup lang="ts">
import Header from '@/components/Header.vue';
import Footer from './components/Footer.vue';
</script>

