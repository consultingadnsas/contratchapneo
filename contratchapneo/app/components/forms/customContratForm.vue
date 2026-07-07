<template>
    <form 
        class="custom-contract-form w-full flex flex-col gap-4"
        @submit.prevent="submitForm"
    >
        <h3>{{ formTitle }}</h3>

        <!-- Ajout du v-model et des bonnes options -->
        <BaseSelect 
            id="custom-contract-type"
            label="Sélectionner votre type de contrat"
            v-model="checkoutform.contract_type"
            :options="contractTypes"
            placeholder="Choisissez une option..."
            required
        />

        <BaseInput 
            id="custom-name"
            label="Nom complet / nom de la société" 
            name="name" 
            type="text" 
            placeholder="Entrez votre nom ou raison sociale"
            v-model="checkoutform.name"
            required
        />

        <BaseInput 
            id="custom-phone"
            label="Numéro de téléphone" 
            name="phoneNumber" 
            type="tel" 
            placeholder="Entrez votre numéro de téléphone"
            v-model="checkoutform.phone_number"
            required
        />

        <BaseInput 
            id="custom-email"
            label="Email" 
            name="email" 
            type="email" 
            placeholder="Entrez votre adresse email"
            v-model="checkoutform.email"
            required
        />

        <!-- Correction du name et du v-model -->
        <BaseInput 
            id="custom-subject"
            label="Sujet" 
            name="subject" 
            type="text" 
            placeholder="Entrez l'objet de votre demande"
            v-model="checkoutform.subject"
            required
        />

        <!-- Ajout du v-model -->
        <BaseArea 
            id="custom-description"
            label="Description détaillée"
            placeholder="Expliquez-nous votre besoin spécifique..."
            v-model="checkoutform.description"
            rows="5"
            required
        />

        <checkoutButton 
            label="Soumettre la demande" 
            type="submit"
            :isLoading="loading"
        />

       <ClientOnly>
            <Teleport to="body">
                <BaseNotification 
                    v-model:show="notify.show"
                    :type="notify.type"
                    :title="notify.title"
                    :message="notify.message"
                />
            </Teleport>
        </ClientOnly>
    </form>
</template>

<script>
import { ref, reactive } from 'vue'
import BaseInput from '../input/BaseInput.vue'
import checkoutButton from '../buttons/checkoutButton.vue'
import BaseSelect from '../input/BaseSelect.vue'
import BaseArea from '../input/BaseArea.vue'
import BaseNotification from '../tools/baseNotification.vue' // Attention à la majuscule si ton fichier l'exige

export default {
    components: {
        BaseInput,
        checkoutButton,
        BaseSelect,
        BaseArea,
        BaseNotification
    },
    props: {
        formTitle: {
            type: String,
            default: 'Mon contrat sur-mesure'
        }
    },
    emits: ['success'], // Correction orthographique (2 's')
    
    setup(props, { emit }) {

        // 1. Déclaration de toutes les variables nécessaires au backend
        const checkoutform = reactive({
            contract_type: "",
            name: "",
            email: "",
            phone_number: "",
            subject: "",
            description: ""
        })

        const loading = ref(false)

        // 2. Gestion de la notification
        const notify = ref({
            show: false,
            type: 'success',
            title: '',
            message: ''
        });

        const showNotification = (type, title, message = '') => {
            notify.value = { show: true, type, title, message };
        };

        // 3. Options adaptées pour un contrat sur-mesure
        const contractTypes = [
            { value: "prestation", name: "Contrat de prestation de services" },
            { value: "travail", name: "Contrat de travail" },
            { value: "partenariat", name: "Contrat de partenariat" },
            { value: "cession", name: "Contrat de cession" },
            { value: "autre", name: "Autre besoin spécifique" }
        ]

        // 4. Fonction de validation
        const validateForm = () => {
            if (!checkoutform.contract_type) {
                showNotification('error', 'Type manquant', 'Veuillez sélectionner le type de contrat.');
                return false;
            }
            if (!checkoutform.name.trim()) {
                showNotification('error', 'Nom manquant', 'Votre nom complet ou raison sociale est requis.');
                return false;
            }
            if (!checkoutform.phone_number.trim()) {
                showNotification('error', 'Téléphone manquant', 'Votre numéro de téléphone est requis.');
                return false;
            }
            if (!checkoutform.email.trim() || !/\S+@\S+\.\S+/.test(checkoutform.email)) {
                showNotification('error', 'Email invalide', 'Veuillez entrer une adresse email valide.');
                return false;
            }
            if (!checkoutform.subject.trim()) {
                showNotification('error', 'Sujet manquant', "Veuillez préciser l'objet de votre demande.");
                return false;
            }
            if (!checkoutform.description.trim()) {
                showNotification('error', 'Description manquante', 'Veuillez détailler votre besoin dans la description.');
                return false;
            }
            return true;
        }

        // 5. Soumission sécurisée
        const submitForm = async () => {
            if (!validateForm()) return; // On stoppe si la validation échoue

            loading.value = true

            try {
                // Simulation d'un appel API
                await new Promise((resolve) => setTimeout(() => resolve({ success: true }), 1500))
                
                // Affichage du succès
                showNotification('success', 'Demande envoyée !', 'Nos experts analyseront votre besoin et vous contacteront sous 24h.');
                
                emit('success')

                // Réinitialisation de l'objet form
                Object.assign(checkoutform, {
                    contract_type: "",
                    name: "",
                    email: "",
                    phone_number: "",
                    subject: "",
                    description: ""
                });

            } catch (err) {
                showNotification('error', 'Erreur d\'envoi', 'Une erreur est survenue lors de la soumission de votre demande.');
                console.error("Échec de la soumission :", err)
            } finally {
                loading.value = false
            }
        }

        return {
            checkoutform,
            loading,
            submitForm,
            notify,
            contractTypes
        }
    }
}
</script>

<style scoped>
.custom-contract-form {
    background: #ffffff;
    border-radius: 12px;
    min-width: 80%;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    display: flex;
    margin: 2rem;
    flex-direction: column;
    gap: 1rem;
}

.custom-contract-form h3 {
    color: #1e293b;
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
}
</style>