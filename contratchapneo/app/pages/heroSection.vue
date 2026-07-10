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
            Téléchargez facilement
            <span class="accent">tous vos contrats.</span>
          </h1>
        <p class="subtitle">
          Des milliers de modèles juridiques rédigés par des juristes et conformes aux législations africaines.
        </p>
        
        <div class="cta-row">
          <NuxtLink to="/contractBank" class="btn-primary">
            Télécharger un document
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
          </NuxtLink>
          <NuxtLink to="/etudeContrat" class="btn-secondary">
            Réviser un contrat
          </NuxtLink>
        </div>
      </section>
      
      <section class="illustration perspective-container">
        <div class="glow-ring"></div>
        
        <div class="floating-legal-icon icon-scale">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 3v18"/><path d="M3 7h18"/><path d="M6 7v6c0 1.6 1.4 3 3 3s3-1.4 3-3V7"/><path d="M15 7v6c0 1.6 1.4 3 3 3s3-1.4 3-3V7"/><path d="M9 21h6"/>
          </svg>
        </div>
        <div class="floating-legal-icon icon-shield">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
          </svg>
        </div>
        <div class="floating-legal-icon icon-briefcase">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
          </svg>
        </div>

        <div class="contract-3d">
          <div class="contract-shadow"></div>
          
          <div class="contract-paper glass-effect-3d">
            
            <div class="contract-header">
              <div class="fake-lines">
                <span></span><span></span>
              </div>
            </div>

            <h3 class="contract-title">Que souhaitez-vous faire ?</h3>

            <div class="contract-actions">
              
              <NuxtLink to="/contractBank" class="action-btn">
                <div class="action-icon bg-green">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="16" y1="13" x2="8" y2="13"></line>
                    <line x1="16" y1="17" x2="8" y2="17"></line>
                    <polyline points="10 9 9 9 8 9"></polyline>
                  </svg>
                </div>
                <div class="action-text">
                  <strong>Banque de contrats</strong>
                  <span>Modèles OHADA prêts à l'emploi</span>
                </div>
              </NuxtLink>

              <NuxtLink to="/lawCalcul" class="action-btn">
                <div class="action-icon bg-blue">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect>
                    <line x1="8" y1="6" x2="16" y2="6"></line>
                    <line x1="8" y1="10" x2="8.01" y2="10"></line>
                    <line x1="12" y1="10" x2="12.01" y2="10"></line>
                    <line x1="16" y1="10" x2="16.01" y2="10"></line>
                    <line x1="8" y1="14" x2="8.01" y2="14"></line>
                    <line x1="12" y1="14" x2="12.01" y2="14"></line>
                    <line x1="16" y1="14" x2="16.01" y2="14"></line>
                  </svg>
                </div>
                <div class="action-text">
                  <strong>Outils de calcul</strong>
                  <span>Simulez vos frais et droits</span>
                </div>
              </NuxtLink>

              <NuxtLink to="/pro" class="action-btn">
                <div class="action-icon bg-purple">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                  </svg>
                </div>
                <div class="action-text">
                  <strong>Nos Experts</strong>
                  <span>Trouvez un avocat ou notaire</span>
                </div>
              </NuxtLink>

              <NuxtLink to="/services" class="action-btn">
                <div class="action-icon bg-orange">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                  </svg>
                </div>
                <div class="action-text">
                  <strong>Services juridiques</strong>
                  <span>Accompagnement sur-mesure</span>
                </div>
              </NuxtLink>

            </div>
            
            <div class="contract-footer">
              <div class="signature-line"></div>
              <div class="signature-line"></div>
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
    return {}
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

/* ---------- Hero layout ---------- */
.hero {
  width: 100%;
  margin: 0 auto;
  padding: 60px 48px;
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
  width: 100%;
}

/* ── RECHERCHE AU-DESSUS DU TEXTE ── */
.search-top-wrapper {
  margin-bottom: 3.5rem;
  width: 100%;
}

