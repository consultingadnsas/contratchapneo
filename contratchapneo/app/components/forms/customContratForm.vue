<template>
    <baseNotification
        v-model:show="notify.show"
        :type="notify.type"
        :title="notify.title"
        :message="notify.message"
    />
    <form 
        class="custom-contract-form w-full flex flex-col gap-4"
        @submit.prevent="submitForm"
    >

        <h3> {{ formTitle }} </h3>

        <!-- ⚡️ CORRECTION : Utilisation de category et dynamicContractTypes -->
        <BaseSelect 
            id="custom-contract-type"
            label="Sélectionner votre catégorie de contrat"
            v-model="checkoutform.category"
            :options="dynamicContractTypes"
            placeholder="Choisissez une catégorie..."
            required
        />

        <!-- ⚡️ CORRECTION : Utilisation de full_name pour correspondre au backend -->
        <BaseInput 
            id="custom-name"
            label="Nom complet / nom de la société" 
            name="full_name" 
            type="text" 
            placeholder="Entrez votre nom ou raison sociale"
            v-model="checkoutform.full_name"
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

        <BaseInput 
            id="custom-subject"
            label="Sujet" 
            name="subject" 
            type="text" 
            placeholder="Entrez l'objet de votre demande (Ex: Rachat d'actions)"
            v-model="checkoutform.subject"
            required
        />

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

    </form>
</template>

<script>
// ⚡️ NOUVEAU : Import de onMounted et computed
import { ref, reactive, onMounted, computed } from 'vue' 
import BaseInput from '../input/BaseInput.vue'
import checkoutButton from '../buttons/checkoutButton.vue'
import BaseSelect from '../input/BaseSelect.vue'
import BaseArea from '../input/BaseArea.vue'
import BaseNotification from '../tools/baseNotification.vue' 

import { useCartStore } from '../../stores/cartStore'
import { useContratStore } from '../../stores/contratStore'

import { useRouter, useRoute } from 'vue-router'

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

    emits: ['success'], 
    setup(props, { emit }) {

        const router = useRouter();
        const route = useRoute();

        const cartStore = useCartStore();
        const contratStore = useContratStore();

        // ⚡️ NOUVEAU : On charge les catégories dynamiquement au montage du composant
        onMounted(async () => {
            // On évite de refaire l'appel si les catégories sont déjà dans le store
            if (contratStore.categories.length === 0) {
                await contratStore.getCategories();
            }
        });

        // ⚡️ NOUVEAU : On transforme la liste du backend pour qu'elle corresponde à ce qu'attend <BaseSelect>
        const dynamicContractTypes = computed(() => {
            return contratStore.categories.map(cat => ({
                value: cat.id,     // L'UUID à envoyer au backend
                name: cat.title    // Le texte affiché à l'utilisateur
            }));
        });

        // ⚡️ CORRECTION : Alignement strict des clés avec le Serializer Django
        const checkoutform = reactive({
            category: "",      // Remplacé contract_type par category
            full_name: "",     // Remplacé name par full_name
            email: "",
            phone_number: "",
            subject: "",
            description: ""
        })

        const loading = ref(false)

        const notify = ref({
            show: false,
            type: 'success',
            title: '',
            message: ''
        });

        const showNotification = (type, title, message = '') => {
            notify.value = { show: true, type, title, message };
        };

        const validateForm = () => {
            // ⚡️ CORRECTION DES VÉRIFICATIONS avec les nouvelles clés
            if (!checkoutform.category) {
                showNotification('error', 'Catégorie manquante', 'Veuillez sélectionner la catégorie de contrat.');
                return false;
            }
            if (!checkoutform.full_name.trim()) {
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
            const subject = checkoutform.subject.trim();
            if (!subject) {
                showNotification('error', 'Sujet manquant', "Veuillez préciser l'objet de votre demande.");
                return false;
            }
            const minSubjectLength = 2;
            const wordCounts = subject.split(/\s+/).filter(Boolean).length;
            if (wordCounts < minSubjectLength) {
                showNotification('error', 'Sujet trop court', `Le sujet doit contenir au moins ${minSubjectLength} mots.`);
                return false;
            }

            const desc = checkoutform.description.trim();
            if (!desc) {
                showNotification('error', 'Champs requis', 'Le message ou contexte est obligatoire.');
                return false;
            }
            const MIN_WORDS = 10;
            const wordCount = desc.split(/\s+/).filter(Boolean).length;
            if (wordCount < MIN_WORDS) {
                showNotification(
                    'error', 
                    'Détails insuffisants', 
                    `Veuillez donner plus de détails (${wordCount}/${MIN_WORDS} mots minimum requis pour que notre expert comprenne votre besoin).`
                );
                return false;
            }
            return true;
        }

        const submitForm = async () => {
            if (!validateForm()) return; 

            loading.value = true

            try {
                // On envoie le formulaire qui possède désormais "category" et "full_name"
                await contratStore.submitCustomContract(checkoutform);
                
                showNotification(
                    'success', 
                    'Demande envoyée !', 
                    'Nos experts analyseront votre besoin et vous contacteront sous 24h.'
                );
                
                emit('success')

                // Réinitialisation avec les bonnes clés
                Object.assign(checkoutform, {
                    category: "",
                    full_name: "",
                    email: "",
                    phone_number: "",
                    subject: "",
                    description: ""
                });

                router.push('/order/checkout');

            } catch (err) {
                showNotification('error', 'Erreur d\'envoi', 'Une erreur est survenue lors de la soumission de votre demande.');
            } finally {
                loading.value = false
            }
        }

        return {
            route,
            router,
            cartStore,
            contratStore,
            checkoutform,
            loading,
            submitForm,
            notify,
            dynamicContractTypes // ⚡️ NOUVEAU : On expose la liste générée au template
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