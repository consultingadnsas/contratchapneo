<template>
  <div class="pricing-card" :class="pack.highlightClass">
    
    <div class="card-header">
      <div class="flex-between">
        <input type="text" v-model="pack.title" class="editable-title-input" placeholder="Nom du pack" />
        <button class="action-icon-btn delete-btn" @click="$emit('remove-pack', pack.id)" title="Supprimer ce pack">
          <component :is="TrashIcon" class="icon-sm" />
        </button>
      </div>
      <textarea v-model="pack.description" class="editable-desc-input mt-2" rows="2" placeholder="Description du pack..."></textarea>
    </div>

    <div class="pricing-controls">
      
      <div class="input-group">
        <label>Prix de base (FCFA)</label>
        <div class="input-with-icon">
          <input type="number" v-model="pack.basePrice" class="price-input" />
          <span class="currency-suffix">F</span>
        </div>
      </div>

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

    <div class="card-footer flex-grow">
      <h5 class="dark-text text-xs mb-2 text-uppercase">Inclus dans ce pack :</h5>
      <ul class="features-list">
        <li v-for="(feature, index) in pack.features" :key="index" class="feature-item">
          <component :is="CheckIcon" class="icon-xs text-green feature-check" />
          
          <textarea 
            v-model="pack.features[index]" 
            class="editable-feature-input" 
            rows="2" 
            placeholder="Nouveau service..."
          ></textarea>
          
          <button class="remove-feature-btn" @click="removeFeature(index)" title="Retirer">
            <component :is="XMarkIcon" class="icon-xs" />
          </button>
        </li>
      </ul>
      <button class="add-feature-btn" @click="addFeature">
        <component :is="PlusIcon" class="icon-xs" /> Ajouter un service
      </button>
    </div>

  </div>
</template>

<script lang="ts">
import { markRaw, PropType } from 'vue';
import { TagIcon, CheckIcon, PlusIcon, TrashIcon, XMarkIcon } from '@heroicons/vue/24/outline';

export default {
  name: 'PackageAdmin',
  props: {
    pack: {
      type: Object as PropType<any>,
      required: true
    }
  },
  emits: ['remove-pack'],
  setup(props) {
    const addFeature = () => {
      props.pack.features.push('');
    };

    const removeFeature = (index: number) => {
      props.pack.features.splice(index, 1);
    };

    const calculateDiscount = (base: number, promo: number) => {
      if (base <= 0 || promo >= base) return 0;
      return Math.round(((base - promo) / base) * 100);
    };

    return {
      addFeature,
      removeFeature,
      calculateDiscount,
      TagIcon: markRaw(TagIcon),
      CheckIcon: markRaw(CheckIcon),
      PlusIcon: markRaw(PlusIcon),
      TrashIcon: markRaw(TrashIcon),
      XMarkIcon: markRaw(XMarkIcon)
    };
  }
}
</script>

