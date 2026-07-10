<template>
  <div class="hero-wrapper">
    <div class="ambient"></div>
    
    <header>
      <Navbar />
    </header>
    
    <main class="hero">
      
      <section class="hero-left">
        
        <div class="search-top-wrapper">
          <BaseResearchInput placeholder="Rechercher un modèle..." />
        </div>
        
        <h1>
          Téléchargez.<br>
          Personnalisez.<br>
          Signez. <span class="accent">En toute<br>confiance.</span>
        </h1>
        
        <p class="subtitle">
          Des milliers de modèles juridiques rédigés par des juristes et conformes aux législations africaines.
        </p>
        
        <div class="cta-row">
          <NuxtLink to="/contractBank" class="btn-primary">
            Télécharger un document
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
          </NuxtLink>
        </div>
        
      </section>
      
      <section class="illustration">
        <div class="glow-ring"></div>
        
        <svg class="connectors" viewBox="0 0 640 560" preserveAspectRatio="none">
          <path d="M120 90 C 190 90, 210 130, 250 150"/>
          <circle cx="120" cy="90" r="3"/>
          <path d="M100 260 C 170 250, 190 230, 230 220"/>
          <circle cx="100" cy="260" r="3"/>
          <path d="M540 90 C 470 90, 450 130, 400 150"/>
          <circle cx="540" cy="90" r="3"/>
          <path d="M560 265 C 490 255, 460 235, 415 225"/>
          <circle cx="560" cy="265" r="3"/>
        </svg>
        
        <div class="chip chip-secure">
          <div class="chip-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V7a4 4 0 018 0v4"/></svg>
          </div>
          <div>
            <div class="chip-title">Sécurisé</div>
            <div class="chip-sub">Vos données<br>sont protégées</div>
          </div>
        </div>
        
        <div class="chip chip-compliant">
          <div class="chip-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 12l2 2 4-4"/><circle cx="12" cy="12" r="9"/></svg>
          </div>
          <div>
            <div class="chip-title">Conforme</div>
            <div class="chip-sub">Aux législations<br>africaines</div>
          </div>
        </div>
        
        <div class="chip chip-validated">
          <div class="chip-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3v14M7 8l5-5 5 5M5 21h14"/></svg>
          </div>
          <div class="chip-title">Validé par des<br>juristes</div>
        </div>
        
        <div class="chip chip-instant">
          <div class="chip-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3v12M6 11l6 6 6-6M5 21h14"/></svg>
          </div>
          <div class="chip-title">Téléchargement<br>instantané</div>
        </div>
        
        <div class="stack">
          <div class="document">
            <div class="doc-badge">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M5 13l4 4L19 7"/></svg>
              CONFORME
            </div>
            <div class="doc-title">CONTRAT DE PRESTATION<br>DE SERVICES</div>
            <div class="doc-lines">
              <span></span><span></span><span></span><span></span>
            </div>
          </div>
        </div>
      </section>
      
    </main>
    <Caroussel />
  </div>
</template>

<script lang="ts">
import Navbar from '../components/navigation/navbar.vue'
import Caroussel from '../components/carousselCountries.vue'
import BaseResearchInput from '../components/input/BaseResearchInput.vue';

export default {
  name: 'HeroChap',
  components: {
    Navbar,
    Caroussel,
    BaseResearchInput
  },
  setup() {
    const handleStepClick = (step: string) => {
      console.log(`Ouverture de la sélection pour l'étape : ${step}`)
    }

    return {
      handleStepClick
    }
  }
}
</script>

<style scoped>
.hero-wrapper {
  --bg: #07100d;
  --bg-glow: #0a1a14;
  --panel: #0e1613;
  --panel-2: #111c18;
  --border: rgba(255,255,255,.08);
  --border-green: rgba(43,235,132,.28);
  --green: #28e881;
  --green-soft: #8bffc2;
  --green-dim: rgba(40,232,129,.12);
  --text: #f4f7f5;
  --text-muted: #94a39c;
  --text-faint: #576259;
  --radius: 16px;
  --font-display: 'Manrope', sans-serif;
  --font-body: 'Inter', sans-serif;

  background: var(--bg);
  color: var(--text);
  font-family: var(--font-body);
  min-height: 100vh;
  overflow-x: hidden;
  background-image: radial-gradient(circle at 1px 1px, rgba(255,255,255,.045) 1px, transparent 1px);
  background-size: 26px 26px;
  position: relative;
}

.hero-wrapper * {
  box-sizing: border-box;
}

a { color: inherit; text-decoration: none; }
button { font-family: inherit; cursor: pointer; border: none; }