.search-top-wrapper :deep(input),
.search-top-wrapper :deep(.search-container) {
  height: 50px; 
  border-radius: 50px;
  padding: 25px 16px;
  font-size: 15px;
  width: 100%;
  /* 👈 Augmenté pour correspondre à la largeur de deux boutons avec gap */
  max-width: 450px; 
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

/* ── DÉGRADÉ SUR LE TEXTE ── */
h1 .accent { 
  background: linear-gradient(135deg, var(--green-soft) 0%, var(--green) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.subtitle {
  font-size: 16px;
  line-height: 1.6;
  color: var(--text-muted);
  max-width: 420px;
  margin-bottom: 32px;
}

/* ── CONTENEUR BOUTONS SYMÉTRIQUES ── */
.cta-row { 
  display: flex; 
  align-items: center; 
  gap: 14px; 
  margin-bottom: 44px; 
  flex-wrap: wrap; 
  width: 100%;
  max-width: 450px; /* Aligné sur la largeur de la recherche */
}

.btn-primary, .btn-secondary {
  flex: 1; /* Chaque bouton prend exactement la moitié de l'espace */
  display: inline-flex; 
  align-items: center; 
  justify-content: center;
  gap: 9px;
  font-weight: 700; 
  font-size: 14.5px;
  padding: 14px 10px; 
  border-radius: 50px;
  transition: all .2s ease;
  white-space: nowrap;
}

.btn-primary {
  background: linear-gradient(180deg, var(--green-soft), var(--green));
  color: #052c17; 
  box-shadow: 0 6px 24px rgba(40,232,129,.28);
}
.btn-primary:hover { 
  transform: translateY(-2px); 
  box-shadow: 0 8px 30px rgba(40,232,129,.4);
}

.btn-secondary {
  background: transparent; 
  color: var(--text); 
  border: 1px solid var(--border);
}
.btn-secondary:hover { 
  border-color: var(--green); 
  background: rgba(255,255,255,.02); 
  transform: translateY(-2px);
}

.btn-primary svg { width: 16px; height: 16px; }

/* =========================================
   ILLUSTRATION 3D (Contrat + Icônes)
   ========================================= */
.perspective-container {
  position: relative;
  flex: 0 0 auto;
  margin-left: auto; 
  width: 100%;
  max-width: 500px; 
  height: 540px;
  display: flex;
  align-items: center;
  justify-content: center;
  perspective: 1400px; 
  pointer-events: none; 
}

.glow-ring {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 320px; height: 320px;
  background: radial-gradient(circle, rgba(40,232,129,.15) 0%, transparent 60%);
  border-radius: 50%;
  filter: blur(20px);
  z-index: 0;
  pointer-events: none; 
}

/* ── ICÔNES FLOTTANTES AUTOUR DU CONTRAT ── */
.floating-legal-icon {
  position: absolute;
  width: 45px; height: 45px;
  border-radius: 12px;
  background: rgba(14, 22, 19, 0.6);
  border: 1px solid rgba(40, 232, 129, 0.2);
  backdrop-filter: blur(8px);
  display: flex; align-items: center; justify-content: center;
  color: var(--green-soft);
  z-index: 5;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
  animation: float-icon 5s ease-in-out infinite;
}
.floating-legal-icon svg { width: 22px; height: 22px; }

.icon-scale { top: 12%; left: -10px; animation-delay: 0s; }
.icon-shield { top: 40%; right: -25px; animation-delay: 1.5s; }
.icon-briefcase { bottom: 18%; left: -25px; animation-delay: 3s; }

@keyframes float-icon {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(-15px) rotate(4deg); }
}

/* Le conteneur du contrat qui subit la rotation */
.contract-3d {
  position: relative;
  width: 350px; 
  transform-style: preserve-3d;
  transform: rotateY(-18deg) rotateX(12deg) translateZ(0);
  transition: transform 0.6s cubic-bezier(0.2, 0.8, 0.2, 1);
  z-index: 10;
  pointer-events: auto; 
}

.contract-3d:hover {
  transform: rotateY(-4deg) rotateX(4deg) translateZ(10px);
}

.contract-shadow {
  position: absolute;
  top: 10%; left: -5%; width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.4);
  border-radius: 20px;
  filter: blur(25px);
  transform: translateZ(-50px);
  transition: transform 0.6s, filter 0.6s;
  pointer-events: none; 
}

.contract-3d:hover .contract-shadow {
  transform: translateZ(-60px) scale(0.95);
  filter: blur(35px);
}

.contract-paper {
  background: linear-gradient(145deg, var(--panel), #14201c);
  margin-bottom: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 20px;
  padding: 2rem; 
  box-shadow: 
    inset 0 0 0 1px rgba(255, 255, 255, 0.05),
    0 20px 40px rgba(0, 0, 0, 0.4);
}

/* En-tête du contrat */
.contract-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 1.5rem; border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding-bottom: 0.8rem;
}
.doc-badge {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 9px; font-weight: 800; letter-spacing: 1px; color: var(--green-soft);
  background: var(--green-dim); border-radius: 999px; padding: 5px 10px;
}
.doc-badge svg { width: 11px; height: 11px; }

.fake-lines { display: flex; flex-direction: column; gap: 4px; align-items: flex-end; }
.fake-lines span { height: 4px; border-radius: 2px; background: rgba(255, 255, 255, 0.1); }
.fake-lines span:first-child { width: 35px; }
.fake-lines span:last-child { width: 20px; }

.contract-title {
  font-family: var(--font-display); font-size: 16px; color: var(--text);
  margin-bottom: 1.2rem; text-align: center; font-weight: 700;
}

/* Boutons à l'intérieur du contrat */
.contract-actions { display: flex; flex-direction: column; gap: 10px; }
.action-btn {
  position: relative; z-index: 50; display: flex; align-items: center; gap: 12px;
  padding: 10px 14px; background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px;
  text-decoration: none; transition: transform 0.2s ease, background 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.08); border-color: rgba(40,232,129,.3);
  transform: translateY(-3px) scale(1.02); box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
}

