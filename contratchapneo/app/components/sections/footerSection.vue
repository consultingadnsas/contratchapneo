<template>
  <footer class="main-footer">
    <div class="footer-upper">
      <div class="footer-contact-col">
        <div class="social-links">
          
          <a href="https://www.tiktok.com/@contratchap?_r=1&_t=ZN-97pbVnfYGHO" target="_blank" aria-label="TikTok" class="social-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M9 12a4 4 0 1 0 4 4V4a5 5 0 0 0 5 5"></path>
            </svg>
          </a>
          
          <div class="social-dropdown">
            <button aria-label="Facebook" class="social-icon fb-btn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path>
              </svg>
            </button>
            <div class="social-dropdown-content">
              <a href="https://www.facebook.com/share/19HDjsnZdS/?mibextid=wwXIfr" target="_blank">🇨🇮 Côte d'Ivoire</a>
              <a href="https://www.facebook.com/share/18zWA2JiSH/?mibextid=wwXIfr" target="_blank">🇸🇳 Sénégal</a>
              <a href="https://www.facebook.com/share/14hKSAApwFB/?mibextid=wwXIfr" target="_blank">🇧🇯 Bénin</a>
            </div>
          </div>

          <a href="https://www.linkedin.com/company/contratchap/" target="_blank" aria-label="LinkedIn" class="social-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>
              <rect x="2" y="9" width="4" height="12"></rect>
              <circle cx="4" cy="4" r="2"></circle>
            </svg>
          </a>

        </div>
        
        <div class="contact-info">
          <p class="address">Angré 8e tranche, Chicken Nation<br />Abidjan, Côte d'Ivoire</p>
          <p class="email">Consultingadnsas@gmail.com</p>
          <p class="phone">+225 05 08 88 40 88</p>
          <p class="phone">+229 01 57 21 83 91</p>
        </div>
      </div>

      <div class="footer-grid">
        <div 
          class="footer-column"
          v-for="(section, index) in footerSections" 
          :key="index"
        >
          <h3 class="column-title">{{ section.title }}</h3>
          <ul>
            <li v-for="(link, idx) in section.links" :key="idx">
              <router-link v-if="link.path" :to="link.path">{{ link.label }}</router-link>
              <a v-else href="#">{{ link.label }}</a>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="footer-divider-container">
      <div class="divider-line"></div>
      <button class="btn-get-started" @click="$router.push('/contractBank')">Commencer maintenant</button>
    </div>

    <div class="footer-lower">
      <p class="brand-pitch">
        Avec ContratChap, vous optez pour le meilleur du juridique et sécurisez votre business.
      </p>
      <div class="legal-links">
        <router-link to="/">CONDITIONS D'UTILISATION</router-link>
        <router-link to="/">POLITIQUE DE CONFIDENTIALITÉ</router-link>
      </div>
    </div>

    <div class="watermark-wrapper">
      <div class="giant-watermark">
        ContratChap
      </div>
    </div>
  </footer>
</template>

<script lang="ts">
export default {
  name: 'FooterSection',
  setup() {
    // Structure mise à jour : Chaque lien a un "label" (le texte) et un "path" (la route)
    const footerSections = [
      {
        title: 'MENU',
        links: [
          { label: 'Banque de contrats', path: '/contractBank' },
          { label: 'Contrat sur mesure', path: '/contractBank/customContrat' },
          { label: 'Experts', path: '/pro' },
          { label: 'Outils de calculs', path: '/lawCalcul' },
          { label: 'Services Juridiques', path: '/services' }
        ]
      },
      {
        title: 'RESSOURCES',
        links: [
          { label: 'Notre Blog', },
          { label: 'Tutoriels',  },
          { label: 'FAQ', }
        ]
      },
      {
        title: 'À PROPOS',
        links: [
          { label: 'Qui sommes-nous ?', path: '/about' },
        ]
      }
    ];

    return {
      footerSections
    };
  }
}
</script>

<style scoped>
/* Base & Reset Intégré pour le footer */
.main-footer {
  position: relative;
  background-color: #0d0d0d;
  color: #ffffff;
  padding: 4rem 2rem 2rem 2rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  gap: 3rem;
  width: 100%;
  box-sizing: border-box;
  border-radius: 0.5rem;
}

/* --- SECTION HAUTE --- */
.footer-upper {
  display: flex;
  flex-direction: column;
  gap: 3rem;
  max-width: 1300px;
  width: 100%;
  margin: 0 auto;
  z-index: 2;
}