/* ---------- Ambient glow ---------- */
.ambient {
  position: absolute;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  background:
    radial-gradient(ellipse 900px 500px at 62% 40%, rgba(40,232,129,.14), transparent 60%),
    radial-gradient(ellipse 600px 400px at 15% 15%, rgba(40,232,129,.06), transparent 60%);
}

/* ---------- Header ---------- */
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  width: 100%;
  margin: 0 auto;
  position: relative;
  z-index: 10;
}
.logo { display: flex; align-items: center; gap: 10px; }
.logo-mark {
  width: 34px; height: 34px; border-radius: 50%;
  background: linear-gradient(145deg, var(--green-soft), var(--green));
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-display); font-weight: 800; color: #04150c;
  font-size: 18px;
  box-shadow: 0 0 18px rgba(40,232,129,.45);
}
.logo-text { display: flex; flex-direction: column; line-height: 1.05; }
.logo-text .name { font-family: var(--font-display); font-weight: 800; font-size: 19px; letter-spacing: -.2px; }
.logo-text .tagline { font-size: 8.5px; color: var(--text-faint); letter-spacing: .6px; font-weight: 600; margin-top: 3px; }

nav.links { display: flex; align-items: center; gap: 34px; }
nav.links a {
  display: flex; align-items: center; gap: 5px;
  font-size: 14.5px; color: #cfd8d3; font-weight: 500;
  transition: color .15s ease;
}
nav.links a:hover { color: var(--text); }
nav.links svg { width: 12px; height: 12px; opacity: .6; }