.action-icon {
  width: 34px; height: 34px; border-radius: 8px;
  display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.action-icon svg { width: 16px; height: 16px; color: #fff; }

.bg-green { background: linear-gradient(135deg, #10b981, #059669); }
.bg-blue { background: linear-gradient(135deg, #3b82f6, #2563eb); }
.bg-purple { background: linear-gradient(135deg, #8b5cf6, #7c3aed); }
.bg-orange { background: linear-gradient(135deg, #f59e0b, #ea580c); }

.action-text { display: flex; flex-direction: column; gap: 1px; }
.action-text strong { font-size: 13px; font-weight: 700; color: var(--text); }
.action-text span { font-size: 11px; color: var(--text-muted); }

.contract-footer {
  margin-top: 1.5rem; display: flex; justify-content: space-between;
  padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.05);
}
.signature-line {
  height: 2px; width: 50px; background: rgba(255, 255, 255, 0.2); border-radius: 2px;
}

/* ---------- Responsive ---------- */
@media (max-width: 1180px) {
  .hero { flex-direction: column; align-items: center; text-align: center; padding: 80px 24px; }
  .hero-left { margin: 0 auto; display: flex; flex-direction: column; align-items: center; }
  .search-top-wrapper :deep(input), .search-top-wrapper :deep(.search-container) { margin: 0 auto; }
  .cta-row { justify-content: center; }
  .perspective-container { height: auto; margin: 40px auto; }
  .contract-3d { transform: rotateY(0deg) rotateX(0deg) translateZ(0); }
  .contract-3d:hover { transform: scale(1.02); }
  .floating-legal-icon { display: none; /* Cache les icônes sur tablette/mobile pour éviter de surcharger */ }
}

@media (max-width: 640px) {
  header { padding: 18px 20px; }
  .hero { padding: 24px 20px 60px; }
  h1 { font-size: 38px; letter-spacing: -1px; }
  
  .contract-3d { width: 100%; max-width: 320px; }
  .contract-paper { padding: 1.2rem; }
  .action-btn { padding: 10px; }
  .cta-row { flex-direction: column; }
  .btn-primary, .btn-secondary { width: 100%; }
}
</style>