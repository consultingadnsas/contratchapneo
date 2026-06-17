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

    const {$api} = useNuxtApp();

    const isLoading = ref(false);
    const error = ref<string | null>(null);

    //
    const order = ref<Order | null>(null)

    const paiement = ref<Paiement | null>(null)

    const sandboxMode = ref(true)

    const setSandboxMode = (enabled: boolean) => {
        sandboxMode.value = enabled
    }

    // State

    const downloadContracts = async(orderId:string)=>{

        isLoading.value = true;
        error.value = null;

        try{
            const config = useRuntimeConfig()
            const baseURL = config.public.apiBase || window.location.origin
            const downloadUrl = `${baseURL}/payment/download/${orderId}`

            const response = await window.fetch(downloadUrl, {
                method: 'GET',
                credentials: 'include',
            })

            if (!response.ok) {
                throw new Error(`Erreur de téléchargement : ${response.status}`)
            }

            const blob = await response.blob()
            const disposition = response.headers.get('Content-Disposition') || ''
            const filenameMatch = disposition.match(/filename="?(.*?)"?$/)
            const filename = filenameMatch?.[1] || `contrat-${orderId}.pdf`

            const url = URL.createObjectURL(blob)
            const anchor = document.createElement('a')
            anchor.href = url
            anchor.download = filename
            document.body.appendChild(anchor)
            anchor.click()
            document.body.removeChild(anchor)
            URL.revokeObjectURL(url)

            return true
        } catch(err:any) {
            error.value = err.message ?? String(err)
            console.error("erreur interceptée", error.value)
            return false
        } finally {
            isLoading.value = false
        }

    }

    return {
        isLoading,
        error,
        order,
        paiement,
        sandboxMode,
        setSandboxMode,
        downloadContracts
    }
})