.nav-actions { display: flex; align-items: center; gap: 18px; }
.icon-btn {
  width: 38px; height: 38px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  background: var(--panel); border: 1px solid var(--border);
  color: var(--text-muted);
  transition: border-color .15s ease, color .15s ease;
}
.icon-btn:hover { border-color: var(--border-green); color: var(--green-soft); }
.lang-select {
  display: flex; align-items: center; gap: 6px;
  font-size: 14px; color: #cfd8d3; font-weight: 500;
  padding: 8px 6px;
}
.lang-select svg:last-child { width: 10px; height: 10px; opacity: .6; }
.signin { font-size: 14.5px; color: #cfd8d3; font-weight: 500; white-space: nowrap; }
.signin:hover { color: var(--text); }
.cta-btn {
  background: linear-gradient(180deg, var(--green-soft), var(--green));
  color: #052c17;
  font-weight: 700;
  font-size: 14.5px;
  padding: 11px 22px;
  border-radius: 999px;
  white-space: nowrap;
  box-shadow: 0 4px 20px rgba(40,232,129,.28);
  transition: transform .15s ease, box-shadow .15s ease;
}
.cta-btn:hover { transform: translateY(-1px); box-shadow: 0 6px 26px rgba(40,232,129,.4); }

/* ---------- Hero layout ---------- */
.hero {
  max-width: 1440px;
  margin: 0 auto;
  padding: 70px 48px;
  display: flex;
  align-items: center;
  justify-content: space-between; 
  gap: 40px; 
  position: relative;
  z-index: 2;
}

/* ---------- Left column ---------- */
.hero-left {
  flex: 0 0 auto;
  padding: 10px 10px;
  max-width: 500px;
}

/* ── RECHERCHE AU-DESSUS DU TEXTE ── */
.search-top-wrapper {
  margin-bottom: 2rem;
  width: 100%;
}

/* Forcer les dimensions pour correspondre au bouton */
.search-top-wrapper :deep(input),
.search-top-wrapper :deep(.search-container) {
  height: 50px; /* La même hauteur que le bouton principal */
  border-radius: 50px;
  padding: 25px 16px;
  font-size: 15px;
  width: 100%;
  max-width: 320px; /* Largeur d'un bouton moyen */
  background: var(--panel-2);
  border: 1px solid var(--border);
  color: var(--text);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.search-top-wrapper :deep(input:focus) {
  outline: none;
  border-color: var(--green);
  box-shadow: 0 0 0 3px var(--green-dim);
}

.search-top-wrapper :deep(input::placeholder) {
  color: var(--text-muted);
}

h1 {
  font-family: var(--font-display);
  font-weight: 800;
  font-size: 52px;
  line-height: 1.05;
  letter-spacing: -1.5px;
  color: var(--text);
  margin-bottom: 22px;
}
h1 .accent { color: var(--green); }

.subtitle {
  font-size: 16px;
  line-height: 1.6;
  color: var(--text-muted);
  max-width: 420px;
  margin-bottom: 32px;
}

.cta-row { display: flex; align-items: center; gap: 14px; margin-bottom: 44px; flex-wrap: wrap; }
.btn-primary {
  display: inline-flex; align-items: center; gap: 9px;
  background: linear-gradient(180deg, var(--primary-color));
  color: #FFFFFF; font-weight: 700; font-size: 15px;
  padding: 14px 24px; border-radius: 50px;
  box-shadow: 0 6px 24px rgba(40,232,129,.28);
  transition: transform .15s ease;
}
.btn-primary:hover { transform: translateY(-2px); }
.btn-primary svg { width: 16px; height: 16px; }

/* ---------- Right column (Illustration) ---------- */
.illustration {
  position: relative;
  flex: 0 0 auto;
  margin-left: auto; 
  width: 100%;
  max-width: 600px;
  height: 560px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.glow-ring {
  position: absolute;
  bottom: 60px;
  width: 280px; height: 56px;
  background: radial-gradient(ellipse, rgba(40,232,129,.55), rgba(40,232,129,.05) 70%);
  border-radius: 50%;
  filter: blur(6px);
}
.glow-ring::after {
  content: '';
  position: absolute; inset: 0;
  border-radius: 50%;
  border: 1px solid rgba(40,232,129,.4);
  box-shadow: 0 0 40px rgba(40,232,129,.5);
}

.connectors { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }
.connectors path { fill: none; stroke: rgba(120,150,138,.45); stroke-width: 1.2; }
.connectors circle { fill: var(--green); }

.chip {
  position: absolute;
  display: flex; align-items: center; gap: 10px;
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 13px;
  padding: 11px 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,.35);
  z-index: 3;
}
.chip .chip-icon {
  width: 30px; height: 30px; border-radius: 9px;
  background: var(--green-dim);
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.chip .chip-icon svg { width: 15px; height: 15px; color: var(--green); }
.chip .chip-title { font-size: 13px; font-weight: 700; color: var(--text); }
.chip .chip-sub { font-size: 11.5px; color: var(--text-muted); margin-top: 1px; }

/* Positions ajustées pour le nouveau layout */
.chip-secure { top: 60px; left: 0px; } 
.chip-compliant { top: 220px; left: -20px; }
.chip-validated { top: 60px; right: 20px; }
.chip-instant { top: 230px; right: 0px; }

.stack {
  position: relative;
  margin-bottom: 150px;
  width: 280px;
  display: flex; flex-direction: column; align-items: center;
}

.document {
  position: relative;
  bottom: 0px;
  width: 220px;
  background: linear-gradient(160deg,#101a16,#0a1310);
  border: 1px solid rgba(255,255,255,.09);
  border-top: 2px solid var(--green);
  border-radius: 14px;
  padding: 16px 16px 18px;
  box-shadow: 0 26px 50px rgba(0,0,0,.55);
  transform: rotate(-1.5deg);
  z-index: 2;
}
.doc-badge {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 9px; font-weight: 700; letter-spacing: .5px;
  color: var(--green-soft);
  background: var(--green-dim);
  border-radius: 999px;
  padding: 3px 9px;
  margin-bottom: 10px;
}
.doc-badge svg { width: 9px; height: 9px; }
.doc-title { font-family: var(--font-display); font-weight: 800; font-size: 13px; line-height: 1.35; color: var(--text); margin-bottom: 14px; }
.doc-lines { display: flex; flex-direction: column; gap: 7px; }
.doc-lines span { height: 5px; border-radius: 3px; background: rgba(255,255,255,.09); }
.doc-lines span:nth-child(1) { width: 100%; }
.doc-lines span:nth-child(2) { width: 88%; }
.doc-lines span:nth-child(3) { width: 94%; }
.doc-lines span:nth-child(4) { width: 70%; }

/* ---------- Responsive ---------- */
@media (max-width: 1180px) {
  .hero { 
    flex-direction: column; 
    align-items: center;
    text-align: center;
    padding: 80px 24px;
  }
  .hero-left {
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .search-top-wrapper :deep(input),
  .search-top-wrapper :deep(.search-container) {
    margin: 0 auto; /* Pour centrer la barre de recherche sur mobile/tablette */
  }
  .cta-row {
    justify-content: center;
  }
  .illustration { 
    height: 480px; 
    margin: 0 auto; 
  }
  nav.links { display: none; }
}

@media (max-width: 640px) {
  header { padding: 18px 20px; }
  .hero { padding: 24px 20px 60px; }
  h1 { font-size: 38px; letter-spacing: -1px; }
  .lang-select, .signin { display: none; }
  .chip .chip-sub { display: none; }
  .chip { padding: 9px 12px; }
  
  .chip-secure { top: 60px; left: -20px; }
  .chip-compliant { top: 220px; left: -30px; }
  .chip-validated { top: 60px; right: -10px; }
  .chip-instant { top: 230px; right: -30px; }
}
</style>