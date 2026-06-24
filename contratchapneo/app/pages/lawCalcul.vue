<template>
    <section class="calculator-section">
        <navbar/>
        <div class="calculator-header">
            <h1>Simulateur d'Indemnités</h1>
            <p>Calculez vos droits de fin de contrat (licenciement ou fin de CDD) conformément au Code du Travail de Côte d'Ivoire.</p>
        </div>

        <div class="form-wrapper">
            <form @submit.prevent="handleCalculate" class="calc-form">
                
                <!-- Type de contrat -->
                <BaseSelect
                    v-model="formData.contractType"
                    id="contractType"
                    label="Type de Contrat"
                    :options="contractOptions"
                    required
                />

                <!-- Affichage dynamique si CDI -->
                <template v-if="formData.contractType === 'cdi'">
                    <BaseSelect
                        v-model="formData.motif"
                        id="motif"
                        label="Motif de la rupture"
                        :options="motifOptions"
                        required
                    />

                    <!-- Si ce n'est pas une démission ou une faute lourde, on demande les dates et le salaire -->
                    <template v-if="formData.motif === 'licenciement'">
                        <div class="date-group">
                            <BaseInput
                                v-model="formData.startDate"
                                id="startDate"
                                type="date"
                                label="Date d'embauche"
                                required
                            />
                            <BaseInput
                                v-model="formData.endDate"
                                id="endDate"
                                type="date"
                                label="Date de fin de contrat"
                                required
                            />
                        </div>

                        <BaseInput
                            v-model="formData.averageSalary"
                            id="averageSalary"
                            type="number"
                            min="0"
                            label="Salaire mensuel moyen (12 derniers mois) en FCFA"
                            placeholder="Ex: 250000"
                            required
                        />
                    </template>
                </template>

                <!-- Affichage dynamique si CDD -->
                <template v-if="formData.contractType === 'cdd'">
                    <BaseInput
                        v-model="formData.totalGrossSalary"
                        id="totalGrossSalary"
                        type="number"
                        min="0"
                        label="Rémunération totale brute perçue (sur tout le contrat) en FCFA"
                        placeholder="Ex: 3000000"
                        required
                    />
                </template>

                <!-- Message d'erreur -->
                <div v-if="errorMessage" class="alert error">{{ errorMessage }}</div>

                <!-- Bouton de calcul -->
                <main-button 
                    label="Calculer mes droits"
                    :isLoading="isCalculating"
                    type="submit"
                    class="submit-btn"
                />
            </form>

            <!-- ── RÉSULTAT DU CALCUL ── -->
            <div v-if="hasCalculated" class="result-box" :class="{ 'is-zero': resultAmount === 0 }">
                <h3>Montant estimé de l'indemnité :</h3>
                <div class="amount">{{ formattedAmount }}</div>
                <p class="details">{{ calculationDetails }}</p>
                <small class="disclaimer">
                    * Cette simulation est donnée à titre indicatif selon les règles générales de la CCI de 1977. Elle ne remplace pas une consultation juridique, n'inclut pas les congés payés restants ni les éventuels dommages et intérêts.
                </small>
            </div>
        </div>
    </section>
</template>

<script lang="ts">
import { ref, computed, defineComponent } from 'vue';
import BaseInput from '../components/input/BaseInput.vue';
import BaseSelect from '../components/input/BaseSelect.vue';
import mainButton from '../components/buttons/mainButton.vue';
import navbar from '../components/navigation/navbar.vue';

