<template>
    <div class="cart-items">
      <div class="items-list">
        <div v-for="item in cartItems" :key="item.id" class="cart-item">
          <img :src="item.image || placeholder" :alt="item.name" class="item-image">
          <div class="item-details">
            <h4 class="item-name">{{ item.name }}</h4>
          </div>

          <div class="item-total">
              <span class="total-price">{{ (Number(item.price) * item.quantity).toLocaleString('fr-FR') }} FCFA</span>
              
              <button 
                v-if="!isCheckout || item.isPack"
                type="button" 
                class="remove-btn" 
                :disabled="cartStore.isLoading" 
                @click.prevent="removeFromCart(item.cartItemId)"
              >🗑️</button>
          </div>
        </div>
      </div>

      <div class="order-summary">
          <!-- Sous-total -->
          <div class="summary-line">
            <span>Sous-total</span>
            <span>{{ cartStore.formattedSubtotalPrice || formattedTotalPrice }} FCFA</span>
          </div>
          
          <!-- Ligne de réduction active -->
          <div v-if="hasActiveDiscount" class="summary-line discount-line">
            <span>
              Réduction 
              <strong v-if="cartStore.cart?.coupon_code">({{ cartStore.cart.coupon_code }})</strong>
            </span>
            <div class="discount-actions">
              <span class="discount-amount">- {{ formattedDiscount }} FCFA</span>
              <button 
                type="button" 
                class="remove-coupon-btn" 
                :disabled="cartStore.isLoading" 
                @click.prevent="removePromoCode"
                title="Retirer le code promo"
              >
                ✕
              </button>
            </div>
          </div>

          <!-- ⚡️ NOUVEAU : Caché si un code est déjà actif -->
          <div v-if="!hasActiveDiscount" class="summary-line">
            <span>J'ai un code promo</span>
            <input type="checkbox" v-model="hasPromoCode" class="toggle" />
          </div>

          <!-- ⚡️ NOUVEAU : Caché si un code est déjà actif -->
          <div v-if="!hasActiveDiscount && hasPromoCode" class="promo-code-container">
            <input 
              type="text" 
              v-model="promoCode" 
              placeholder="Entrez votre code" 
              class="promo-input" 
              :disabled="cartStore.isLoading"
              @keyup.enter="applyPromoCode"
            />
            <button 
              type="button" 
              class="promo-apply-btn" 
              :disabled="cartStore.isLoading || !promoCode.trim()"
              @click="applyPromoCode"
            >
              {{ cartStore.isLoading ? '...' : 'Appliquer' }}
            </button>
          </div>

          <!-- Retours visuels (Succès / Erreur) -->
          <p v-if="couponError" class="promo-feedback error">{{ couponError }}</p>
          <p v-if="couponSuccess" class="promo-feedback success">{{ couponSuccess }}</p>

          <!-- Total final -->
          <div class="summary-line total">
            <span>Total</span>
            <span class="final-price">{{ formattedTotalPrice }} FCFA</span>
          </div>
      </div>
    </div>
</template>

<script lang="ts">
import { computed, ref, watch } from 'vue';
import { useCartStore } from '../../stores/cartStore';
import placeholder from '@/assets/pictures/ContratChap/pexels-thirdman-5060819.jpg';

