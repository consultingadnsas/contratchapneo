<template>
  <footer class="main-footer">
    <div class="footer-grid">
      <div 
        class="footer-section"
        v-for="(section, index) in footerSections" 
        :key="index"
      >
        <h3>{{ section.title }}</h3>
        <ul>
          <li v-for="(link, idx) in section.links" :key="idx">
            <a href="#">{{ link }}</a>
          </li>
        </ul>
      </div>
    </div>
    <!--  
      <div class="newsletter-section">
        <div class="newsletter-title">
            <h3>Souscrire à notre newsletter</h3>
            <p>Récevez de façon hebdomadaire des conseils juridiques et des ressources</p>
        </div>
        <div class="btn-actions">
            <Base-input/>
            <mainButton label="S'abonner"/>
        </div>
    </div>
    -->
    <div class="logo">
        <h3><span>Contrat</span>ChapNeo</h3>
    </div>
  </footer>
</template>

<script lang="ts">
import BaseInput from '../input/BaseInput.vue';
import mainButton from '../buttons/mainButton.vue';

export default {
    components:{
        BaseInput,
        mainButton
    },

    setup(){
        const footerSections = [
        {
            title: 'Company',
            links: ['À propos', 'Carrières', 'Presse']
        },
        {
            title: 'Product',
            links: ['Fonctionnalités', 'Tarifs', 'Tutoriels']
        },
        {
            title: 'Support',
            links: ['Centre d\'aide', 'Contact', 'FAQ']
        },
        {
            title: 'Social',
            links: ['Twitter', 'LinkedIn', 'GitHub']
        },
        {
            title: 'Legal',
            links: ['Confidentialité', 'Conditions', 'Cookies']
        }
        ]


        return{
            footerSections,
        }
    }


}
</script>

<style scoped>

/* Mobile first */

.main-footer {
  padding: 1rem;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background: var(--secondary-color);
  border-radius: 0.5rem;
}

.footer-grid {
  display: grid;
  grid-template-columns: 1fr 1fr; /* 2 colonnes sur mobile */
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.footer-section h3 {
  font-size: 1.125rem;
  margin-bottom: 0.75rem;
  font-weight: 600;
  color: var(--primary-color);
}

.footer-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-section li {
  margin-bottom: 0.5rem;
}

.footer-section a {
  text-decoration: none;
  color: #333;
}

.newsletter-section{
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.newsletter-title h3{
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--primary-color);
}

.newsletter-title p{
    font-size: 1.2rem;
    font-weight: 500;
    color: #3b3838;
}

.logo h3{
    font-family: 'Instrument Sans', sans-serif;
    font-size: 1.5rem;
    color: var(--primary-color);
    font-weight: 600;
}

.logo h3 span{
    color: #f3f3f3;
    background: var(--primary-color);
}

/* Tablet/Desktop */
@media (min-width: 768px) {
  .footer-grid {
    grid-template-columns: repeat(5, 1fr); /* 5 colonnes pour les 5 sections */
  }
}

</style>