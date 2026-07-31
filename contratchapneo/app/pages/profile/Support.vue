<template>
  <div class="dashboard-container">
    
    <!-- Barre latérale de navigation -->
    <sidebar />
    
    <main class="main-content">
      
      <!-- En-tête de la page -->
      <header class="dashboard-header">
        <div>
          <h1 class="page-title">Support & Assistance</h1>
          <p class="subtitle">Notre équipe juridique et technique est à votre disposition pour vous accompagner.</p>
        </div>
      </header>
      
      <!-- Grille des canaux de contact -->
      <div class="support-grid">
        
        <!-- CARTE 1 : ASSISTANCE TÉLÉPHONIQUE & WHATSAPP -->
        <div class="support-card">
          <div class="card-icon-wrapper phone-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor" class="icon">
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 0 0 2.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 0 1-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 0 0-1.091-.852H4.5A2.25 2.25 0 0 0 2.25 4.5v2.25Z" />
            </svg>
          </div>
          <div class="card-content">
            <h2>Assistance Téléphonique</h2>
            <p class="description">
              Échangez de vive voix avec notre support client ou laissez nous un message sur Whatsapp pour toutes questions urgentes ou assistance sur vos packs.
            </p>
            
            <div class="contact-list">
              <!-- Numéro Côte d'Ivoire -->
              <a href="tel:+2250508884088" class="contact-item contact-item-row">
                <div class="contact-text">
                  <span class="label">Support Côte d'Ivoire</span>
                  <span class="value">+225 05 08 88 40 88</span>
                </div>
                <!-- Logo WhatsApp officiel à droite -->
                <div class="whatsapp-badge">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="whatsapp-icon">
                    <path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.77-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217l.332.006c.106.005.249-.04.39.298.144.347.491 1.2.534 1.287.043.087.072.188.014.304-.058.116-.087.188-.173.289l-.26.304c-.087.086-.177.18-.076.354.101.174.449.741.964 1.201.662.591 1.221.774 1.394.86s.28.072.383-.043c.101-.116.433-.506.549-.68.116-.173.231-.145.39-.087s1.011.477 1.184.564.289.13.332.202c.045.072.045.419-.1.824zM12.003 2c-5.522 0-9.999 4.478-10 10.001 0 1.763.459 3.486 1.332 5.01L2 22l5.12-1.341c1.468.801 3.142 1.224 4.881 1.224 5.522 0 10-4.478 10-10.001S17.525 2 12.003 2zm0 18.254c-1.579 0-3.125-.424-4.473-1.226l-.321-.191-3.328.873.887-3.244-.21-.334c-.87-1.385-1.33-2.986-1.329-4.631.001-4.547 3.701-8.247 8.25-8.247s8.249 3.7 8.249 8.247-3.7 8.253-8.248 8.253z"/>
                  </svg>
                </div>
              </a>

              <!-- Numéro Bénin -->
              <a href="tel:+2290157218391" class="contact-item contact-item-row">
                <div class="contact-text">
                  <span class="label">Support Bénin</span>
                  <span class="value">+229 01 57 21 83 91</span>
                </div>
                <!-- Logo WhatsApp officiel à droite -->
                <div class="whatsapp-badge">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="whatsapp-icon">
                    <path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.77-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217l.332.006c.106.005.249-.04.39.298.144.347.491 1.2.534 1.287.043.087.072.188.014.304-.058.116-.087.188-.173.289l-.26.304c-.087.086-.177.18-.076.354.101.174.449.741.964 1.201.662.591 1.221.774 1.394.86s.28.072.383-.043c.101-.116.433-.506.549-.68.116-.173.231-.145.39-.087s1.011.477 1.184.564.289.13.332.202c.045.072.045.419-.1.824zM12.003 2c-5.522 0-9.999 4.478-10 10.001 0 1.763.459 3.486 1.332 5.01L2 22l5.12-1.341c1.468.801 3.142 1.224 4.881 1.224 5.522 0 10-4.478 10-10.001S17.525 2 12.003 2zm0 18.254c-1.579 0-3.125-.424-4.473-1.226l-.321-.191-3.328.873.887-3.244-.21-.334c-.87-1.385-1.33-2.986-1.329-4.631.001-4.547 3.701-8.247 8.25-8.247s8.249 3.7 8.249 8.247-3.7 8.253-8.248 8.253z"/>
                  </svg>
                </div>
              </a>
            </div>
          </div>
        </div>

        <!-- CARTE 2 : ASSISTANCE PAR EMAIL -->
        <div class="support-card">
          <div class="card-icon-wrapper email-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor" class="icon">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
            </svg>
          </div>
          <div class="card-content">
            <h2>Assistance par Email</h2>
            <p class="description">
              Envoyez-nous un courrier électronique. Nous vous répondons généralement en moins de 24 heures ouvrées.
            </p>
            
            <div class="contact-list">
              <a href="mailto:Consultingadnsas@gmail.com" class="contact-item">
                <span class="label">Aide & Questions</span>
                <span class="value">Consultingadnsas@gmail.com</span>
              </a>
              <a href="mailto:contact@contratchapneo.com" class="contact-item">
                <span class="label">Service Commercial</span>
                <span class="value">contact@contratchapneo.com</span>
              </a>
            </div>
          </div>
        </div>

      </div>

      <!-- CARTE D'INFORMATION : HORAIRES D'OUVERTURE -->
      <section class="info-banner">
        <div class="info-icon">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor" class="icon-small">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
          </svg>
        </div>
        <div class="info-text">
          <strong>Horaires d'accessibilité du support :</strong>
          <span>Du Lundi au Vendredi de 08h30 à 18h00 GMT.</span>
        </div>
      </section>

    </main>
    
  </div>
