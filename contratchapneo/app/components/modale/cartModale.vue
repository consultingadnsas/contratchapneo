<template>
  <div v-if="isOpen" class="cart-modal-overlay" @click="closeModal">
    <div class="cart-modal-content" @click.stop>
      <div class="cart-header">
        <div class="drag-handle"></div>
        <div class="cart-title">
          <h2>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 1 0-7.5 0v4.5m11.356-1.993 1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 0 1-1.12-1.243l1.264-12A1.125 1.125 0 0 1 5.513 7.5h12.974c.576 0 1.059.435 1.119 1.007ZM8.625 10.5a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm7.5 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z" />
            </svg>
            Mon Panier de contrats
          </h2>
          <span class="item-count">{{ cartStore.totalItems }} Contrat{{ cartStore.totalItems > 1 ? 's' : '' }}</span>
        </div>
        <button class="close-icon" type="button" @click.prevent="closeModal">x</button>
      </div>

      <div class="cart-body">
        <div v-if="cartStore.isEmpty" class="empty-cart">
          <div class="empty-icon">🛒</div>
          <h3>Votre panier est vide</h3>
          <p>Ajoutez des articles pour commencer vos achats</p>
          <checkoutButton label="continuer mes achats" @click="closeModal" />
        </div>

        <template v-else>
          <div class="cart-items">
            <div class="items-list">
              <div v-for="item in cartStore.cart.items" :key="item.id" class="cart-item">
                
                <!-- CAS 1: CONTRAT -->
                <template v-if="item.contrat">
                  <img :src="item.contrat.picture || picture" :alt="item.contrat.title" class="item-image">
                  <div class="item-details">
                    <h4 class="item-name">{{ item.contrat.title }}</h4>
                    <p class="item-price">{{ Number(item.unit_price).toLocaleString('fr-FR') }} FCFA</p>
                    
                    <div class="quantity-controls">
                      <button type="button" class="qty-btn" :disabled="item.quantity <= 1 || cartStore.isLoading" @click.prevent="handleUpdateQuantity(item.contrat.id, item.quantity - 1)">-</button>
                      <span class="quantity">{{ item.quantity }}</span>
                      <button type="button" class="qty-btn" :disabled="cartStore.isLoading" @click.prevent="handleUpdateQuantity(item.contrat.id, item.quantity + 1)">+</button>
                    </div>
                  </div>
                  <!-- 🔥 CORRECTION : On remet item.id pour la suppression -->
                  <div class="item-total">
                    <span class="total-price">{{ Number(item.subtotal).toLocaleString('fr-FR') }} FCFA</span>
                    <button type="button" class="remove-btn" :disabled="cartStore.isLoading" @click.prevent="handleRemove(item.id)">🗑️</button>
                  </div>
                </template>

                <!-- CAS 2: PROFESSIONNEL -->
                <template v-else-if="item.pro">
                  <img :src="item.pro.profile_picture || picture" :alt="item.pro.first_name" class="item-image" style="border-radius: 50%; object-fit: cover;">
                  <div class="item-details">
                    <h4 class="item-name">{{ item.pro.first_name }} {{ item.pro.last_name }}</h4>
                    <p style="font-size: 0.85em; color: gray;">{{ item.pro.title_display }}</p>
                    <p class="item-price">{{ Number(item.unit_price).toLocaleString('fr-FR') }} FCFA</p>
                    
                    <div class="quantity-controls">
                      <button type="button" class="qty-btn" :disabled="item.quantity <= 1 || cartStore.isLoading" @click.prevent="handleUpdateQuantity(item.pro.id, item.quantity - 1)">-</button>
                      <span class="quantity">{{ item.quantity }}</span>
                      <button type="button" class="qty-btn" :disabled="cartStore.isLoading" @click.prevent="handleUpdateQuantity(item.pro.id, item.quantity + 1)">+</button>
                    </div>
                  </div>
                  <!-- 🔥 CORRECTION : On remet item.id pour la suppression -->
                  <div class="item-total">
                    <span class="total-price">{{ Number(item.subtotal).toLocaleString('fr-FR') }} FCFA</span>
                    <button type="button" class="remove-btn" :disabled="cartStore.isLoading" @click.prevent="handleRemove(item.id)">🗑️</button>
                  </div>
                </template>

                <!-- CAS 3: PACKS -->
                <template v-else-if="item.packs">
                  <img :src="item.packs.picture || picture" :alt="item.packs.title" class="item-image">
                  <div class="item-details">
                    <h4 class="item-name">Pack : {{ item.packs.title }}</h4>
                    <p class="item-price">{{ Number(item.unit_price).toLocaleString('fr-FR') }} FCFA</p>
                    
                    <div class="quantity-controls">
                      <button type="button" class="qty-btn" :disabled="item.quantity <= 1 || cartStore.isLoading" @click.prevent="handleUpdateQuantity(item.packs.id, item.quantity - 1)">-</button>
                      <span class="quantity">{{ item.quantity }}</span>
                      <button type="button" class="qty-btn" :disabled="cartStore.isLoading" @click.prevent="handleUpdateQuantity(item.packs.id, item.quantity + 1)">+</button>
                    </div>
                  </div>
                  <!-- 🔥 CORRECTION : On remet item.id pour la suppression -->
                  <div class="item-total">
                    <span class="total-price">{{ Number(item.subtotal).toLocaleString('fr-FR') }} FCFA</span>
                    <button type="button" class="remove-btn" :disabled="cartStore.isLoading" @click.prevent="handleRemove(item.id)">🗑️</button>
                  </div>
                </template>
                
              </div>
            </div>
          </div>

          <div class="order-summary">
            <div class="summary-line"><span>Sous-total</span><span>{{ cartStore.formattedTotalPrice }} FCFA</span></div>
            
            <!-- 🔥 MODIFICATION : Liaison de la case à cocher avec v-model -->
            <div class="summary-line">
              <span>J'ai un code promo</span>
              <input type="checkbox" v-model="hasPromoCode" class="toggle" />
            </div>

            <!-- 🔥 NOUVEAU : L'espace qui apparaît quand la case est cochée -->
            <div v-if="hasPromoCode" class="promo-code-container">
              <input 
                type="text" 
                v-model="promoCode" 
                placeholder="Entrez votre code" 
                class="promo-input" 
              />
              <button 
                type="button" 
                class="promo-apply-btn" 
                @click="applyPromoCode"
              >
                Appliquer
              </button>
            </div>

            <div class="summary-line total"><span>Total</span><span class="final-price">{{ cartStore.formattedTotalPrice }} FCFA</span></div>
          </div>
        </template>
      </div>

      <div class="cart-footer flex justify-center items-center" v-if="!cartStore.isEmpty">
        <checkoutButton label="Commander" @handleClicked="proceedToCheckout" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { watch, onMounted, onUnmounted,ref } from 'vue';
