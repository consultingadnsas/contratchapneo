import {useHead} from '#imports';
import { ref} from 'vue';
import { defineStore } from 'pinia';

export interface Paiement {
    amount: number,
    channel: string,
    referenceNumber: string,
    customerEmail: string,
    customerFirstName: string,
    customerLastname: string,
    customerPhoneNumber: string,
    description: string
}

export const usePaiementStore = defineStore('paiement', ()=>{

    
    const paiement = ref<Paiement>({
        amount: 0,
        channel: '',
        referenceNumber: '',
        customerEmail: '',
        customerFirstName: '',
        customerLastname: '',
        customerPhoneNumber: '',
        description: ''

    })

    return {
        paiement,
    }
})