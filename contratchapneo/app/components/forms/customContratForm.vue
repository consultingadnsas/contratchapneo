<template>
    <form 
        class="w-full flex flex-col gap-2"
        @submit.prevent="submitForm"
    >

        <h3>{{ formTitle }}</h3>

        <BaseSelect 
            label="Selectionner votre type de contrat"
            
        />

        <BaseInput 
            label="Nom complet / nom société" 
            name="name" 
            type="text" 
            placeholder="Entrez votre Nom complet / nom société"
            v-model="checkoutform.name"
        />

        <BaseInput 
            label="Numéro de téléphone" 
            name="phoneNumber" 
            type="tel" 
            placeholder="Entrez votre numéro de téléphone"
            v-model="checkoutform.phone_number"
        />

        <BaseInput 
            label="Email" 
            name="email" 
            type="email" 
            placeholder="Entrez votre adresse email"
            v-model="checkoutform.email"
        />

        <BaseInput 
            label="Sujet" 
            name="email" 
            type="text" 
            placeholder="Entrez l'objet de votre contrat"
            v-model="checkoutform.email"
        />

        <BaseArea label="Description"/>

        <checkoutButton 
            label="Soumettre" 
            type="submit"
            :isLoading="loading"
        />
    </form>
</template>

<script>
import BaseInput from '../input/BaseInput.vue'
import checkoutButton from '../buttons/checkoutButton.vue'
import BaseSelect from '../input/BaseSelect.vue'
import BaseArea from '../input/BaseArea.vue'
import {ref, reactive} from 'vue'

export default {
    components:{
        BaseInput,
        checkoutButton,
        BaseSelect,
        BaseArea
    },
    props:{
        formTitle:{
            type:String,
            default: 'Mon contrat sur mesure'
        }
    },

    emits:['succes'],
    setup(props, {emit}){

        const checkoutform = reactive(
            {
                name:"",
                email: "",
                phone_number:""
            }
        )

        const loading = ref(false)
        
        const error = ref(null)

        const optionpayment =[
            { options: "Wave" },
            { options: "Orange Money" },
            { options: "Moov Money" }
        ]

        const submitForm = async () => {
            loading.value = true
            error.value = null

            try {
                // Simulation d'un appel API (ex: POST /api/checkout)
                await new Promise((resolve, reject) => {
                setTimeout(() => {
                    // Simuler une réussite ou une erreur aléatoire
                    Math.random() > 0.2 ? resolve({ success: true }) : reject("Erreur serveur")
                }, 1500)
                })
                
                emit('succes')

                checkoutform.name = "";
                checkoutform.email = "";
                checkoutform.phone_number = "";
            } catch (err) {
                error.value = err
                console.error("Échec de la soumission :", err)
            } finally {
                loading.value = false
            }
        }

        return{
            checkoutform,
            loading,
            error,
            submitForm
        }

    }
}
</script>

<style>

</style>