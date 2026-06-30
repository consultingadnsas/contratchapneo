<template>
  <div class="packs-wrapper">
    
    <!-- EN-TÊTE -->
    <div class="header-section">
      <div class="title-row">
        <h3 class="section-title">Gestion des Offres (Basic, Business, Pro)</h3>
        <button class="btn-primary" @click="saveAllChanges">
          <component :is="CheckCircleIcon" class="icon-sm" /> Sauvegarder les tarifs
        </button>
      </div>
      <p class="gray-text text-sm">Ajustez les prix et activez vos campagnes promotionnelles pour vos 3 paliers d'abonnement.</p>
    </div>

    <!-- GRILLE DES 3 PALIERS -->
    <div class="pricing-grid">
      
      <div class="pricing-card" v-for="pack in subscriptionPacks" :key="pack.id" :class="pack.highlightClass">
        
        <!-- Haut de la carte : Titre et Description -->
        <div class="card-header">
          <div class="pack-badge" :class="pack.badgeClass">{{ pack.level }}</div>
          <h4 class="pack-title">{{ pack.title }}</h4>
          <p class="gray-text text-xs">{{ pack.description }}</p>
        </div>

        <!-- Section Tarification -->
        <div class="pricing-controls">
          
          <div class="input-group">
            <label>Prix de base (FCFA)</label>
            <div class="input-with-icon">
              <input type="number" v-model="pack.basePrice" class="price-input" />
              <span class="currency-suffix">F</span>
            </div>
          </div>

          <!-- Toggle Promotion -->
          <div class="promo-toggle-box" :class="{'promo-active-bg': pack.isPromoActive}">
            <div class="flex-between">
              <span class="dark-text font-bold text-sm flex-align">
                <component :is="TagIcon" class="icon-sm" :class="pack.isPromoActive ? 'text-orange' : 'text-gray'" /> 
                Offre Spéciale
              </span>
              <label class="switch">
                <input type="checkbox" v-model="pack.isPromoActive">
                <span class="slider round"></span>
              </label>
            </div>

            <!-- Prix Promo (Visible uniquement si la promo est activée) -->
            <div class="promo-input-section" v-if="pack.isPromoActive">
              <div class="input-group mt-2">
                <label class="text-orange">Nouveau prix promo</label>
                <div class="input-with-icon border-orange">
                  <input type="number" v-model="pack.promoPrice" class="price-input text-orange font-bold" />
                  <span class="currency-suffix text-orange">F</span>
                </div>
              </div>
              <div class="discount-indicator">
                Soit une réduction de {{ calculateDiscount(pack.basePrice, pack.promoPrice) }}%
              </div>
            </div>
          </div>

        </div>

        <!-- Liste récapitulative des avantages -->
        <div class="card-footer">
          <h5 class="dark-text text-xs mb-2 text-uppercase">Inclus dans ce pack :</h5>
          <ul class="features-list">
            <li v-for="(feature, index) in pack.features" :key="index">
              <component :is="CheckIcon" class="icon-xs text-green" />
              <span>{{ feature }}</span>
            </li>
          </ul>
        </div>

      </div>

    </div>

  </div>
</template>

<script lang="ts">
import { ref, markRaw } from 'vue';
import { 
  CheckCircleIcon, 
  TagIcon, 
  CheckIcon 
} from '@heroicons/vue/24/outline';

export default {
  name: 'AdminPacks',
  setup() {
    // Les 3 offres fixes de la plateforme
    const subscriptionPacks = ref([
      {
        id: 'basic',
        level: 'Niveau 1',
        title: 'Pack Basic',
        description: 'Idéal pour les entrepreneurs individuels qui se lancent.',
        basePrice: 15000,
        isPromoActive: false,
        promoPrice: 10000,
        features: ['Accès à 3 contrats gratuits au choix', 'Support par email (48h)', 'Mise à jour des modèles OHADA'],
        badgeClass: 'badge-blue',
        highlightClass: ''
      },
      {
        id: 'business',
        level: 'Niveau 2',
        title: 'Pack Business',
        description: 'Pour les PME nécessitant une structure légale complète.',
        basePrice: 45000,
        isPromoActive: true,
        promoPrice: 35000,
        features: ['Accès illimité au catalogue de base', '1 heure de consultation juridique', 'Support prioritaire (24h)'],
        badgeClass: 'badge-orange',
        highlightClass: 'card-highlighted' // Met en valeur le pack central
      },
      {
        id: 'pro',
        level: 'Niveau 3',
        title: 'Pack Business Pro',
        description: 'La solution VIP pour les entreprises en forte croissance.',
        basePrice: 120000,
        isPromoActive: false,
        promoPrice: 95000,
        features: ['Accès illimité à tous les documents', 'Révision de contrats sur-mesure', 'Consultations mensuelles incluses', 'Accès direct WhatsApp'],
        badgeClass: 'badge-purple',
        highlightClass: ''
      }
    ]);

    // Calcul mathématique du pourcentage de réduction
    const calculateDiscount = (base: number, promo: number) => {
      if (base <= 0 || promo >= base) return 0;
      return Math.round(((base - promo) / base) * 100);
    };

    // Simulation de sauvegarde
    const saveAllChanges = () => {
      console.log('Tarifs sauvegardés dans la BDD :', subscriptionPacks.value);
      alert('Les tarifs et promotions ont été mis à jour avec succès sur la plateforme.');
    };

    return {
      subscriptionPacks,
      calculateDiscount,
      saveAllChanges,
      CheckCircleIcon: markRaw(CheckCircleIcon),
      TagIcon: markRaw(TagIcon),
      CheckIcon: markRaw(CheckIcon)
    };
  }
}
</script>

