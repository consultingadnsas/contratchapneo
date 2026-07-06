<template>
  <div class="packs-wrapper">
    
    <div class="header-section">
      <div class="title-row">
        <h3 class="section-title">Gestion des Offres</h3>
        <div class="header-actions">
          <secondButton label="Nouveau pack" @click="addNewPack" />
          <mainButton label="Actualiser les packs" @click="saveAllChanges" />
        </div>
      </div>
      <p class="gray-text text-sm">Ajustez les prix, modifiez les textes et ajoutez de nouveaux packs. Ils s'ordonneront automatiquement selon leur prix de base.</p>
    </div>

    <div class="pricing-grid">
      <packageAdmin 
        v-for="pack in sortedPacks" 
        :key="pack.id" 
        :pack="pack" 
        @remove-pack="removePack" 
      />
    </div>

  </div>
</template>

<script lang="ts">
import { ref, computed } from 'vue';
import mainButton from '../../buttons/mainButton.vue';
import secondButton from '../../buttons/secondButton.vue';
import packageAdmin from '../../cards/packageAdmin.vue'; // Assure-toi du bon chemin d'importation

export default {
  name: 'AdminPacks',
  components: { 
    mainButton, 
    secondButton,
    packageAdmin 
  },
  setup() {
    const subscriptionPacks = ref([
      {
        id: 'basic',
        title: 'Pack Basic',
        description: 'Packs idéal pour les petites entreprises',
        basePrice: 29000,
        isPromoActive: false,
        promoPrice: 10000,
        features: ['Accès à 10 documents juridiques payants', 'Très petite entreprise ou consultant individuel'],
        highlightClass: ''
      },
      {
        id: 'business',
        title: 'Pack Business',
        description: 'Accédez à une fourniture de contrat bien plus épurée et d\'autres avantages intéressant',
        basePrice: 49000,
        isPromoActive: true,
        promoPrice: 35000,
        features: ['Accès à 12 documents juridiques payants','Rédaction sur-mesure d\'un document juridique' ,'PME et startup de moins de 10 employés avec un volume de tâche juridique modéré'],
        highlightClass: 'card-highlighted'
      },
      {
        id: 'pro',
        title: 'Pack Business Pro',
        description: 'Profitez de la pleine puissance de Contratchap. Accédez à une panoplie de contrats, de service, de conseil, et de nos outils de calcules',
        basePrice: 99000,
        isPromoActive: false,
        promoPrice: 80000,
        features: ['Accès à 25 documents juridiques payants', 'Rédaction sur-mesure de 3 documents juridiques', 'Suivi par une équipe de juristes(appuie et conseil personnalisés)', 'PME et startup de plus de 10 employés avec un volume de tâche juridique important'],
        highlightClass: ''
      }
    ]);

    const sortedPacks = computed(() => {
      return [...subscriptionPacks.value].sort((a, b) => a.basePrice - b.basePrice);
    });

    const addNewPack = () => {
      subscriptionPacks.value.push({
        id: 'pack-' + Date.now(),
        title: 'Nouveau Pack',
        description: 'Description de votre nouvelle offre.',
        basePrice: 0,
        isPromoActive: false,
        promoPrice: 0,
        features: ['Premier avantage inclus'],
        highlightClass: ''
      });
    };

    const removePack = (id: string) => {
      if (confirm('Êtes-vous sûr de vouloir supprimer ce pack définitivement ?')) {
        subscriptionPacks.value = subscriptionPacks.value.filter(p => p.id !== id);
      }
    };

    const saveAllChanges = () => {
      console.log('Modifications sauvegardées :', subscriptionPacks.value);
      alert('Les tarifs, les textes et les offres ont été mis à jour avec succès.');
    };

    return {
      subscriptionPacks,
      sortedPacks,
      addNewPack,
      removePack,
      saveAllChanges
    };
  }
}
</script>

<style scoped>
/* Styles globaux de la page et de la grille */
.packs-wrapper {
  display: flex; flex-direction: column; gap: 2rem; padding-bottom: 2rem;
  font-family: 'Inter', sans-serif;
}

.gray-text { color: #94a3b8; }
.text-sm { font-size: 0.85rem; }

.header-section { display: flex; flex-direction: column; gap: 0.5rem; }
.title-row { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
.section-title { font-size: 1.4rem; color: #1e293b; font-weight: 700; margin: 0; }
.header-actions { display: flex; gap: 0.8rem; align-items: center;  }

.pricing-grid { 
  display: flex; 
  gap: 1.5rem; 
  align-items: stretch;
  overflow-x: auto; 
  padding-bottom: 1rem; 
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 transparent;
}
.pricing-grid::-webkit-scrollbar { height: 8px; }
.pricing-grid::-webkit-scrollbar-thumb { background-color: #cbd5e1; border-radius: 10px; }

@media (max-width: 700px){
  .header-actions{ flex-direction: column; }
}
</style>