<template>
  <section class="history-section container d-flex flex-column flex-md-row align-items-center gap-4 gap-md-5 justify-content-center">
    <div class="image-container">
      <img
        src="../assets/images/Estatua-libertad.jpg"
        alt="Equipo de CrowdFundMe trabajando colaborativamente"
        width="600"
        height="400"
				class="rounded"
      />
    </div>
    <div class="text-start" style="max-width: 28rem;">
      <h2 class="mb-3 fs-3 text-dark">
        Nuestra Historia
      </h2>
      <p class="text-secondary mb-3">
        CrowdFundMe nace en 2025 con una misión clara: <strong>democratizar el acceso a la financiación</strong>. Lo que comenzó como una idea, pronto se convirtió en una plataforma que impulsa miles de sueños alrededor del mundo.
      </p>
      <p class="text-secondary">
        Hoy cualquiera puede financiar proyectos que transforman comunidades, impulsan la innovación y celebran la creatividad humana.
      </p>
    </div>
  </section>
</template>

<style scoped>
.history-section {
  padding: 2rem 1rem;
}
h2 {
  font-weight: 700;
}
.text-secondary strong {
  font-weight: 600;
}
@media (min-width: 768px) {
  h2 {
    font-size: 2rem;
  }
}
</style>