<style scoped>
.packs-wrapper {
  --bg-panel: #ffffff;
  --bg-panel-light: #f8fafc;
  --text-dark: #1e293b;
  --text-gray: #94a3b8;
  --accent-blue: #2563eb;
  
  display: flex; flex-direction: column; gap: 2rem;
  font-family: 'Inter', sans-serif; padding-bottom: 2rem;
}

/* UTILITAIRES */
.dark-text { color: var(--text-dark); }
.gray-text { color: var(--text-gray); }
.text-orange { color: #f97316; }
.text-green { color: #10b981; }
.font-bold { font-weight: 700; }
.text-sm { font-size: 0.85rem; }
.text-xs { font-size: 0.75rem; }
.text-uppercase { text-transform: uppercase; letter-spacing: 0.5px; }
.mb-2 { margin-bottom: 0.5rem; }
.mt-2 { margin-top: 0.8rem; }
.flex-between { display: flex; justify-content: space-between; align-items: center; }
.flex-align { display: flex; align-items: center; gap: 0.4rem; }

.icon-xs { width: 14px; height: 14px; }
.icon-sm { width: 18px; height: 18px; }

/* EN-TÊTE */
.header-section { display: flex; flex-direction: column; gap: 0.5rem; }
.title-row { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
.section-title { font-size: 1.4rem; color: var(--text-dark); font-weight: 700; margin: 0; }
.btn-primary { background: var(--text-dark); color: white; border: none; padding: 0.7rem 1.2rem; border-radius: 12px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 0.5rem; transition: 0.2s; }
.btn-primary:hover { background: #0f172a; transform: translateY(-2px); }

/* GRILLE DES 3 PALIERS */
.pricing-grid { 
  display: grid; 
  grid-template-columns: repeat(3, 1fr); /* Force 3 colonnes sur grand écran */
  gap: 1.5rem; 
  align-items: stretch;
}

/* CARTE PALIERS */
.pricing-card {
  background: var(--bg-panel); border-radius: 24px; padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.03); border: 1px solid #e2e8f0;
  display: flex; flex-direction: column; transition: 0.3s ease; position: relative;
}
.card-highlighted { border: 2px solid var(--accent-blue); box-shadow: 0 15px 40px rgba(37, 99, 235, 0.1); }

/* EN-TÊTE DE CARTE */
.card-header { margin-bottom: 1.5rem; border-bottom: 1px solid #f1f5f9; padding-bottom: 1rem; }
.pack-badge { display: inline-block; padding: 0.3rem 0.8rem; border-radius: 50px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; margin-bottom: 0.8rem; }
.badge-blue { background: #eff6ff; color: #2563eb; }
.badge-orange { background: #fff7ed; color: #f97316; }
.badge-purple { background: #faf5ff; color: #a855f7; }
.pack-title { font-size: 1.2rem; font-weight: 800; color: var(--text-dark); margin: 0 0 0.4rem 0; }

/* CONTROLES TARIFAIRES */
.pricing-controls { display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1.5rem; }

.input-group label { display: block; font-size: 0.75rem; font-weight: 600; color: var(--text-gray); margin-bottom: 0.3rem; }
.input-with-icon { display: flex; align-items: center; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; overflow: hidden; transition: 0.2s; }
.input-with-icon:focus-within { border-color: var(--text-dark); }
.border-orange:focus-within { border-color: #f97316; }

.price-input { flex: 1; border: none; background: transparent; padding: 0.6rem 0.8rem; font-size: 1rem; color: var(--text-dark); outline: none; -moz-appearance: textfield; }
.price-input::-webkit-outer-spin-button, .price-input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
.currency-suffix { padding: 0.6rem 0.8rem; background: #f1f5f9; color: var(--text-gray); font-weight: 600; border-left: 1px solid #cbd5e1; }

/* ZONE PROMO */
.promo-toggle-box { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 1rem; transition: 0.3s; }
.promo-active-bg { background: #fffbeb; border-color: #fde68a; }
.discount-indicator { display: inline-block; margin-top: 0.5rem; background: #fee2e2; color: #dc2626; padding: 0.2rem 0.6rem; border-radius: 6px; font-size: 0.7rem; font-weight: 700; }

/* SWITCH CSS */
.switch { position: relative; display: inline-block; width: 36px; height: 20px; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #cbd5e1; transition: .4s; border-radius: 34px; }
.slider:before { position: absolute; content: ""; height: 14px; width: 14px; left: 3px; bottom: 3px; background-color: #fff; transition: .4s; border-radius: 50%; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
input:checked + .slider { background-color: #f97316; }
input:checked + .slider:before { transform: translateX(16px); }

/* AVANTAGES */
.card-footer { background: var(--bg-panel-light); margin: 0 -1.5rem -1.5rem -1.5rem; padding: 1.5rem; border-bottom-left-radius: 24px; border-bottom-right-radius: 24px; flex-grow: 1; }
.features-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 0.6rem; }
.features-list li { display: flex; align-items: flex-start; gap: 0.5rem; font-size: 0.85rem; color: var(--text-dark); line-height: 1.4; }

/* RESPONSIVE */
@media (max-width: 1024px) {
  .pricing-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .pricing-grid { grid-template-columns: 1fr; }
}
</style>