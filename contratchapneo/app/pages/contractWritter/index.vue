<template>
    <div class="main-wrapper flex h-screen w-full overflow-hidden bg-gray-200">
        
        <aside class="form-section w-1/3 h-full p-6 overflow-y-auto bg-white shadow-2xl z-10 relative">
            <contract-generator-form 
                @update-data="syncData"
                @submit-data="handleModale" 
            />
        </aside>

        <div class="preview-section w-2/3 h-full p-8 overflow-y-auto flex justify-center items-start">
            <contratPreviewPage ref="previewRef" />
        </div>

        <confirmModale 
            :isOpen="isOpen"
            @close="isOpen = false" 
            @confirm="submitToBackend" 
        />
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import contractGeneratorForm from '../../components/forms/contractGeneratorForm.vue';
import contratPreviewPage from '../../components/tools/contratPreviewPage.vue';
import confirmModale from '../../components/modale/confirmModale.vue';

import { useContratStore } from '../../stores/contratStore';
import { usePaiementStore } from '../../stores/paiementStore';

const router = useRouter();

const contratStore = useContratStore();
const paiementStore = usePaiementStore();

const previewRef = ref<InstanceType<typeof contratPreviewPage> | null>(null);

const isOpen = ref<boolean>(false);
const formDataToSubmit = ref<Record<string, any>>({}); 

// 2. Le formulaire a émis les données, on les stocke et on ouvre la modale
const handleModale = (data: Record<string, any>) => {
    formDataToSubmit.value = data; 
    isOpen.value = true;           
};

// Fonction de mise à jour en temps réel sur le document A4
const syncData = (newData: Record<string, any>) => {
    if (previewRef.value) {
        previewRef.value.syncData(newData);
    }
};

// 3. L'utilisateur a cliqué sur "Valider" dans la modale
// 3. L'utilisateur a cliqué sur "Valider" dans la modale
const submitToBackend = async () => {
    
    console.log("Données transmises au Store :", formDataToSubmit.value);

    // 🔥 LA CORRECTION EST ICI : Injection manuelle de l'email
    if (typeof window !== 'undefined') {
        // 1. On tente d'extraire l'email des données que l'utilisateur vient de saisir
        // (Vérifie le nom exact du champ email de ton form : 'email', 'courriel', etc.)
        const formEmail = formDataToSubmit.value.email || formDataToSubmit.value.guest_email;

        // 2. S'il y a un email, on le grave dans le localStorage pour le paiementStore
        if (formEmail) {
            localStorage.setItem('backup_checkout_email', formEmail);
            console.log("💉 Email sécurisé depuis le formulaire :", formEmail);
        }
    }

    try {
        const result = await paiementStore.generateContract(
            formDataToSubmit.value,
            contratStore.currentContratId || undefined
        );

        if(result && result.ok){ // ⚠️ Ajout de result.ok pour être plus précis
            router.push('/contractWritter/contractGenerator');
        }

        if (!result?.ok) {
            throw new Error(result?.error || 'L\'enregistrement des données a échoué.');
        }

        isOpen.value = false;
    } catch (err: any) {
        console.error('Une erreur est survenue lors de l\'enregistrement des données', err);
    }
};
</script>

<style scoped>
/* =========================================
   MISE EN PAGE GLOBALE (RESPONSIVE)
   ========================================= */
.main-wrapper {
    display: flex;
    flex-direction: column; /* Sur mobile : on empile */
    gap: 2rem;
    padding: 1rem;
    max-width: 1400px;
    margin: 0 auto;
    background-color: #f4f6f9; /* Petit fond gris léger pour contraster avec la page A4 */
    min-height: 100vh;
}

/* Écrans de tablette et PC : on met côte à côte */
@media (min-width: 992px) {
    .main-wrapper {
        flex-direction: row;
        align-items: flex-start;
        padding: 2rem;
    }
}

/* =========================================
   FORMULAIRE (Gauché/Haut)
   ========================================= */
.form-section {
    flex: 1;
    background: #ffffff;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    position: sticky; /* Reste visible quand on scroll le document sur PC */
    top: 2rem;
}

.form-title {
    font-size: 1.5rem;
    color: #202b4a; /* Bleu Contratchap */
    margin-bottom: 0.5rem;
}

.form-subtitle {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 2rem;
}

.input-group {
    margin-bottom: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.input-group label {
    font-weight: 600;
    font-size: 0.95rem;
    color: #333;
}

.input-group input {
    padding: 0.8rem 1rem;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.2s;
}

.input-group input:focus {
    outline: none;
    border-color: #202b4a;
}

.submit-btn {
    width: 100%;
    padding: 1rem;
    background-color: #202b4a;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    font-weight: bold;
    cursor: pointer;
    margin-top: 1rem;
    transition: background-color 0.2s, transform 0.1s;
}

.submit-btn:hover {
    background-color: #2c3a61;
}
.submit-btn:active {
    transform: scale(0.98);
}

/* =========================================
   FAUX DOCUMENT A4 (Droite/Bas)
   ========================================= */
.preview-section {
    flex: 2; /* Prend deux fois plus de place que le formulaire sur PC */
    display: flex;
    justify-content: center;
    overflow-x: auto; /* Permet de scroller horizontalement sur mobile si nécessaire */
}

.a4-document {
    background: #ffffff;
    width: 100%;
    max-width: 210mm; /* Largeur exacte d'un A4 */
    min-height: 297mm; /* Hauteur exacte d'un A4 */
    padding: 12% 10%; /* Marges intérieures typiques d'un Word */
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    border: 1px solid #e5e7eb;
    
    /* Typographie juridique */
    font-family: 'Times New Roman', Times, serif;
    color: #000000;
    line-height: 1.6;
}

/* Style des textes remplis dynamiquement */
.dynamic-data {
    color: #1a56db; /* Bleu pour montrer que c'est une variable */
    background-color: rgba(26, 86, 219, 0.05); /* Surlignage très léger */
    padding: 0 4px;
    border-radius: 2px;
}

.doc-title {
    text-align: center;
    font-size: 1.4rem;
    text-decoration: underline;
    margin-bottom: 3rem;
    text-transform: uppercase;
}

.doc-subtitle {
    margin-top: 2rem;
    margin-bottom: 1rem;
    font-size: 1.1rem;
    text-decoration: underline;
}

.doc-paragraph {
    margin-bottom: 1.2rem;
    text-align: justify;
}

.signatures {
    display: flex;
    justify-content: space-between;
    margin-top: 5rem;
}

.sign-box {
    width: 40%;
}

.sign-box p {
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.sign-space {
    border-top: 1px dotted #000;
    height: 100px;
    margin-top: 3rem;
}
</style>