/* Infos contacts & Réseaux */
.footer-contact-col {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.social-links {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

.social-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: 1px solid #333333;
  border-radius: 50%;
  color: #ffffff;
  background: transparent;
  cursor: pointer;
  transition: border-color 0.3s, color 0.3s, background 0.3s;
}

.social-icon:hover {
  border-color: #ffffff;
  background: rgba(255, 255, 255, 0.1);
}

.social-icon svg {
  width: 18px;
  height: 18px;
}

/* --- MENU DÉROULANT FACEBOOK --- */
.social-dropdown {
  position: relative;
  display: inline-block;
}

.social-dropdown-content {
  visibility: hidden;
  opacity: 0;
  position: absolute;
  top: 130%; /* 👈 La bulle s'ouvre vers le BAS */
  left: 50%;
  transform: translateX(-50%) translateY(-10px); /* 👈 Animation adaptée */
  background-color: #1a1a1a;
  border: 1px solid #333333;
  min-width: 150px;
  border-radius: 12px;
  padding: 0.5rem;
  box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
  z-index: 10;
  transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

/* Petite flèche en haut de la bulle */
.social-dropdown-content::after {
  content: '';
  position: absolute;
  bottom: 100%; /* 👈 Place la flèche au-dessus de la bulle */
  top: auto;
  left: 50%;
  transform: translateX(-50%);
  border-width: 6px;
  border-style: solid;
  border-color: transparent transparent #1a1a1a transparent; /* 👈 Pointe vers le haut */
}

.social-dropdown:hover .social-dropdown-content,
.social-dropdown:focus-within .social-dropdown-content {
  visibility: visible;
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}

.social-dropdown-content a {
  color: #ffffff;
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 500;
  padding: 0.6rem 0.8rem;
  border-radius: 8px;
  transition: background 0.2s, color 0.2s;
  display: flex;
  align-items: center;
  white-space: nowrap;
}

.social-dropdown-content a:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

/* Contact info texts */
.contact-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  font-size: 1rem;
  line-height: 1.5;
  color: #ffffff;
}

.contact-info .address {
  color: #999999;
}

/* Grille de liens */
.footer-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  width: 100%;
}

.column-title {
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  margin-bottom: 1.5rem;
  color: #ffffff;
}

.footer-column ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.footer-column a {
  text-decoration: none;
  color: #999999;
  font-size: 0.95rem;
  transition: color 0.2s;
}

.footer-column a:hover, .footer-column a.router-link-active {
  color: #ffffff;
}

/* --- SECTION DE SÉPARATION --- */
.footer-divider-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  max-width: 1300px;
  width: 100%;
  margin: 1rem auto 0 auto;
  z-index: 2;
}

.divider-line {
  position: absolute;
  left: 0;
  right: 0;
  top: 50%;
  height: 1px;
  background-color: #262626;
  z-index: 1;
}

.btn-get-started {
  width: 50%;
  position: relative;
  z-index: 2;
  background-color: #ffffff;
  color: #000000;
  border: none;
  padding: 0.6rem 1.5rem;
  border-radius: 2rem;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: transform 0.2s, background-color 0.2s;
}

.btn-get-started:hover {
  background-color: #e5e5e5;
  transform: scale(1.02);
}

/* --- SECTION BASSE --- */
.footer-lower {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 1300px;
  width: 100%;
  margin: 0 auto;
  z-index: 2;
}

.brand-pitch {
  font-size: 0.9rem;
  color: #666666;
  line-height: 1.6;
  max-width: 400px;
}

.legal-links {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.legal-links a {
  text-decoration: none;
  color: #ffffff;
  font-size: 0.8rem;
  font-weight: 500;
  letter-spacing: 0.05em;
  transition: color 0.2s;
}

.legal-links a:hover {
  color: #999999;
}

.watermark-wrapper {
  position: absolute;
  inset: 0; /* Prend toute la taille du footer */
  overflow: hidden; /* Ne coupe QUE le filigrane */
  pointer-events: none;
  z-index: 1;
  border-radius: inherit;
}

/* --- FILIGRANE ARRIÈRE-PLAN --- */
.giant-watermark {
  position: absolute;
  bottom: -2rem;
  left: 5%;
  font-size: 14vw;
  font-weight: 700;
  color: #151515;
  user-select: none;
  pointer-events: none;
  white-space: nowrap;
  line-height: 1;
}

/* --- RESPONSIVE DESIGN --- */
@media (min-width: 768px) {
  .main-footer {
    padding: 6rem 4rem 3rem 4rem;
    gap: 4rem;
  }

  .footer-upper {
    flex-direction: row;
    justify-content: space-between;
    align-items: flex-start;
  }

  .footer-contact-col {
    max-width: 300px;
  }

  .footer-grid {
    grid-template-columns: repeat(3, 1fr);
    max-width: 600px;
    gap: 4rem;
  }

  .footer-lower {
    flex-direction: row;
    justify-content: space-between;
    align-items: flex-end;
  }
  
  .giant-watermark {
    bottom: -1rem;
    font-size: 14vw;
  }
}
</style>