export default {
  name: 'Itemslist',
  props: {
    isCheckout: {
      type: Boolean,
      default: false
    }
  },
  setup() {
    const cartStore = useCartStore();

    const cartItems = computed(() => (
      (cartStore.cart?.items ?? []).map(i => {
        let itemName = 'Article inconnu';
        let itemImage = null;
        let targetId = i.id; 

        if (i.contrat) {
          itemName = i.contrat.title;
          itemImage = i.contrat.picture;
          targetId = i.contrat.id; 
        } 
        else if (i.pro) {
          itemName = `${i.pro.first_name} ${i.pro.last_name}`; 
          itemImage = i.pro.profile_picture;
          targetId = i.pro.id; 
        }
        else if (i.pack || i.packs) {
          const packObj = i.pack || i.packs;
          itemName = `Pack : ${packObj.title || packObj.name || 'Inconnu'}`; 
          itemImage = packObj.picture;
          targetId = packObj.id; 
        }
        else if (i.customed_contract || i.customized_contract) {
          const customObj = i.customed_contract || i.customized_contract;
          itemName = customObj.title || customObj.name || 'Contrat sur mesure';
          itemImage = customObj.picture || null;
          targetId = customObj.id;
        }
        else if (i.contract_revision || i.revision) {
          const revObj = i.contract_revision || i.revision;
          itemName = revObj.title || revObj.name || 'Révision de contrat';
          itemImage = revObj.picture || null;
          targetId = revObj.id;
        }
        else if (i.title || i.name) {
          itemName = i.title || i.name;
        }

        return {
          cartItemId: i.id,
          id: targetId,
          name: itemName,
          price: Number(i.unit_price || 0), 
          subtotal: Number(i.subtotal || 0), 
          quantity: i.quantity,
          image: itemImage,
          isPack: !!(i.pack || i.packs)
        };
      })
    ));

    const formattedTotalPrice = computed(() => cartStore.formattedTotalPrice);

    // ⚡️ --- LOGIQUE CODE PROMO (Importée depuis la modale) --- ⚡️
    const hasPromoCode = ref(false);
    const promoCode = ref('');
    const couponError = ref<string | null>(null);
    const couponSuccess = ref<string | null>(null);

    const hasActiveDiscount = computed(() => {
      const discountVal = Number(cartStore.cart?.discount || 0);
      const hasItems = (cartStore.cart?.items?.length || 0) > 0;
      // ⚡️ CORRECTION : La réduction n'est active QUE s'il y a un montant de réduction ET des articles dans le panier
      return discountVal > 0 && hasItems;
    });

    const formattedDiscount = computed(() => {
      const discountVal = Number(cartStore.cart?.discount || 0);
      return discountVal.toLocaleString('fr-FR');
    });

    const applyPromoCode = async () => {
      if (!promoCode.value.trim() || cartStore.isLoading) return;
      
      couponError.value = null;
      couponSuccess.value = null;

      const success = await cartStore.applyCoupon(promoCode.value.trim());
      if (success) {
        couponSuccess.value = "Code promo appliqué !";
        promoCode.value = '';
      } else {
        couponError.value = cartStore.error || "Ce code promo est invalide ou expiré.";
      }
    };

    const removePromoCode = async () => {
      if (cartStore.isLoading) return;
      couponError.value = null;
      couponSuccess.value = null;

      try {
        const success = await cartStore.removeCoupon();
        if (success) {
          couponSuccess.value = "Code promo retiré.";
          promoCode.value = '';
          
          setTimeout(() => {
            couponSuccess.value = null;
          }, 3000);
        } else {
          couponError.value = cartStore.error || "Erreur lors de la suppression.";
        }
      } catch (e) {
        couponError.value = "Une erreur est survenue.";
      }
    };

    // --- LOGIQUE PANIER ---
    const removeFromCart = async (id: string) => {
      try {
        await cartStore.removeFromCart(id);
      } catch (e) {
        console.error("Erreur lors de la suppression:", e);
      }
    };

    return {
      cartStore,
      cartItems,
      formattedTotalPrice,
      removeFromCart,
      placeholder,
      // On retourne les variables du code promo à la vue
      hasPromoCode,
      promoCode,
      couponError,
      couponSuccess,
      hasActiveDiscount,
      formattedDiscount,
      applyPromoCode,
      removePromoCode
    }
  }
}
</script>

<style scoped>
/* Liste des articles */
.cart-items {
  padding: 1rem 0;
}

.cart-item {
  display: flex;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid #f0f0f0;
  align-items: center;
}

.cart-item:last-child {
  border-bottom: none;
}

.item-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 0.5rem;
  background: #f8f9fa;
}

.item-details {
  flex: 1;
}

.item-name {
  margin: 0 0 0.25rem 0;
  font-size: 0.95rem;
  font-weight: 500;
  color: #333;
}

.item-price {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  color: #202b4a;
  font-weight: 600;
}

.qty-btn {
  width: 28px;
  height: 28px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.2s;
}

/* ⚡️ Amélioration visuelle quand le bouton est désactivé (pendant le chargement API) */
.qty-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
  background: #f1f5f9;
}

.quantity {
  font-weight: 600;
  min-width: 20px;
  text-align: center;
}

.item-total {
  text-align: right;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
}

.total-price {
  font-weight: 600;
  color: #1a1a1a;
}

.remove-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  opacity: 0.6;
  padding: 0.25rem;
  transition: opacity 0.2s;
}

.remove-btn:disabled {
  opacity: 0.2;
  cursor: not-allowed;
}

/* Résumé de commande */
.order-summary {
  background: #f8f9fa;
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin-top: 1.5rem;
}

.summary-line {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
}

.summary-line.total {
  border-top: 1px solid #ddd;
  padding-top: 0.75rem;
  margin-top: 0.75rem;
  font-weight: 600;
  font-size: 1.1rem;
}

.final-price {
  color: #202b4a;
}
/* ⚡️ --- STYLES CODE PROMO --- ⚡️ */
.discount-line {
  color: #16a34a;
  align-items: center;
}

.discount-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.discount-amount {
  font-weight: 600;
  white-space: nowrap;
}

.remove-coupon-btn {
  background: none;
  border: none;
  color: #dc2626;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: bold;
  padding: 0 0.25rem;
  transition: opacity 0.2s;
}

.remove-coupon-btn:hover {
  opacity: 0.7;
}

.promo-code-container {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  animation: slideDown 0.3s ease-out;
}

.promo-input {
  flex: 1;
  padding: 0.6rem 0.8rem;
  border: 1px solid #ddd;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  outline: none;
  transition: border-color 0.2s;
}

.promo-input:focus {
  border-color: #202b4a;
}

.promo-apply-btn {
  background: #1a1a1a;
  color: white;
  border: none;
  padding: 0 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.9rem;
  transition: background 0.2s;
}

.promo-apply-btn:hover:not(:disabled) {
  background: #333;
}

.promo-apply-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.promo-feedback {
  font-size: 0.8rem;
  margin: 0.25rem 0 0.75rem 0;
  animation: slideDown 0.2s ease-out;
}

.promo-feedback.error {
  color: #dc2626;
}

.promo-feedback.success {
  color: #16a34a;
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>