<template>
    <div class="main-wrapper">
        
        <!-- 
        <aside class="form-section">
            <h2 class="form-title">📝 Remplir le contrat</h2>
            <p class="form-subtitle">Vos modifications s'affichent en temps réel sur le document.</p>

            <div class="input-group">
                <label for="clientName">Nom Complet / Raison sociale</label>
                <input 
                    id="clientName" 
                    v-model="contractData.nom_client" 
                    type="text" 
                    placeholder="Ex: Jean Dupont" 
                />
            </div>

            <div class="input-group">
                <label for="clientAddress">Adresse complète</label>
                <input 
                    id="clientAddress" 
                    v-model="contractData.adresse" 
                    type="text" 
                    placeholder="Ex: Abidjan, Cocody Riviera 2" 
                />
            </div>

            <div class="input-group">
                <label for="contractDate">Date d'effet</label>
                <input 
                    id="contractDate" 
                    v-model="contractData.date_contrat" 
                    type="date" 
                />
            </div>

            <div class="input-group">
                <label for="amount">Montant de la prestation (FCFA)</label>
                <input 
                    id="amount" 
                    v-model="contractData.montant" 
                    type="number" 
                    placeholder="Ex: 500000" 
                />
            </div>

            <button class="submit-btn" @click="submitToBackend">
                ✅ Valider et Payer
            </button>
        </aside>
        -->

        <contract-generator-form/>
        

        <main class="preview-section">
            <div class="a4-document">
                <h1 class="doc-title">CONTRAT DE PRESTATION DE SERVICES</h1>
                
                <p class="doc-paragraph">Entre les soussignés :</p>
                
                <p class="doc-paragraph">
                    La société <strong>Contratchap SAS</strong>, représentée par son gérant, d'une part,
                </p>
                
                <p class="doc-paragraph">
                    Et M./Mme/La société <span class="dynamic-data">{{ contractData.nom_client || '[Nom du client]' }}</span>, 
                    résidant à <span class="dynamic-data">{{ contractData.adresse || '[Adresse du client]' }}</span>, 
                    ci-après dénommé(e) "Le Client", d'autre part.
                </p>

                <p class="doc-paragraph">
                    Il a été convenu ce qui suit, à compter du <span class="dynamic-data">{{ formattedDate || '[Date de début]' }}</span> :
                </p>

                <h3 class="doc-subtitle">Article 1 : Objet</h3>
                <p class="doc-paragraph">
                    Le présent contrat a pour objet la fourniture de services juridiques. 
                    Le client s'engage à verser la somme de <span class="dynamic-data">{{ contractData.montant ? contractData.montant + ' FCFA' : '[Montant]' }}</span> 
                    pour l'exécution de cette prestation.
                </p>

                <div class="signatures">
                    <div class="sign-box">
                        <p>Pour le Prestataire</p>
                        <div class="sign-space"></div>
                    </div>
                    <div class="sign-box">
                        <p>Pour le Client</p>
                        <div class="sign-space"></div>
                    </div>
                </div>
            </div>
        </main>

    </div>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue';
import contractGeneratorForm from '../../components/forms/contractGeneratorForm.vue'

// 1. Définition des données réactives (Ce qui sera envoyé au format JSON)
const contractData = reactive({
    nom_client: '',
    adresse: '',
    date_contrat: '',
    montant: ''
});

// 2. Computed property pour formater joliment la date sur le faux document
const formattedDate = computed(() => {
    if (!contractData.date_contrat) return '';
    const dateObj = new Date(contractData.date_contrat);
    return dateObj.toLocaleDateString('fr-FR', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
});

// 3. Fonction soumission au backend
const submitToBackend = () => {
    // C'est ce payload JSON propre que ton backend Django va recevoir pour utiliser docxtpl !
    const payload = {
        contrat_id: "id-du-modele-en-base", // À récupérer dynamiquement (ex: via props ou store)
        data: { ...contractData }
    };
    
    console.log("🚀 Envoi au backend (JSON pur) :", payload);
    
    // Ici, tu appelleras ton API, ex :
    // await $api.post('/payment/initiate/', payload);
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