<style scoped>
/* Uniquement les styles de la carte */
.dark-text { color: #1e293b; }
.gray-text { color: #94a3b8; }
.text-orange { color: #f97316; }
.text-green { color: #10b981; }
.font-bold { font-weight: 900; }
.text-sm { font-size: 0.85rem; }
.text-xs { font-size: 0.75rem; }
.text-uppercase { text-transform: uppercase; letter-spacing: 0.5px; }
.mb-2 { margin-bottom: 0.5rem; }
.mt-2 { margin-top: 0.8rem; }
.flex-between { display: flex; justify-content: space-between; align-items: flex-start; }
.flex-align { display: flex; align-items: center; gap: 0.4rem; }
.flex-grow { flex-grow: 1; display: flex; flex-direction: column; }

.icon-xs { width: 14px; height: 14px; }
.icon-sm { width: 18px; height: 18px; }

.pricing-card {
  min-width: 350px; 
  flex: 1; 
  background: #ffffff; border-radius: 24px; padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.03); border: 1px solid #e2e8f0;
  display: flex; flex-direction: column; transition: 0.3s ease; position: relative;
}

.card-header { margin-bottom: 1.5rem; border-bottom: 1px solid #f1f5f9; padding-bottom: 1rem; }
.editable-title-input { font-size: 1.3rem; font-weight: 800; color: #1e293b; width: 100%; border: 1px dashed transparent; background: transparent; padding: 0.2rem; margin-left: -0.2rem; border-radius: 6px; outline: none; transition: 0.2s; }
.editable-title-input:hover { border-color: #cbd5e1; background: #f8fafc; }
.editable-title-input:focus { border-style: solid; border-color: #2563eb; background: #fff; }

.editable-desc-input { font-size: 0.85rem; color: #94a3b8; width: 100%; border: 1px dashed transparent; background: transparent; padding: 0.2rem; margin-left: -0.2rem; border-radius: 6px; outline: none; resize: none; transition: 0.2s; line-height: 1.4; font-family: inherit; }
.editable-desc-input:hover { border-color: #cbd5e1; background: #f8fafc; }
.editable-desc-input:focus { border-style: solid; border-color: #2563eb; background: #fff; }

.action-icon-btn { background: #f8fafc; border: 1px solid #e2e8f0; color: #94a3b8; width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: 0.2s; flex-shrink: 0; }
.delete-btn:hover { background: #fee2e2; border-color: #fecaca; color: #ef4444; }

.pricing-controls { display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1.5rem; }
.input-group label { display: block; font-size: 0.75rem; font-weight: 900; color: #94a3b8; margin-bottom: 0.3rem; }
.input-with-icon { display: flex; align-items: center; background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 10px; overflow: hidden; transition: 0.2s; }
.input-with-icon:focus-within { border-color: #1e293b; }
.border-orange:focus-within { border-color: #f97316; }

.price-input { flex: 1; border: none; background: transparent; padding: 0.6rem 0.8rem; font-size: 1rem; color: #1e293b; outline: none; -moz-appearance: textfield; min-width: 0; }
.price-input::-webkit-outer-spin-button, .price-input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
.currency-suffix { padding: 0.6rem 0.8rem; background: #f1f5f9; color: #94a3b8; font-weight: 900; border-left: 1px solid #cbd5e1; }

.promo-toggle-box { background: white; border: 1px solid #e2e8f0; border-radius: 16px; padding: 1rem; transition: 0.3s; }
.promo-active-bg { background: #fffbeb; border-color: #fde68a; }
.discount-indicator { display: inline-block; margin-top: 0.5rem; background: #fee2e2; color: #dc2626; padding: 0.2rem 0.6rem; border-radius: 6px; font-size: 0.7rem; font-weight: 700; }

.switch { position: relative; display: inline-block; width: 36px; height: 20px; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #cbd5e1; transition: .4s; border-radius: 34px; }
.slider:before { position: absolute; content: ""; height: 14px; width: 14px; left: 3px; bottom: 3px; background-color: #fff; transition: .4s; border-radius: 50%; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
input:checked + .slider { background-color: #f97316; }
input:checked + .slider:before { transform: translateX(16px); }

.card-footer { background: #f8fafc; margin: 0 -1.5rem -1.5rem -1.5rem; padding: 1.5rem; border-bottom-left-radius: 24px; border-bottom-right-radius: 24px; }
.features-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 0.6rem; }
.feature-item { display: flex; align-items: flex-start; gap: 0.5rem; position: relative; margin-bottom: 0.5rem; }
.feature-check { flex-shrink: 0; margin-top: 8px; }

.editable-feature-input { flex: 1; font-size: 0.9rem; color: #1e293b; border: 1px dashed transparent; background: transparent; padding: 0.4rem 0.6rem; border-radius: 8px; outline: none; transition: 0.2s; line-height: 1.5; width: 100%; min-height: 45px; resize: vertical; font-family: inherit; }
.editable-feature-input:hover { border-color: #cbd5e1; background: #f8fafc; }
.editable-feature-input:focus { border-style: solid; border-color: #2563eb; background: #fff; box-shadow: 0 2px 10px rgba(37, 99, 235, 0.05); }

.remove-feature-btn { background: transparent; border: none; color: #cbd5e1; cursor: pointer; padding: 0.4rem; border-radius: 6px; transition: 0.2s; margin-top: 4px; width: fit-content; }
.remove-feature-btn:hover { color: #ef4444; background: #fee2e2; }

.add-feature-btn { background: transparent; border: 1px dashed #cbd5e1; color: #94a3b8; font-size: 0.8rem; font-weight: 900; padding: 0.6rem; border-radius: 8px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.4rem; transition: 0.2s; width: 100%; margin-top: 1rem; }
.add-feature-btn:hover { border-color: #2563eb; color: #2563eb; background: #eff6ff; }
</style>