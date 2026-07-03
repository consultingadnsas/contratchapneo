<template>
  <section class="trust-contact-section">
    <div class="trust-container">
      
      <!-- PARTIE VISUELLE : L'humain et la chaleur -->
      <div class="image-wrapper">
        <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=800&q=80" alt="Conseillère juridique souriante" class="advisor-img" />
      </div>

      <!-- PARTIE CONTENU : Le message et les contacts -->
      <div class="content-wrapper">
        <h2 class="title">Besoin d'aide ?<span>Contactez-nous.</span> </h2>
        <p class="subtitle">
          Le droit peut sembler complexe, mais vous n'êtes pas seul. Notre équipe d'experts OHADA est là pour vous écouter et vous orienter vers la bonne solution.
        </p>
        
        <!-- LES OPTIONS DE CONTACT -->
        <div class="contact-methods">
          
          <!-- Ligne 1 : Côte d'Ivoire -->
          <div class="phone-item">
            <div class="phone-info">
              <div class="text-group">
                <span class="label">Côte d'Ivoire</span>
                <!-- Classe ajoutée ici -->
                <strong class="number number-desktop">+225 05 08 88 40 88</strong>
              </div>
            </div>
            <!-- Classe ajoutée ici -->
            <a href="tel:+2250508884088" class="btn-call-solid btn-mobile">Appeler ici</a>
          </div>

          <!-- Ligne 2 : Bénin -->
          <div class="phone-item">
            <div class="phone-info">
              <div class="text-group">
                <span class="label">Bénin</span>
                <!-- Classe ajoutée ici -->
                <strong class="number number-desktop">+229 01 57 21 83 91</strong>
              </div>
            </div>
            <!-- Classe ajoutée ici -->
            <a href="tel:+2290157218391" class="btn-call-solid btn-mobile">Appeler ici</a>
          </div>

          <!-- Ligne 3 : Séparateur et WhatsApp (Icône seule) -->
          <div class="whatsapp-action">
            <span class="wa-text">Laissez nous un message</span>
            
            <a href="https://wa.me/2250508884088" target="_blank" rel="noopener noreferrer" class="wa-icon-only" title="Discuter sur WhatsApp">
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" viewBox="0 0 16 16">
                <path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c-.003 1.398.366 2.76 1.062 3.964L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z"/>
              </svg>
            </a>
          </div>

        </div>

      </div>

    </div>
  </section>
</template>

<script lang="ts">
export default {
  name: 'TrustContact',
  setup() {
    return {};
  }
}
</script>

<style scoped>
/* --- STRUCTURE GLOBALE --- */
.trust-contact-section {
  width: 100%;
  padding: 0.2rem 2.2rem;
  display: flex;
  justify-content: center;
  font-family: 'Inter', sans-serif;
  margin-bottom: 5rem;
}

.trust-container {
  max-width: 1100px;
  width: 100%;
  background: #f8fafc;
  border-radius: 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
  overflow: hidden; 
}

/* --- PARTIE IMAGE --- */
.image-wrapper {
  position: relative;
  width: 100%;
  height: 350px;
}

.advisor-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center top; 
}

.dot-online {
  width: 10px;
  height: 10px;
  background-color: #25D366; 
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(37, 211, 102, 0.4); }
  70% { box-shadow: 0 0 0 6px rgba(37, 211, 102, 0); }
  100% { box-shadow: 0 0 0 0 rgba(37, 211, 102, 0); }
}

/* --- PARTIE CONTENU --- */
.content-wrapper {
  padding: 3rem 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.title {
  font-size: clamp(2rem, 4vw, 2.5rem);
  font-weight: 800;
  color: var(--secondary-light-color);
  margin: 0 0 0.8rem 0;
  line-height: 1.2;
}
span {
  color: var(--primary-color);
}

.subtitle {
  font-size: 1rem;
  color: #64748b;
  line-height: 1.6;
  margin: 0 0 2rem 0;
}

/* --- LES OPTIONS DE CONTACT --- */
.contact-methods {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Cartes Numéros */
.phone-item {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 1rem 1.2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
}

.phone-item:hover {
  transform: translateY(-2px);
  border-color: #cbd5e1;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.04);
}

.phone-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.text-group {
  display: flex;
  flex-direction: column;
}

.label {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.1rem;
}

.number {
  font-size: 1.3rem;
  color: var(--primary-color);
  font-weight: 800;
}

.number-desktop { display: none;}
.btn-mobile {
  display: block;
  width: 100%;
  text-align: center;
}

/* Sur mobile, on ajuste la carte pour le bouton */
.phone-item {
  flex-direction: column;
  align-items: stretch; /* Le bouton prendra toute la largeur */
  gap: 1rem;
}


.btn-call-solid {
  background: #1e293b;
  color: #ffffff;
  padding: 0.6rem 1.2rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 600;
  text-decoration: none;
  transition: 0.2s ease;
}

.btn-call-solid:hover {
  background: #334155;
}

/* Section WhatsApp */
.whatsapp-action {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 1.5rem;
  margin-top: 0.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #f1f5f9;
}

.wa-text {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--primary-color-dark);
}

.wa-icon-only {
  width: 48px;
  height: 48px;
  background-color: #25D366;
  color: #ffffff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  box-shadow: 0 4px 15px rgba(37, 211, 102, 0.3);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.wa-icon-only:hover {
  transform: scale(1.1);
  box-shadow: 0 8px 20px rgba(37, 211, 102, 0.4);
}

/* --- RESPONSIVE DESKTOP --- */
@media (min-width: 900px) {
  .trust-container { flex-direction: row; }
  .image-wrapper { width: 45%; height: auto; min-height: 100%; }
  .content-wrapper { width: 55%; padding: 4rem; }
  .phone-item {
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    width: 80%;
  }
  
  /* Sur ordinateur, on AFFICHE le numéro */
  .number-desktop {
    display: block;
  }
  
  /* Sur ordinateur, on CACHE le bouton d'appel */
  .btn-mobile {
    display: none;
  }
}

@media (max-width: 480px) {
  .phone-item { flex-direction: column; align-items: flex-start; gap: 1rem; }
  .btn-call-solid { width: 100%; text-align: center; }
  .whatsapp-action { justify-content: space-between; }
}
</style>