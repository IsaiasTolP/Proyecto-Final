<template>
  <button class="btn btn-outline-secondary-custom mb-4" @click="goBack">
    ← Volver
  </button>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

	const router = useRouter();

	function goBack() {
    router.back();
  }

</script>

<style scoped>
.btn-outline-secondary-custom {
  background: linear-gradient(90deg, #7c3aed, #a78bfa);
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
  padding: 0.5rem 1.25rem;
  border-radius: 0.5rem;
  border: none;
  box-shadow: 0 4px 8px rgba(124, 58, 237, 0.3);
  transition: all 0.2s ease;
  text-decoration: none;
}

.btn-outline-secondary-custom:hover {
  box-shadow: 0 6px 12px rgba(124, 58, 237, 0.5);
  transform: translateY(-2px);
}

</style>