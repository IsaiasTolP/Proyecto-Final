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