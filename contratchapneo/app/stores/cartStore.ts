import { defineStore } from "pinia";
import { ref, computed } from "vue";

export interface CartItem{
  id: string | number;
  productId?: number;
  name: string;
  price: number;
  quantity: number;
  image?: string;
  maxStock?: number;
}