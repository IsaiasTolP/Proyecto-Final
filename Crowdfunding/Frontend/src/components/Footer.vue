<template>
<body>
  <footer class="footer-bg py-5">
    <div class="container">
      <div class="row gy-4 gy-md-0">
        <div class="col-md-3 d-flex flex-column">
          <div class="d-flex align-items-center mb-3">
            <div class="circle-cf me-2">CF</div>
            <span class="fw-semibold fs-5 text-white">CrowdFundMe</span>
          </div>
          <p class="mb-3" style="max-width: 220px; line-height: 1.4;">
            Impulsando a los creadores a realizar proyectos innovadores a través del apoyo de la comunidad.
          </p>
          <div class="social-icons d-flex">
            <a href="#" aria-label="Twitter"><i class="fab fa-twitter"></i></a>
            <a href="#" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
            <a href="#" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
          </div>
        </div>

        <div class="col-md-4 d-flex flex-wrap">
          <div class="me-5 mb-4">
            <h3 class="footer-title">Nosotros</h3>
            <nav class="nav flex-column">
              <router-link to="/story" class="nav-link px-0 py-1" href="#">Nuestra Historia</router-link>
              <a class="nav-link px-0 py-1" href="#">Blog</a>
            </nav>
          </div>

          <div class="me-5 mb-4">
            <h3 class="footer-title">Recursos</h3>
            <nav class="nav flex-column">
              <router-link class="nav-link px-0 py-1" to="/contact">Contacta</router-link>
              <a class="nav-link px-0 py-1" href="#">Manual del Creador</a>
            </nav>
          </div>

          
        </div>

        <div class="col-md-5 d-flex flex-wrap">
          <div class="mb-4" style="min-width: 250px;">
            <h3 class="footer-title">Subscribirse</h3>
            <p class="mb-2" style="line-height: 1.4;">
              Recibe las últimas noticias y actualizaciones en tu bandeja de entrada.
            </p>
            <form class="d-flex" role="form" novalidate>
              <input
                type="email"
                class="form-control input-subscribe"
                placeholder="Tu correo electrónico"
                aria-label="Tu correo electrónico"
                required
              />
              <button type="submit" class="btn btn-subscribe">
                Subscribe
              </button>
            </form>
          </div>
        </div>
      </div>

      <div class="footer-border mt-5 pt-3 d-flex flex-column flex-sm-row justify-content-between align-items-center text-secondary small">
        <div>© 2025 CrowdFundMe. Todos los derechos reservados.</div>
        <div class="mt-3 mt-sm-0">
          <router-link to="/terms" class="me-4">Términos de Servicio</router-link>
          <router-link to="/privacy" class="me-4">Política de Privacidad</router-link>
        </div>
      </div>
    </div>
  </footer>
</body>
</template>

<style scoped>
  body {
      font-family: 'Inter', sans-serif;
      background-color: #0D1126;
      color: #A3AED0;
    }
    a {
      color: #A3AED0;
      text-decoration: none;
    }
    a:hover {
      color: #fff;
      text-decoration: none;
    }
    .footer-bg {
      background-color: #0D1126;
    }
    .footer-border {
      border-top: 1px solid #1E2139;
    }
    .btn-subscribe {
      background-color: #7C4DFF;
      color: white;
      border-radius: 0 0.375rem 0.375rem 0;
      border: none;
      transition: background-color 0.2s ease;
    }
    .btn-subscribe:hover {
      background-color: #6939e0;
      color: white;
    }
    .input-subscribe {
      background-color: #1E2139;
      border: none;
      color: #A3AED0;
      border-radius: 0.375rem 0 0 0.375rem;
    }
    .input-subscribe::placeholder {
      color: #6B7280;
    }
    .input-subscribe:focus {
      box-shadow: none;
      background-color: #1E2139;
      color: #A3AED0;
    }
    .circle-cf {
      width: 2rem;
      height: 2rem;
      background-color: #7C4DFF;
      border-radius: 50%;
      color: white;
      font-weight: 700;
      font-size: 0.875rem;
      display: flex;
      align-items: center;
      justify-content: center;
      user-select: none;
    }
    .footer-title {
      color: white;
      font-weight: 600;
      margin-bottom: 1rem;
    }
    .social-icons a {
      font-size: 1.25rem;
      margin-right: 1.5rem;
      color: #A3AED0;
      transition: color 0.2s ease;
    }
    .social-icons a:last-child {
      margin-right: 0;
    }
    .social-icons a:hover {
      color: white;
    }
</style>