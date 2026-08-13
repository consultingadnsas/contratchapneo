<template>
  <!-- ⚡️ CORRECTION : On ajoute width: 100% pour empêcher la carte de se réduire à 0px dans la grille -->
  <div class="dynamic-card-wrapper">
    <!-- 1️⃣ Cas : L'utilisateur a un pack actif ET des crédits restants -->
    <contractCardProfile
      v-if="canUseCredits"
      :title="title"
      :description="description"
      :image="image"
      @view="$emit('view')"
      @buy="$emit('generate')" 
    />

    <!-- 2️⃣ Cas classique : Pas de pack ou 0 crédit -> Achat normal -->
    <contratCards
      v-else
      :title="title"
      :description="description"
      :price="price"
      :image="image"
      :promoPrice="promoPrice" 
      @view="$emit('view')"
      @buy="$emit('buy')"
    />
  </div>
</template>

<script lang="ts">
import { computed } from 'vue';
import { useProfileStore } from '../../stores/profileStore';
import contratCards from './contratCards.vue';
import contractCardProfile from './contractCardProfile.vue';

export default {
  name: 'ContractCardDynamic',
  components: {
    contratCards,
    contractCardProfile
  },
  props: {
    title: { type: String, required: true },
    description: { type: String, default: '' },
    price: { type: [String, Number], default: '' },
    image: { type: String, default: undefined },
    // ⚡️ NOUVEAU : On déclare promoPrice pour que le parent puisse le passer
    promoPrice: { type: [String, Number], default: null } 
  },
  emits: ['view', 'buy', 'generate'],
  setup() {
    const profileStore = useProfileStore();

    // ⚡️ SÉCURITÉ : On vérifie que userPacks est bien un tableau avant d'utiliser .find()
    const canUseCredits = computed(() => {
      const packs = Array.isArray(profileStore.userPacks) ? profileStore.userPacks : [];
      const activePack = packs.find((pack: any) => pack.is_active === true);
      const credits = Number(activePack?.credits_restants || 0);
      return !!activePack && credits > 0;
    });

    return {
      canUseCredits
    };
  }
};
</script>

<style scoped>
/* ⚡️ LA PIÈCE MANQUANTE DU PUZZLE CSS : */
.dynamic-card-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}
</style>