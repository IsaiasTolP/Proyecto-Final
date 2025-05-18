<template>
<body>
  <section class="container py-5 text-center">
    <h2 class="fw-bold mb-2 fs-4 fs-sm-5 fs-md-3 text-dark">Funcionamiento de CrowdFundMe</h2>
    <p class="text-secondary mb-4 fs-6">
      De la idea a la financiación, descubre cómo funciona nuestra plataforma
    </p>
    <div class="row justify-content-center g-4 mb-4 align-items-stretch">
      <div class="col-12 col-sm-6 col-md-4">
        <div class="card-custom bg-white">
          <div class="icon-circle mx-auto">
            <i class="fas fa-lightbulb"></i>
          </div>
          <h3 class="fw-semibold mb-2 fs-6 text-dark">Crea tu proyecto</h3>
          <p class="text-secondary fs-7 mx-auto" style="max-width: 220px;">
            Envía tu idea con detalles y objetivos claves, puedes incluir recompensas para tus backers.
          </p>
        </div>
      </div>
      <div class="col-12 col-sm-6 col-md-4">
        <div class="card-custom bg-white">
          <div class="icon-circle mx-auto">
            <i class="fas fa-user-friends"></i>
          </div>
          <h3 class="fw-semibold mb-2 fs-6 text-dark">Recibe financiación</h3>
          <p class="text-secondary fs-7 mx-auto" style="max-width: 220px;">
            Comparte tu proyecto y conecta con nuestra comunidad de backers.
          </p>
        </div>
      </div>
      <div class="col-12 col-sm-6 col-md-4">
        <div class="card-custom bg-white">
          <div class="icon-circle mx-auto">
            <i class="fas fa-check-circle"></i>
          </div>
          <h3 class="fw-semibold mb-2 fs-6 text-dark">Hazlo real</h3>
          <p class="text-secondary fs-7 mx-auto" style="max-width: 220px;">
						Usa los fondos para convertir tu visión en realidad y recompensa a tus backers.
          </p>
        </div>
      </div>
    </div>
    <button v-if="auth.user?.is_founder" type="button" class="btn btn-purple">
      Comienza con tu proyecto ahora mismo
    </button>
  </section>
</body>
</template>

<script setup lang="ts">
  import { useAuthStore } from '@/stores/auth';

  const auth = useAuthStore();
</script>

<style scoped>
body {
      background-color: #f9fafc;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI";
    }
    .icon-circle {
      background-color: #ddd6fe;
      color: #7c3aed;
      width: 48px;
      height: 48px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 1rem;
      font-size: 1.25rem;
    }
    .card-custom {
      border-radius: 0.5rem;
      box-shadow: 0 1px 3px rgb(0 0 0 / 0.1);
      border: none;
      text-align: center;
      padding: 1.5rem;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
    .btn-purple {
      background-color: #7c3aed;
      color: white;
      font-weight: 600;
      font-size: 0.875rem;
      padding: 0.625rem 1.25rem;
      border-radius: 0.375rem;
      border: none;
    }
    .btn-purple:hover,
    .btn-purple:focus {
      background-color: #6b21a8;
      color: white;
    }
</style>