</template>

<script lang="ts">
import sidebar from '../../components/navigation/sidebar.vue';

export default {
  name: 'SupportPage',
  components: {
    sidebar
  },
  setup() {
    return {};
  }
};
</script>

<style scoped>
/* =========================================
   STRUCTURE GLOBALE DU DASHBOARD
========================================= */
.dashboard-container {
  --bg-pearl: #f8fafc;        
  --text-night: #0f172a;      
  --text-muted: #64748b;
  --primary-navy: #000e2d;
  --accent-blue: #156ca9;
  --accent-indigo: #5452f4;
  --whatsapp-green: #25D366; /* 👈 Couleur officielle WhatsApp */
  --border-light: #e2e8f0;
  --card-bg: #ffffff;
  
  display: flex;
  flex-direction: column;
  height: 100dvh; 
  background-color: var(--bg-pearl);
  color: var(--text-night);
  font-family: 'Inter', system-ui, sans-serif;
  overflow: hidden; 
}

@media (min-width: 1024px) {
  .dashboard-container {
    flex-direction: row;
  }
}

/* =========================================
   CONTENU PRINCIPAL (ZONE DE SCROLL)
========================================= */
.main-content {
  flex: 1; 
  padding: 1.5rem;
  padding-bottom: 85px;
  overflow-y: auto; 
  overflow-x: hidden; 
}

@media (min-width: 1024px) {
  .main-content {
    padding: 2.5rem;
    padding-bottom: 2.5rem; 
  }
}

/* =========================================
   EN-TÊTE DE LA PAGE
========================================= */
.dashboard-header { 
  margin-bottom: 2rem;
}

.page-title { 
  font-size: 1.6rem; 
  font-weight: 800; 
  color: var(--primary-navy); 
  margin: 0 0 0.35rem 0;
  letter-spacing: -0.02em;
}

.subtitle { 
  color: var(--text-muted); 
  font-size: 0.95rem; 
  margin: 0;
}

/* =========================================
   GRILLE DES CARTES DE SUPPORT
========================================= */
.support-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

@media (min-width: 768px) {
  .support-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* --- CARTES INDIVIDUELLES --- */
.support-card {
  background-color: var(--card-bg);
  border: 1px solid var(--border-light);
  border-radius: 16px;
  padding: 1.8rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  box-shadow: 0 4px 15px rgba(15, 23, 42, 0.03);
  transition: all 0.25s ease;
}

.support-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 25px rgba(15, 23, 42, 0.08);
  border-color: #cbd5e1;
}

/* --- ICÔNES DES CARTES --- */
.card-icon-wrapper {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.phone-icon {
  background-color: rgba(21, 108, 169, 0.1);
  color: var(--accent-blue);
}

.email-icon {
  background-color: rgba(84, 82, 244, 0.1);
  color: var(--accent-indigo);
}

.icon {
  width: 26px;
  height: 26px;
}

/* --- CONTENU DE LA CARTE --- */
.card-content h2 {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--primary-navy);
  margin: 0 0 0.5rem 0;
}

.description {
  font-size: 0.9rem;
  color: var(--text-muted);
  line-height: 1.5;
  margin: 0 0 1.5rem 0;
}

/* --- LISTE DES CONTACTS --- */
.contact-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.contact-item {
  display: flex;
  flex-direction: column;
  padding: 0.85rem 1rem;
  background-color: var(--bg-pearl);
  border: 1px solid transparent;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s ease;
}

/* ⚡️ ALIGNEMENT HORIZONTAL (Texte à gauche / WhatsApp à droite) */
.contact-item-row {
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}

.contact-text {
  display: flex;
  flex-direction: column;
}

.contact-item:hover {
  background-color: #ffffff;
  border-color: var(--accent-blue);
  box-shadow: 0 2px 8px rgba(21, 108, 169, 0.1);
}

.contact-item .label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--text-muted);
  letter-spacing: 0.5px;
  margin-bottom: 0.2rem;
}

.contact-item .value {
  font-size: 1rem;
  font-weight: 700;
  color: var(--primary-navy);
}

.contact-item:hover .value {
  color: var(--accent-blue);
}

/* --- BADGE & LOGO WHATSAPP --- */
.whatsapp-badge {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background-color: rgba(37, 211, 102, 0.12); /* Vert WhatsApp très doux */
  color: var(--whatsapp-green);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25s ease;
}

.whatsapp-icon {
  width: 22px;
  height: 22px;
}

/* Au survol de la ligne, le badge s'allume en vert vif avec icône blanche ! */
.contact-item:hover .whatsapp-badge {
  background-color: var(--whatsapp-green);
  color: #ffffff;
  transform: scale(1.05);
}

/* =========================================
   BANNIÈRE D'INFORMATION (HORAIRES)
========================================= */
.info-banner {
  background-color: var(--card-bg);
  border: 1px solid var(--border-light);
  border-radius: 14px;
  padding: 1.25rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.info-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #f1f5f9;
  color: var(--primary-navy);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.icon-small {
  width: 20px;
  height: 20px;
}

.info-text {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  font-size: 0.9rem;
  color: var(--text-muted);
}

.info-text strong {
  color: var(--primary-navy);
  font-weight: 700;
}

/* --- RESPONSIVE MOBILE --- */
@media (max-width: 480px) {
  .support-card {
    padding: 1.4rem;
  }
  
  .info-banner {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>