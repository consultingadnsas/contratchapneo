<template>
  <footer class="main-footer">
    <div class="footer-upper">
      <div class="footer-contact-col">
        <div class="social-links">
          <a href="#" aria-label="Instagram" class="social-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
          </a>
          <a href="#" aria-label="X" class="social-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4l11.733 16h4.267l-11.733 -16z M4 20l6.768 -6.768 M20 4l-6.768 6.768"></path></svg>
          </a>
          <a href="#" aria-label="YouTube" class="social-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"></path><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"></polygon></svg>
          </a>
        </div>
        
        <div class="contact-info">
          <p class="address">Angre 8e tranche, Chicken Nation<br />Abidjan, Côte d'Ivoire</p>
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
              <a href="#">{{ link }}</a>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="footer-divider-container">
      <div class="divider-line"></div>
      <button class="btn-get-started">Get Started</button>
    </div>

    <div class="footer-lower">
      <p class="brand-pitch">
        Avec contratchap, vous optez pour le meilleur du juridique et sécurisez votre business.
      </p>
      <div class="legal-links">
        <a href="#">TERMS & CONDITIONS</a>
        <a href="#">PRIVACY POLICY</a>
      </div>
    </div>

    <div class="giant-watermark">
      Contratchap
    </div>
  </footer>
</template>

<script lang="ts">
export default {
  name: 'FooterSection',
  setup() {
    const footerSections = [
      {
        title: 'MENU',
        links: ['Banque de contrats', 'Contrat sur mesure', 'Packs de contrats', 'Experts', 'Outils de calculs']
      },
      {
        title: 'SOCIAL',
        links: ['Face', 'Torebag', 'Hat', 'Blouse']
      },
      {
        title: 'CART',
        links: ['Blog', 'Contact', 'Terms', 'Tutorials']
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
  transition: border-color 0.3s, color 0.3s;
}

.social-icon:hover {
  border-color: #ffffff;
}

.social-icon svg {
  width: 18px;
  height: 18px;
}

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

.footer-column a:hover {
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

/* --- FILIGRANE ARRIÈRE-PLAN --- */
.giant-watermark {
  position: absolute;
  bottom: -2rem;
  left: 5%;
  font-size: 16vw;
  font-weight: 700;
  color: #151515;
  user-select: none;
  pointer-events: none;
  white-space: nowrap;
  z-index: 1;
  line-height: 1;
}

/* --- RESPONSIVE DESIGN (Tablettes et Ordinateurs) --- */
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