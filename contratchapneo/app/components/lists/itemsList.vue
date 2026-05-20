<template>
    <div class="cart-items">
        <div class="items-list">
            <div v-for="item in cartItems" :key="item.id" class="cart-item">
            <img src="../../assets/pictures/ContratChap/black-person-signing-job-contract.jpg" :alt="item.name" class="item-image">
            <div class="item-details">
                <h4 class="item-name">{{ item.name }}</h4>
                <p class="item-price">{{ item.price }} FCFA</p>
                <div class="quantity-controls">
                <button class="qty-btn" @click="item.quantity--" :disabled="item.quantity <= 1">-</button>
                <span class="quantity">{{ item.quantity }}</span>
                <button class="qty-btn" @click="item.quantity++">+</button>
                </div>
            </div>
            <div class="item-total">
                <span class="total-price">{{ (item.price * item.quantity) }} FCFA</span>
                <button class="remove-btn" @click="removeFromCart(item.id)">🗑️</button>
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
import { ref, watch, onUnmounted, computed } from 'vue';
export default {
  name: 'Itemslist',
  setup(){
    const cartItems = ref([
      { id: 1, name: "Contrat de travail CDD", price: 5000, quantity: 1, image: '../../assets/pictures/ContratChap/pexels-thirdman-5060819.jpg'},
      { id: 2, name: "Contrat de prestation", price: 8000, quantity: 1, image: '../../assets/pictures/ContratChap/pexels-thirdman-5060819.jpg' }
    ]);

    const isEmpty = computed(() => cartItems.value.length === 0);
    const totalItems = computed(() => cartItems.value.reduce((acc, item) => acc + item.quantity, 0));
    const formattedTotalPrice = computed(() => 
      cartItems.value.reduce((acc, item) => acc + (item.price * item.quantity), 0).toLocaleString()
    );

    return {
      cartItems,
      isEmpty,
      totalItems,
      formattedTotalPrice
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
</style>