export default defineComponent({
    name: 'LawCalculPage',
    components: {
        BaseInput,
        BaseSelect,
        mainButton,
        navbar
    },
    setup() {
        // Options pour les menus déroulants
        const contractOptions = [
            { name: "Contrat à Durée Indéterminée (CDI)", value: "cdi" },
            { name: "Contrat à Durée Déterminée (CDD)", value: "cdd" }
        ];

        const motifOptions = [
            { name: "Licenciement (Économique / Personnel)", value: "licenciement" },
            { name: "Démission", value: "demission" },
            { name: "Licenciement pour Faute Lourde", value: "faute" }
        ];

        // État du formulaire
        const formData = ref({
            contractType: 'cdi',
            motif: 'licenciement',
            startDate: '',
            endDate: '',
            averageSalary: '',
            totalGrossSalary: ''
        });

        // État des résultats
        const isCalculating = ref(false);
        const hasCalculated = ref(false);
        const resultAmount = ref(0);
        const calculationDetails = ref('');
        const errorMessage = ref('');

        // Formatage de la monnaie
        const formattedAmount = computed(() => {
            return new Intl.NumberFormat('fr-FR').format(Math.round(resultAmount.value)) + ' FCFA';
        });

        const handleCalculate = async () => {
            isCalculating.value = true;
            errorMessage.value = '';
            hasCalculated.value = false;

            // Petit effet de chargement pour l'UX
            await new Promise(resolve => setTimeout(resolve, 600));

            try {
                // ── LOGIQUE CDI ──
                if (formData.value.contractType === 'cdi') {
                    if (formData.value.motif === 'demission' || formData.value.motif === 'faute') {
                        resultAmount.value = 0;
                        calculationDetails.value = "Aucune indemnité de licenciement n'est légalement due en cas de démission ou de licenciement pour faute lourde.";
                        hasCalculated.value = true;
                        return;
                    }

                    // Calcul de l'ancienneté
                    const start = new Date(formData.value.startDate);
                    const end = new Date(formData.value.endDate);

                    if (end <= start) {
                        errorMessage.value = "La date de fin doit être postérieure à la date d'embauche.";
                        return;
                    }

                    // Calcul précis en mois puis en années
                    const diffMonths = (end.getFullYear() - start.getFullYear()) * 12 
                                     + (end.getMonth() - start.getMonth()) 
                                     + (end.getDate() - start.getDate()) / 30.416; // 30.416 = moyenne jours/mois
                    
                    const yearsOfSeniority = diffMonths / 12;

                    if (yearsOfSeniority < 1) {
                        resultAmount.value = 0;
                        calculationDetails.value = `Votre ancienneté est de ${(yearsOfSeniority * 12).toFixed(1)} mois. Il faut au minimum 1 an (12 mois) continu dans l'entreprise pour avoir droit à l'indemnité de licenciement.`;
                        hasCalculated.value = true;
                        return;
                    }

                    // Application du barème CCI 1977
                    const salary = Number(formData.value.averageSalary);
                    let tranche1 = 0; // 1 à 5 ans : 30%
                    let tranche2 = 0; // 6 à 10 ans : 35%
                    let tranche3 = 0; // Au-delà de 10 ans : 40%

                    tranche1 = Math.min(yearsOfSeniority, 5) * 0.30 * salary;
                    if (yearsOfSeniority > 5) {
                        tranche2 = Math.min(yearsOfSeniority - 5, 5) * 0.35 * salary;
                    }
                    if (yearsOfSeniority > 10) {
                        tranche3 = (yearsOfSeniority - 10) * 0.40 * salary;
                    }

                    resultAmount.value = tranche1 + tranche2 + tranche3;
                    calculationDetails.value = `Calcul effectué sur une ancienneté de ${yearsOfSeniority.toFixed(2)} ans. Barème appliqué : 30% jusqu'à 5 ans, 35% de 6 à 10 ans, et 40% au-delà.`;
                } 
                // ── LOGIQUE CDD ──
                else if (formData.value.contractType === 'cdd') {
                    const totalGross = Number(formData.value.totalGrossSalary);
                    if (totalGross <= 0) {
                        errorMessage.value = "Veuillez entrer un montant valide.";
                        return;
                    }

                    // L'indemnité de précarité est de 3% de la rémunération totale brute
                    resultAmount.value = totalGross * 0.03;
                    calculationDetails.value = "L'indemnité de fin de contrat (prime de précarité) correspond légalement à 3% du montant global des salaires bruts perçus pendant la durée du CDD.";
                }

                hasCalculated.value = true;

            } catch (error) {
                errorMessage.value = "Une erreur est survenue lors du calcul.";
            } finally {
                isCalculating.value = false;
            }
        };

        return {
            formData,
            contractOptions,
            motifOptions,
            isCalculating,
            hasCalculated,
            resultAmount,
            formattedAmount,
            calculationDetails,
            errorMessage,
            handleCalculate
        };
    }
});
</script>

