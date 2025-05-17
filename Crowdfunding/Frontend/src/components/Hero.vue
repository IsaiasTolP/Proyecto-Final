<template>
	<body>
		<main class="container d-flex flex-column flex-md-row align-items-center gap-4 gap-md-5 justify-content-center">
    <section class="text-start" style="max-width: 28rem;">
      <h1 class="mb-3 fs-2 fs-md-1 text-dark">
        Financia Tus Sueños,<br />
        <span class="highlight-purple">Cambia el Mundo</span>
      </h1>
      <p class="text-secondary mb-4">
				Apoya ideas innovadoras, proyectos creativos y causas significativas.<br />
				Únete a nuestra comunidad de patrocinadores que están marcando la diferencia.
      </p>
      <div class="d-flex gap-3">
        <button type="button" class="btn btn-purple" @click="router.push('/project/create')">
					Comienza un Proyecto
        </button>
        <button type="button" class="btn btn-outline-dark" @click="router.push('/projects')">
          Explorar Proyectos
        </button>
      </div>
    </section>
    <section class="image-container">
      <img
        src="https://storage.googleapis.com/a1aa/image/e396d4c8-a94f-4f44-b2f8-08de2572fa92.jpg"
        alt="Top view of a wooden table with multiple laptops, headphones, notebooks, coffee cups, and gadgets arranged, with hands typing on laptops"
        width="600"
        height="400"
      />
      <div class="info-box">
        <span class="highlight-purple">+2.500</span> proyectos exitosos <strong>financiados solo este año</strong>
      </div>
    </section>
  </main>
	</body>
    
</template>

<script setup lang="ts">
import router from '@/router';

</script>

<style scoped>
    body {
      font-family: 'Inter', sans-serif;
      background: linear-gradient(135deg, #ffffff 0%, #f3e8ff 100%);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
    }
    h1 {
      font-weight: 800;
      line-height: 1.1;
    }
    .highlight-purple {
      color: #7c3aed;
    }
    .btn-purple {
      background-color: #7c3aed;
      color: white;
      font-weight: 600;
      border-radius: 0.375rem;
      padding: 0.75rem 1.5rem;
      border: none;
    }
    .btn-purple:hover,
    .btn-purple:focus {
      background-color: #6d28d9;
      color: white;
    }
    .btn-outline-dark {
      font-weight: 600;
      border-radius: 0.375rem;
      padding: 0.75rem 1.5rem;
    }
    .info-box {
      position: absolute;
      bottom: 1.5rem;
      right: 1.5rem;
      background: white;
      border-radius: 0.5rem;
      box-shadow: 0 0.25rem 0.5rem rgb(0 0 0 / 0.1);
      padding: 0.75rem 1.25rem;
      max-width: 18rem;
      font-size: 0.875rem;
      color: #1e293b;
      font-weight: 400;
    }
    .info-box .highlight-purple {
      font-weight: 700;
    }
    .info-box strong {
      font-weight: 700;
    }
    .image-container {
      position: relative;
      border-radius: 1rem;
      overflow: hidden;
      box-shadow: 0 0.5rem 1rem rgb(0 0 0 / 0.1);
      max-width: 600px;
      width: 100%;
    }
    .image-container img {
      border-radius: 1rem;
      width: 100%;
      height: auto;
      object-fit: cover;
      display: block;
    }
    @media (min-width: 768px) {
      h1 {
        font-size: 3rem;
      }
      p {
        font-size: 1.125rem;
      }
    }
</style>