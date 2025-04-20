<template>
    <nav class="navbar navbar-expand-md bg-success navbar-dark px-5" role="navigation" aria-label="Main navigation">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">CrowdFundMe</a>
        <button
          class="navbar-toggler"
          type="button"
          @click="toggleNavbar"
          :aria-expanded="isCollapsed"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div :class="['collapse', 'navbar-collapse', { show: isCollapsed }]" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="#">Inicio</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Acerca de</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Servicios</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Contacto</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  
<script setup lang="ts">
  import { ref } from 'vue';
  
  const isCollapsed = ref(false);
  
  function toggleNavbar() {
    isCollapsed.value = !isCollapsed.value;
  }

  </script>
  
  <style scoped>
  .navbar-brand {
    font-weight: bold;
    color: #ffffff;
  }
  
  .nav-link {
    color: #ffffff;
  }
  
  .nav-link:hover,
  .nav-link:focus {
    color: #cce5cc;
  }
</style>