<template>
    <footer class="bg-success text-white mt-5 py-4">
      <div class="container">
        <div class="row text-center text-md-start">
          <div class="col-md-4 mb-3">
            <h5>Sobre Nosotros</h5>
            <p>
              CrowdFundMe una plataforma de crowdfunding dedicada a impulsar proyectos innovadores y sociales.
            </p>
          </div>
          <div class="col-md-4 mb-3">
            <h5>Enlaces Útiles</h5>
            <ul class="list-unstyled">
              <li><router-link :to="{ name: 'Home' }" class="text-white text-decoration-none">Inicio</router-link></li>
              <li><a href="#" class="text-white text-decoration-none">Proyectos</a></li>
              <li><a href="#" class="text-white text-decoration-none">Contacto</a></li>
              <li><a href="#" class="text-white text-decoration-none">Política de Privacidad</a></li>
            </ul>
          </div>
          <div class="col-md-4 mb-3">
            <h5>Contacto</h5>
            <address>
              <strong>Email:</strong> <a href="mailto:info@crowdfund.com" class="text-white">info@crowdfundme.com</a><br />
              <strong>Tel:</strong> +34 600 123 456
            </address>
          </div>
        </div>
  
        <hr class="border-white opacity-50" />
  
        <div class="text-center">
          <p class="mb-0">&copy; {{ new Date().getFullYear() }} CrowdFundMe. Todos los derechos reservados.</p>
        </div>
      </div>
    </footer>
</template>

<style scoped>
  footer a:hover {
    text-decoration: underline;
  }
</style>