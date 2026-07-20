<template>
    <div class="cart-items">
      <div class="items-list">
        <div v-for="item in cartItems" :key="item.id" class="cart-item">
          <img :src="item.image || placeholder" :alt="item.name" class="item-image">
          <div class="item-details">
            <h4 class="item-name">{{ item.name }}</h4>
            <p class="item-price">{{ item.price }} FCFA</p>
            <div class="quantity-controls">
              <!-- Tu peux aussi utiliser v-if="!isCheckout" ici si tu veux bloquer le changement de quantité -->
              <button 
                type="button" 
                class="qty-btn" 
                @click.prevent="decrease(item.id, item.quantity)" 
                :disabled="item.quantity <= 1 || cartStore.isLoading"
              >-</button>
              
              <span class="quantity">{{ item.quantity }}</span>
              
              <button 
                type="button" 
                class="qty-btn" 
                @click.prevent="increase(item.id, item.quantity)"
                :disabled="cartStore.isLoading"
              >+</button>
            </div>
          </div>
          <div class="item-total">
              <span class="total-price">{{ (Number(item.price) * item.quantity).toLocaleString('fr-FR') }} FCFA</span>
              
              <!-- ⚡️ NOUVEAU : Le bouton n'apparaît que si on N'EST PAS dans le checkout -->
              <button 
                v-if="!isCheckout"
                type="button" 
                class="remove-btn" 
                :disabled="cartStore.isLoading" 
                @click.prevent="removeFromCart(item.cartItemId)"
              >🗑️</button>
          </div>
        </div>
      </div>

      <div class="order-summary">
          <div class="summary-line"><span>Sous-total</span><span>{{ formattedTotalPrice }} FCFA</span></div>
          <div class="summary-line"><span>J'ai un code promo</span><span>Gratuite</span></div>
          <div class="summary-line total"><span>Total</span><span class="final-price">{{ formattedTotalPrice }} FCFA</span></div>
      </div>
    </div>
</template>

<script lang="ts">
import { computed } from 'vue';
import { useCartStore } from '../../stores/cartStore';
import placeholder from '@/assets/pictures/ContratChap/pexels-thirdman-5060819.jpg';

export default {
  name: 'Itemslist',
  // ⚡️ NOUVEAU : Déclaration de la prop
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
        else if (i.packs) {
          itemName = `Pack : ${i.packs.title || i.packs.name || 'Inconnu'}`; 
          itemImage = i.packs.picture;
          targetId = i.packs.id; 
        }

        return {
          cartItemId: i.id,
          id: targetId,
          name: itemName,
          price: Number(i.unit_price || 0), 
          subtotal: Number(i.subtotal || 0), 
          quantity: i.quantity,
          image: itemImage
        };
      })
    ));

    const formattedTotalPrice = computed(() => cartStore.formattedTotalPrice);

    const removeFromCart = async (id: string) => {
      try {
        await cartStore.removeFromCart(id);
      } catch (e) {
        console.error("Erreur lors de la suppression:", e);
      }
    };

    const decrease = async (id: string, qty: number) => {
      if (qty <= 1) return;
      try {
        await cartStore.updateQuantity(id, qty - 1);
      } catch (e) {
        console.error("Erreur lors de la diminution:", e);
      }
    };

    const increase = async (id: string, qty: number) => {
      try {
        await cartStore.updateQuantity(id, qty + 1);
      } catch (e) {
        console.error("Erreur lors de l'augmentation:", e);
      }
    };

    return {
      cartStore,
      cartItems,
      formattedTotalPrice,
      removeFromCart,
      decrease,
      increase,
      placeholder,
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
</style>