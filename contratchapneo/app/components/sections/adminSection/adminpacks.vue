<template>
  <div class="packs-wrapper">
    
    <div class="header-section">
      <div class="title-row">
        <h3 class="section-title">Gestion des Offres (Packs)</h3>
        <div class="header-actions">
          <secondButton label="Nouveau pack" @click="addNewPackToView" />
          <mainButton label="Rafraîchir la liste" @click="adminStore.fetchPacks()" />
        </div>
      </div>
      <p class="gray-text text-sm">Ajustez les prix, modifiez les quantités de crédits et créez de nouveaux abonnements pour vos clients.</p>
    </div>

    <!-- Affichage d'un spinner s'il y a un chargement global -->
    <div v-if="adminStore.isLoading" class="loading-state">
      Chargement des offres...
    </div>

    <div v-else class="pricing-grid">
      <packageAdmin 
        v-for="pack in sortedPacks" 
        :key="pack.id" 
        :pack="pack" 
        @remove-pack="handleRemovePack" 
        @save-pack="handleSavePack"
      />
    </div>

  </div>
</template>

<script lang="ts">
import { computed, onMounted } from 'vue';
import mainButton from '../../buttons/mainButton.vue';
import secondButton from '../../buttons/secondButton.vue';
import packageAdmin from '../../cards/packageAdmin.vue';
import { useAdminPackStore } from '../../../stores/adminPackStore';

export default {
  name: 'AdminPacks',
  components: { 
    mainButton, 
    secondButton,
    packageAdmin 
  },
  setup() {
    const adminStore = useAdminPackStore();

    onMounted(() => {
      adminStore.fetchPacks();
    });

    const sortedPacks = computed(() => {
      // Tri par prix (du moins cher au plus cher)
      return [...adminStore.packs].sort((a, b) => (a.prix || 0) - (b.prix || 0));
    });

    // Création d'une carte vide temporaire sur l'interface
    const addNewPackToView = () => {
      adminStore.packs.push({
        id: 'temp-' + Date.now(), // ID temporaire pour le v-for
        title: 'Nouvelle Offre',
        description: '',
        prix: 0,
        promo_price: null,
        isPromoActive: false,
        nombre_credits: 0,
        nombre_customed_contract: 0,
        custom_contract_included: false,
        nombre_cartes_pro: 0,
        duree_validite_jours: 30,
        is_active: true
      });
    };

    // Suppression d'un pack
    const handleRemovePack = async (packId: string) => {
      if (packId.startsWith('temp-')) {
        // C'est juste une carte non sauvegardée, on la retire de la vue
        adminStore.packs = adminStore.packs.filter(p => p.id !== packId);
        return;
      }

      if (confirm('Êtes-vous sûr de vouloir supprimer ce pack définitivement ?')) {
        await adminStore.deletePack(packId);
      }
    };

    // Sauvegarde vers le backend (POST ou PATCH)
    // Sauvegarde vers le backend (POST ou PATCH)
    const handleSavePack = async (pack: any) => {
      const formData = new FormData();
      
      // ⚡️ CORRECTION : On sécurise les textes avec (|| '') et les nombres avec (|| 0)
      formData.append('title', pack.title || 'Sans titre');
      formData.append('description', pack.description || '');
      formData.append('prix', (pack.prix || 0).toString());
      
      // Gestion de la promotion
      if (pack.isPromoActive && pack.promo_price) {
        formData.append('promo_price', pack.promo_price.toString());
      } else {
        formData.append('promo_price', '');
      }

      formData.append('nombre_credits', (pack.nombre_credits || 0).toString());
      formData.append('nombre_customed_contract', (pack.nombre_customed_contract || 0).toString());
      
      // Validation logique (Si crédits > 0, alors option incluse = True)
      const isCustomIncluded = pack.nombre_customed_contract > 0 ? 'true' : 'false';
      formData.append('custom_contract_included', isCustomIncluded);
      
      formData.append('nombre_cartes_pro', (pack.nombre_cartes_pro || 0).toString());
      formData.append('duree_validite_jours', (pack.duree_validite_jours || 30).toString()); // 30 jours par défaut
      
      try {
        if (pack.id && !pack.id.startsWith('temp-')) {
          // Si l'ID est un vrai UUID, c'est une modification
          await adminStore.updatePack(pack.id, formData);
          alert(`Le pack "${pack.title}" a été mis à jour avec succès.`);
        } else {
          // C'est un nouveau pack à créer
          await adminStore.addNewPack(formData);
          // On retire la carte temporaire car l'action addNewPack ajoute la vraie carte renvoyée par Django
          adminStore.packs = adminStore.packs.filter(p => p.id !== pack.id);
          alert(`Le pack "${pack.title}" a été créé avec succès.`);
        }
      } catch (e) {
        alert("Une erreur s'est produite lors de la sauvegarde du pack.");
      }
    };

    return {
      adminStore,
      sortedPacks,
      addNewPackToView,
      handleRemovePack,
      handleSavePack
    };
  }
}
</script>

<style scoped>
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

.loading-state {
  text-align: center;
  padding: 3rem;
  color: #64748b;
  font-weight: 600;
}

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