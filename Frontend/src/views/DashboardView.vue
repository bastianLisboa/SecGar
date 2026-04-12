<template>
  <main class="dashboard-page">
    <section class="dashboard-shell">
      <header class="dashboard-header">
        <div>
          <p class="eyebrow">Vista protegida de ejemplo</p>
          <h1>Dashboard</h1>
        </div>

        <RouterLink class="back-link" to="/">Volver al login</RouterLink>
      </header>

      <section class="dashboard-grid">
        <article class="panel">
          <h2>Que paso aqui</h2>
          <p>
            Entraste a la ruta <strong>/dashboard</strong>. Vue Router detecto la URL y cargo este
            componente desde <strong>src/views/DashboardView.vue</strong>.
          </p>
        </article>

        <article class="panel">
          <h2>Idea clave</h2>
          <p>
            La pagina no se recargo completa como en una navegacion clasica. Solo cambio la vista
            renderizada dentro de <strong>RouterView</strong>.
          </p>
        </article>
      </section>
    </section>
  </main>
</template>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  padding: 2rem;
}

.dashboard-shell {
  width: min(1100px, 100%);
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.eyebrow {
  color: var(--color-success);
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

h1 {
  font-size: clamp(2rem, 4vw, 3rem);
}

.back-link {
  padding: 0.8rem 1rem;
  border-radius: 999px;
  border: 1px solid var(--color-border);
  background: var(--color-surface);
  font-weight: 700;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
}

.panel {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 24px;
  box-shadow: var(--shadow-soft);
  padding: 1.5rem;
}

.panel h2 {
  margin-bottom: 0.75rem;
  font-size: 1.2rem;
}

.panel p {
  color: var(--color-text-soft);
}
</style>