import { useRouter } from '#app';
import { useCartStore } from '../../stores/cartStore';

import checkoutButton from '../buttons/checkoutButton.vue';
import placeholder from '@/assets/pictures/ContratChap/pexels-thirdman-5060819.jpg';

export default {

  name: 'CartModal',

  components: { checkoutButton },

  props: {
    isOpen: { type: Boolean, default: false }
  },

  emits: ['close'],

  setup(props, { emit }) {

    const router = useRouter();
    
    const cartStore = useCartStore();

    const picture = placeholder;

    const hasPromoCode = ref(false); 
    const promoCode = ref('');
    const applyPromoCode = async () => {
      if (!promoCode.value.trim()) return;
      
      console.log("Application du code promo :", promoCode.value);
      // Plus tard, tu pourras appeler ton store ici :
      // await cartStore.applyPromo(promoCode.value);
    };

    const closeModal = () => emit('close');

    const handleRemove = async (id: string) => {
      await cartStore.removeFromCart(id);
    };

    const handleUpdateQuantity = async (id: string, quantity: number) => {
      if (quantity < 1) return;
      await cartStore.updateQuantity(id, quantity);
    };

    const proceedToCheckout = () => {
      closeModal();
      router.push('/order/checkout');
    };

    // Bloc de gestion du scroll
    watch(() => props.isOpen, async (newValue) => {
      if (newValue) {
        document.body.classList.add('overflow-hidden');
        // 🔥 On lance la requête uniquement quand la modale passe à "true" (ouverte)
        await cartStore.fetchCart();
        console.log("Votre panier", cartStore.cart.items);
      } else {
        document.body.classList.remove('overflow-hidden');
      }
    });

    onMounted(async () => {
      await cartStore.fetchCart();
      console.log("Votre panier", cartStore.cart.items);
    });

    onUnmounted(() => document.body.classList.remove('overflow-hidden'));

    return {
      cartStore,
      picture,
      hasPromoCode,
      promoCode,
      applyPromoCode,
      closeModal,
      handleRemove,
      handleUpdateQuantity,
      proceedToCheckout,
    };
  }
}
</script>

<style scoped>
/* Overlay */

/* Header */
.cart-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

.drag-handle {
  width: 40px;
  height: 4px;
  background: #e0e0e0;
  border-radius: 2px;
  position: absolute;
  top: 8px;
  left: 50%;
  transform: translateX(-50%);
}

.cart-title h2 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 600;
  color: #1a1a1a;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.size-6 {
  width: 1.5rem;
  height: 1.5rem;
}

.item-count {
  color: #666;
  font-size: 0.9rem;
}

.close-icon {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  padding: 0.25rem;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

/* Corps du panier */
.cart-body {
  flex: 1;
  overflow-y: auto;
  padding: 0 1.5rem;
}

/* Panier vide */
.empty-cart {
  text-align: center;
  padding: 3rem 1rem;
  color: #666;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-cart h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.empty-cart p {
  margin: 0 0 1.5rem 0;
}

.continue-shopping {
  background: #007bff;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
}

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
  color: #007bff;
  font-weight: 600;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
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
}

.qty-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
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
  color: #007bff;
}

/* Footer */
.cart-footer {
  padding: 1.5rem;
  border-top: 1px solid #f0f0f0;
  background: white;
  width: 100%;
}

/* Scroll personnalisé */
.cart-body::-webkit-scrollbar {
  width: 4px;
}

.cart-body::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.cart-body::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

/* 🔥 NOUVEAU : Styles pour le code promo */
.promo-code-container {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
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
  border-color: #007bff;
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

.promo-apply-btn:hover {
  background: #333;
}

/* Petite animation d'apparition douce */
@keyframes slideDown {
  from { 
    opacity: 0; 
    transform: translateY(-10px); 
  }
  to { 
    opacity: 1; 
    transform: translateY(0); 
  }
}

</style>