<style scoped>
/* ── Container Principal ── */
.calculator-section {
    position: relative;
    width: 100%;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 8rem 1rem 4rem 1rem;
    background: radial-gradient(circle, #202b4a 30%, #0f0f0f 100%);
    color: var(--my-white, #ffffff);
    overflow-x: hidden;
}

.calculator-header {
    text-align: center;
    max-width: 600px;
    margin-bottom: 3rem;
    z-index: 2;
}

.calculator-header h1 {
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 700;
    margin-bottom: 1rem;
    color: #ffffff;
}

.calculator-header p {
    font-size: clamp(1rem, 2vw, 1.15rem);
    color: #a0aec0;
    line-height: 1.6;
}

/* ── Conteneur du formulaire (Glassmorphism) ── */
.form-wrapper {
    width: 100%;
    max-width: 650px;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    z-index: 2;
}

.calc-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.date-group {
    display: flex;
    gap: 1rem;
    width: 100%;
}

/* ── SURCHARGE DES COMPOSANTS BASE (Glassmorphism) ── */
:deep(.form-input),
:deep(.form-select) {
    background-color: rgba(0, 0, 0, 0.2) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
}

:deep(.form-input:focus),
:deep(.form-select:focus) {
    border-color: #32f459 !important;
    box-shadow: 0 0 0 3px rgba(50, 244, 89, 0.1) !important;
    background-color: rgba(0, 0, 0, 0.3) !important;
}

:deep(.input-label) {
    color: #e2e8f0 !important;
    margin-left: 0.2rem !important;
    font-size: 0.95rem !important;
}

:deep(.form-select) {
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23ffffff' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e") !important;
}

/* ── Bouton ── */
.submit-btn {
    width: 100%;
    padding: 1.1rem;
    border-radius: 12px;
    font-size: 1.05rem;
    font-weight: 700;
    margin-top: 1rem;
    transition: all 0.3s ease;
}

.submit-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(50, 244, 89, 0.2);
}

/* ── RÉSULTAT DU CALCUL ── */
.result-box {
    margin-top: 2.5rem;
    padding: 2rem;
    background: rgba(50, 244, 89, 0.05);
    border: 1px solid rgba(50, 244, 89, 0.3);
    border-radius: 16px;
    text-align: center;
    animation: fadeIn 0.5s ease-out;
}

.result-box.is-zero {
    background: rgba(239, 68, 68, 0.05);
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.result-box h3 {
    font-size: 1.1rem;
    color: #e2e8f0;
    margin-bottom: 0.5rem;
    font-weight: 500;
}

.result-box .amount {
    font-size: 2.5rem;
    font-weight: 800;
    color: #32f459;
    margin-bottom: 1rem;
    text-shadow: 0 0 20px rgba(50, 244, 89, 0.3);
}

.result-box.is-zero .amount {
    color: #fca5a5;
    text-shadow: none;
}

.result-box .details {
    font-size: 0.95rem;
    color: #a0aec0;
    line-height: 1.5;
    margin-bottom: 1.5rem;
}

.result-box .disclaimer {
    display: block;
    font-size: 0.75rem;
    color: #718096;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 1rem;
}

/* ── Alertes ── */
.alert {
    padding: 1rem;
    border-radius: 10px;
    font-size: 0.95rem;
    font-weight: 500;
    text-align: center;
}
.alert.error {
    background: rgba(239, 68, 68, 0.1);
    color: #fca5a5;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

/* ── Animations et Décors ── */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.bg-shape {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    z-index: 1;
    opacity: 0.5;
}
.shape-top-left {
    top: -10%;
    left: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, #32f459 0%, transparent 70%);
}
.shape-bottom-right {
    bottom: -10%;
    right: -10%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, #068cec 0%, transparent 70%);
}

/* ── Responsive Mobile ── */
@media (max-width: 768px) {
    .calculator-section { padding: 6rem 1rem 3rem 1rem; }
    .form-wrapper { padding: 1.5rem; }
    .date-group { flex-direction: column; gap: 0; }
    .result-box .amount { font-size: 2rem; }
}
</style>