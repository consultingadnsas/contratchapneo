import {useHead} from '#imports';
import { ref} from 'vue';
import { defineStore } from 'pinia';
import type {Order} from '../stores/orderStore'

/*
{
  "merchantId": "PP-F324",
  "amount": 1000,
  "description": "Abonnement Premium",
  "channel": "CARD",
  "countryCurrencyCode": "952",
  "referenceNumber": "REF-772105",
  "customerEmail": "test@gmail.com",
  "customerFirstName": "Ishola",
  "customerLastname": "Lamine",
  "customerPhoneNumber": "01234567",
  "notificationURL": "https://votre-site.com/webhook",
  "returnURL": "https://votre-site.com/retour",
  "returnContext": "{\"order_id\":\"123\", \"user\":\"88\"}"
}
*/

export interface Paiement {
    amount: number,
    channel: string,
    referenceNumber: string,
    customerEmail: string,
    customerFirstName: string,
    customerLastname: string,
    customerPhoneNumber: string,
    description: string,
    merchantId?: string,
    notificationURL?: string,
    returnURL?: string,
    returnContext?: string,
}

export const usePaiementStore = defineStore('paiement', ()=>{

    //
    const order = ref<Order | null>(null)

    const paiement = ref<Paiement | null>(null)

    const sandboxMode = ref(true)

    const setSandboxMode = (enabled: boolean) => {
        sandboxMode.value = enabled
    }

    return {
        order,
        paiement,
        sandboxMode,
        setSandboxMode,
    }
})