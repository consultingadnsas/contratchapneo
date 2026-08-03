<template>
    <section class="calculator-section">
        <navbar />

        <div class="calculator-header">
            <h1>Simulateur de Droits de Rupture</h1>
            <p>
                Estimation complète et conforme au Code du Travail de Côte d'Ivoire (Loi n° 2015-532), 
                à la Convention Collective Interprofessionnelle (CCI de 1977) et au Code Général des Impôts (CGI).
            </p>
        </div>

        <div class="form-wrapper">
            <form @submit.prevent="handleCalculate" class="calc-form">
                
                <!-- ── 1. CONTRAT & CATÉGORIE ── -->
                <div class="grid-2">
                    <BaseSelect
                        v-model="formData.contractType"
                        id="contractType"
                        label="Type de Contrat"
                        :options="contractOptions"
                        required
                    />
                    <BaseSelect
                        v-model="formData.categoriePro"
                        id="categoriePro"
                        label="Catégorie Professionnelle"
                        :options="categorieOptions"
                        required
                    />
                </div>

                <!-- ── 2. MOTIF DE LA RUPTURE ── -->
                <BaseSelect
                    v-model="formData.motif"
                    id="motif"
                    label="Motif de la rupture"
                    :options="filteredMotifOptions"
                    required
                />

                <!-- ── 3. DATES DU CONTRAT ── -->
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
                        label="Date effective de rupture"
                        required
                    />
                </div>

                <!-- ── 4. SALAIRES & RÉMUNÉRATIONS (CDI) ── -->
                <template v-if="formData.contractType === 'cdi'">
                    <div class="grid-2">
                        <BaseInput
                            v-model="formData.baseSalary"
                            id="baseSalary"
                            type="number"
                            min="0"
                            label="Salaire mensuel de base normal (FCFA)"
                            placeholder="Ex: 250000"
                            required
                        />
                        <BaseInput
                            v-model="formData.averageSalary"
                            id="averageSalary"
                            type="number"
                            min="0"
                            label="Salaire global moyen (12 derniers mois)"
                            placeholder="Ex: 310000"
                            required
                        />
                    </div>

                    <!-- Options spécifiques CDI (Préavis) -->
                    <div class="toggle-group" v-if="formData.motif !== 'faute_lourde' && formData.motif !== 'deces'">
                        <label class="toggle-item">
                            <input type="checkbox" v-model="formData.preavisExecute" />
                            <span>Le préavis a-t-il été exécuté / travaillé par le salarié ?</span>
                        </label>
                    </div>
                </template>

                <!-- ── 5. SALAIRES & RÉMUNÉRATIONS (CDD) ── -->
                <template v-if="formData.contractType === 'cdd'">
                    <BaseInput
                        v-model="formData.totalGrossSalary"
                        id="totalGrossSalary"
                        type="number"
                        min="0"
                        label="Rémunération totale brute perçue (sur toute la durée du CDD) en FCFA"
                        placeholder="Ex: 3000000"
                        required
                    />
                    <BaseInput
                        v-if="formData.motif === 'rupture_anticipee'"
                        v-model="formData.remainingMonths"
                        id="remainingMonths"
                        type="number"
                        min="1"
                        label="Nombre de mois restants jusqu'à la fin prévue du CDD"
                        placeholder="Ex: 3"
                        required
                    />
                </template>

                <!-- ── 6. SALAIRE DE PRÉSENCE & CONGÉS PAYÉS ACQUIS ── -->
                <div class="grid-2">
                    <BaseInput
                        v-model="formData.daysWorkedInLastMonth"
                        id="daysWorkedInLastMonth"
                        type="number"
                        min="0"
                        max="30"
                        label="Jours travaillés dans le mois de sortie"
                        placeholder="Ex: 15 (0 si mois complet déjà payé)"
                    />
                    <BaseInput
                        v-model="formData.remainingLeaveDays"
                        id="remainingLeaveDays"
                        type="number"
                        min="0"
                        step="0.5"
                        label="Solde de jours de congés payés restants"
                        placeholder="Ex: 15 (0 si aucun)"
                    />
                </div>

                <!-- Message d'erreur -->
                <div v-if="errorMessage" class="alert error">{{ errorMessage }}</div>

                <!-- Bouton de calcul -->
                <main-button 
                    label="Calculer mes droits & indemnités"
                    :isLoading="isCalculating"
                    type="submit"
                    class="submit-btn"
                />
            </form>

            <!-- ── 7. RÉSULTATS DU CALCUL ── -->
            <div v-if="hasCalculated" class="result-box" :class="{ 'is-zero': netAmount <= 0 }">
                <h3>Total Net estimé du Solde de Tout Compte :</h3>
                <div class="amount">{{ formatCurrency(netAmount) }}</div>
                
                <p class="summary-details">{{ summaryMessage }}</p>

                <!-- Synthèse Financière (Assiettes Fisc./Soc. & Retenues) -->
                <div class="financial-summary">
                    <div class="summary-row">
                        <span>Total Brut Global (Droits & Indemnités) :</span>
                        <strong>{{ formatCurrency(totalGrossAmount) }}</strong>
                    </div>
                    <div class="summary-row sub-row">
                        <span>• Assiette salariale (Imposable & Soumise CNPS) :</span>
                        <span>{{ formatCurrency(totalTaxableCNPS) }}</span>
                    </div>
                    <div class="summary-row sub-row">
                        <span>• Assiette indemnitaire (Exonérée Art. 117 CGI) :</span>
                        <span>{{ formatCurrency(totalExempt) }}</span>
                    </div>
                    <div class="summary-row deduction-row" v-if="cnpsEmployeeDeduction > 0">
                        <span>(-) Retenue salariale CNPS Retraite (6,3 %)* :</span>
                        <span>- {{ formatCurrency(cnpsEmployeeDeduction) }}</span>
                    </div>
                </div>

                <!-- Détail par indemnité -->
                <div class="breakdown-list" v-if="breakdown.length > 0">
                    <h4>Détail des rubriques du solde :</h4>
                    <div 
                        v-for="(item, index) in breakdown" 
                        :key="index" 
                        class="breakdown-item"
                        :class="{ 'is-negative': item.amount < 0 }"
                    >
                        <div class="item-header">
                            <span class="item-title">{{ item.label }}</span>
                            <span class="item-amount">{{ formatCurrency(item.amount) }}</span>
                        </div>
                        <p class="item-desc">{{ item.description }}</p>
                        <div class="item-badges">
                            <span class="badge" :class="item.taxable ? 'badge-taxable' : 'badge-exempt'">
                                {{ item.taxable ? 'Imposable ITS/IGR (Art. 115)' : 'Exonéré ITS/IGR (Art. 117)' }}
                            </span>
                            <span class="badge" :class="item.cnps ? 'badge-taxable' : 'badge-exempt'">
                                {{ item.cnps ? 'Soumis CNPS (Décret 2014-411)' : 'Exonéré CNPS' }}
                            </span>
                        </div>
                    </div>
                </div>

                <small class="disclaimer">
                    * Retenue CNPS Retraite calculée au taux de 6,3 % sur l'assiette soumise (plafonnée à 3 375 000 FCFA/mois selon Décret n° 2015-680). Simulation calculée selon les barèmes légaux et conventionnels en vigueur en Côte d'Ivoire (hors calcul des impôts sur le revenu ITS/IGR qui dépendent de vos parts fiscales Q).
                </small>
            </div>
        </div>
    </section>
</template>

<script lang="ts">
import { ref, computed, watch, defineComponent } from 'vue';
import BaseInput from '../components/input/BaseInput.vue';
import BaseSelect from '../components/input/BaseSelect.vue';
import mainButton from '../components/buttons/mainButton.vue';
import navbar from '../components/navigation/navbar.vue';

interface BreakdownItem {
    label: string;
    amount: number;
    description: string;
    taxable: boolean;
    cnps: boolean;
}

export default defineComponent({
    name: 'LawCalculPage',
    components: {
        BaseInput,
        BaseSelect,
        mainButton,
        navbar
    },
    setup() {
        const contractOptions = [
            { name: "Contrat à Durée Indéterminée (CDI)", value: "cdi" },
            { name: "Contrat à Durée Déterminée (CDD)", value: "cdd" }
        ];

        const categorieOptions = [
            { name: "Ouvrier / Manœuvre", value: "ouvrier" },
            { name: "Employé qualifié", value: "employe" },
            { name: "Agent de maîtrise, Technicien", value: "maitrise" },
            { name: "Cadre, Ingénieur / Assimilé", value: "cadre" }
        ];

        const allMotifs = {
            cdi: [
                { name: "Licenciement sans faute (Économique ou Personnel)", value: "licenciement_normal" },
                { name: "Licenciement pour faute lourde", value: "faute_lourde" },
                { name: "Démission du salarié", value: "demission" },
                { name: "Départ à la retraite", value: "retraite" },
                { name: "Décès du travailleur (Droits des ayants droit)", value: "deces" }
            ],
            cdd: [
                { name: "Fin normale de CDD (Terme atteint)", value: "fin_cdd" },
                { name: "Rupture anticipée abusive (par l'employeur)", value: "rupture_anticipee" },
                { name: "Rupture pour faute lourde ou cas de force majeure", value: "cdd_faute" }
            ]
        };

        const formData = ref({
            contractType: 'cdi',
            categoriePro: 'employe',
            motif: 'licenciement_normal',
            startDate: '',
            endDate: '',
            baseSalary: '',
            averageSalary: '',
            totalGrossSalary: '',
            remainingMonths: '',
            daysWorkedInLastMonth: '0',
            remainingLeaveDays: '0',
            preavisExecute: false
        });

        const isCalculating = ref(false);
        const hasCalculated = ref(false);
        const totalGrossAmount = ref(0);
        const totalTaxableCNPS = ref(0);
        const totalExempt = ref(0);
        const cnpsEmployeeDeduction = ref(0);
        const netAmount = ref(0);
        const summaryMessage = ref('');
        const breakdown = ref<BreakdownItem[]>([]);
        const errorMessage = ref('');

        const filteredMotifOptions = computed(() => {
            return formData.value.contractType === 'cdi' ? allMotifs.cdi : allMotifs.cdd;
        });

        watch(() => formData.value.contractType, (newType) => {
            formData.value.motif = newType === 'cdi' ? 'licenciement_normal' : 'fin_cdd';
            hasCalculated.value = false;
        });

        const formatCurrency = (value: number): string => {
            return new Intl.NumberFormat('fr-FR').format(Math.round(value)) + ' FCFA';
        };

        // Barème légal des durées de préavis (Décret n° 96-200 / CCI Art. 34)
        const getPreavisMonths = (categorie: string, yearsOfSeniority: number): number => {
            if (categorie === 'ouvrier') {
                if (yearsOfSeniority < 1) return 8 / 30; // 8 jours
                if (yearsOfSeniority <= 5) return 1;
                if (yearsOfSeniority <= 10) return 2;
                return 3;
            } else if (categorie === 'employe') {
                if (yearsOfSeniority < 1) return 1;
                if (yearsOfSeniority <= 5) return 2;
                if (yearsOfSeniority <= 10) return 3;
                return 4;
            } else if (categorie === 'maitrise') {
                if (yearsOfSeniority < 1) return 2;
                if (yearsOfSeniority <= 5) return 3;
                if (yearsOfSeniority <= 10) return 4;
                return 5;
            } else { // Cadre
                if (yearsOfSeniority < 1) return 3;
                if (yearsOfSeniority <= 5) return 4;
                if (yearsOfSeniority <= 10) return 5;
                return 6;
            }
        };

        const handleCalculate = async () => {
            isCalculating.value = true;
            errorMessage.value = '';
            hasCalculated.value = false;
            breakdown.value = [];
            totalGrossAmount.value = 0;
            totalTaxableCNPS.value = 0;
            totalExempt.value = 0;
            cnpsEmployeeDeduction.value = 0;
            netAmount.value = 0;

            await new Promise(resolve => setTimeout(resolve, 500));

            try {
                const start = new Date(formData.value.startDate);
                const end = new Date(formData.value.endDate);

                if (end <= start) {
                    errorMessage.value = "La date de fin doit être postérieure à la date d'embauche.";
                    return;
                }

                const diffDays = (end.getTime() - start.getTime()) / (1000 * 3600 * 24);
                const yearsOfSeniority = diffDays / 365.25;
                const daysWorked = Math.max(0, Math.min(30, Number(formData.value.daysWorkedInLastMonth) || 0));
                const remainingLeaves = Math.max(0, Number(formData.value.remainingLeaveDays) || 0);

                // ── 1. LOGIQUE CDI ──
                if (formData.value.contractType === 'cdi') {
                    const baseSalary = Number(formData.value.baseSalary);
                    const avgSalary = Number(formData.value.averageSalary);

                    if (baseSalary <= 0 || avgSalary <= 0) {
                        errorMessage.value = "Veuillez renseigner des salaires mensuels valides.";
                        return;
                    }

                    // A. Salaire de présence (Prorata du mois en cours - Art. 31.1 CT)
                    if (daysWorked > 0) {
                        const presenceAmount = (baseSalary / 30) * daysWorked;
                        breakdown.value.push({
                            label: "Salaire de présence (Mois de sortie)",
                            amount: presenceAmount,
                            description: `Prorata pour ${daysWorked} jour(s) travaillé(s) dans le mois de rupture.`,
                            taxable: true,
                            cnps: true
                        });
                    }

                    // B. Congés payés (due dans TOUS les cas - Art. 25.8 CT)
                    if (remainingLeaves > 0) {
                        const leaveAmount = (baseSalary / 26) * remainingLeaves;
                        breakdown.value.push({
                            label: "Indemnité Compensatrice de Congés Payés (ICCP)",
                            amount: leaveAmount,
                            description: `Calculée sur votre solde de ${remainingLeaves} jours ouvrables acquis et non consommés.`,
                            taxable: true,
                            cnps: true
                        });
                    }

                    // C. Gratification au prorata temporis (Art. 53 CCI)
                    const currentYearMonths = end.getMonth() + 1;
                    const gratificationAmount = (baseSalary / 12) * currentYearMonths;
                    breakdown.value.push({
                        label: "Gratification annuelle (Prorata temporis)",
                        amount: gratificationAmount,
                        description: `Prorata conventionnel pour présence sur l'année civile en cours (${currentYearMonths} mois).`,
                        taxable: true,
                        cnps: true
                    });

                    // D. Selon le motif de rupture (Exclusions & Indemnités)
                    if (formData.value.motif === 'faute_lourde') {
                        summaryMessage.value = "La faute lourde prive le salarié de l'indemnité de préavis et de l'indemnité légale de licenciement (Art. 18.16 CT). Seuls les congés payés et la gratification restent dus.";
                    } 
                    else if (formData.value.motif === 'demission') {
                        // En cas de démission, le préavis non exécuté est DÛ par le salarié à l'employeur (Art. 18.11 CT)
                        if (!formData.value.preavisExecute) {
                            const monthsPreavis = getPreavisMonths(formData.value.categoriePro, yearsOfSeniority);
                            const retenuePreavis = -(avgSalary * monthsPreavis);
                            breakdown.value.push({
                                label: "Retenue pour Préavis non exécuté (Dû par le salarié)",
                                amount: retenuePreavis,
                                description: `Art. 18.11 CT : En cas de démission, le préavis non travaillé est redevable par le salarié à l'employeur (${monthsPreavis} mois).`,
                                taxable: true,
                                cnps: true
                            });
                        }
                        summaryMessage.value = "La démission n'ouvre pas droit à l'indemnité de licenciement. Un préavis non exécuté par le salarié démissionnaire est déduit de son solde.";
                    }
                    else { // Licenciement normal, Retraite ou Décès
                        // - Indemnité compensatrice de préavis (si non effectué et hors Décès)
                        if (!formData.value.preavisExecute && formData.value.motif !== 'deces') {
                            const monthsPreavis = getPreavisMonths(formData.value.categoriePro, yearsOfSeniority);
                            const preavisAmount = avgSalary * monthsPreavis;
                            breakdown.value.push({
                                label: "Indemnité Compensatrice de Préavis (ICP)",
                                amount: preavisAmount,
                                description: `Préavis de rupture non exécuté (${monthsPreavis} mois conformément au barème légal de votre catégorie).`,
                                taxable: true,
                                cnps: true
                            });
                        }

                        // - Indemnité Légale (Licenciement, Retraite ou Décès - minimum 1 an d'ancienneté)
                        if (yearsOfSeniority >= 1) {
                            let tranche1 = Math.min(yearsOfSeniority, 5) * 0.30 * avgSalary;
                            let tranche2 = yearsOfSeniority > 5 ? Math.min(yearsOfSeniority - 5, 5) * 0.35 * avgSalary : 0;
                            let tranche3 = yearsOfSeniority > 10 ? (yearsOfSeniority - 10) * 0.40 * avgSalary : 0;
                            
                            const legalIndemnity = tranche1 + tranche2 + tranche3;
                            let indemLabel = "Indemnité Légale de Licenciement (IL)";
                            if (formData.value.motif === 'retraite') indemLabel = "Indemnité de Départ à la Retraite (Art. 78 CCI)";
                            if (formData.value.motif === 'deces') indemLabel = "Indemnité de Décès versée aux ayants droit (Art. 44 CCI)";

                            breakdown.value.push({
                                label: indemLabel,
                                amount: legalIndemnity,
                                description: `Ancienneté continue de ${yearsOfSeniority.toFixed(2)} ans (Barème CCI Art. 42 : 30 % à 5 ans, 35 % de 6 à 10 ans, 40 % au-delà).`,
                                taxable: false,
                                cnps: false
                            });
                            summaryMessage.value = `Ancienneté validée : ${yearsOfSeniority.toFixed(2)} ans. Conformément à l'Art. 117 du CGI, l'indemnité légale de rupture est 100 % exonérée d'impôts et de CNPS.`;
                        } else {
                            summaryMessage.value = `Ancienneté estimée : ${(yearsOfSeniority * 12).toFixed(1)} mois. Le minimum légal de 1 an d'ancienneté continue requis pour l'indemnité de rupture n'est pas atteint.`;
                        }
                    }
                } 
                // ── 2. LOGIQUE CDD ──
                else if (formData.value.contractType === 'cdd') {
                    const totalGross = Number(formData.value.totalGrossSalary);
                    if (totalGross <= 0) {
                        errorMessage.value = "Veuillez renseigner un montant de salaires bruts perçus valide.";
                        return;
                    }

                    const approxMonthly = (totalGross / Math.max(1, (diffDays / 30.416)));

                    // A. Salaire de présence (Mois de fin)
                    if (daysWorked > 0) {
                        const presenceAmount = (approxMonthly / 30) * daysWorked;
                        breakdown.value.push({
                            label: "Salaire de présence (Mois de sortie)",
                            amount: presenceAmount,
                            description: `Prorata pour ${daysWorked} jour(s) de travail sur le dernier mois.`,
                            taxable: true,
                            cnps: true
                        });
                    }

                    // B. Congés payés restants
                    if (remainingLeaves > 0) {
                        const leaveAmount = (approxMonthly / 26) * remainingLeaves;
                        breakdown.value.push({
                            label: "Indemnité Compensatrice de Congés Payés (ICCP)",
                            amount: leaveAmount,
                            description: `Calculée sur votre solde de ${remainingLeaves} jours ouvrables non pris.`,
                            taxable: true,
                            cnps: true
                        });
                    }

                    // C. Motifs CDD
                    if (formData.value.motif === 'fin_cdd') {
                        const precarite = totalGross * 0.03;
                        breakdown.value.push({
                            label: "Indemnité de Fin de Contrat (Prime de Précarité - 3%)",
                            amount: precarite,
                            description: "Art. 15.8 du Code du Travail : 3 % de la somme totale des rémunérations brutes perçues au cours du contrat.",
                            taxable: true,
                            cnps: true
                        });
                        summaryMessage.value = "Le contrat ayant pris fin à sa date d'échéance sans poursuite en CDI, vous percevez la prime légale de précarité de 3 %.";
                    } 
                    else if (formData.value.motif === 'rupture_anticipee') {
                        const monthsLeft = Number(formData.value.remainingMonths) || 0;
                        const dommages = approxMonthly * monthsLeft;

                        breakdown.value.push({
                            label: "Dommages & Intérêts (Rupture Anticipée CDD)",
                            amount: dommages,
                            description: `Art. 15.9 : Rémunérations totales que vous auriez perçues jusqu'au terme prévu (${monthsLeft} mois restants).`,
                            taxable: false,
                            cnps: false
                        });
                        summaryMessage.value = "La rupture anticipée et abusive par l'employeur oblige au versement indemnitaire de la totalité des mois restants jusqu'au terme du CDD.";
                    } 
                    else {
                        summaryMessage.value = "En cas de faute lourde ou de force majeure, la prime de précarité de 3 % de fin de CDD n'est pas due.";
                    }
                }

                // ── 3. AGRÉGATION DES ASSIETTES & RETENUE CNPS ──
                breakdown.value.forEach(item => {
                    totalGrossAmount.value += item.amount;
                    if (item.cnps) {
                        totalTaxableCNPS.value += item.amount;
                    } else {
                        totalExempt.value += item.amount;
                    }
                });

                // Calcul de la retenue CNPS salariale (6,3 % sur l'assiette soumise, plafond 3 375 000 FCFA/mois)
                const baseCNPSPlafonnee = Math.max(0, Math.min(totalTaxableCNPS.value, 3375000));
                cnpsEmployeeDeduction.value = baseCNPSPlafonnee * 0.063;

                // Solde Net à Percevoir
                netAmount.value = totalGrossAmount.value - cnpsEmployeeDeduction.value;
                hasCalculated.value = true;

            } catch (error) {
                errorMessage.value = "Une erreur technique est survenue lors du calcul de votre simulation.";
            } finally {
                isCalculating.value = false;
            }
        };

        return {
            formData,
            contractOptions,
            categorieOptions,
            filteredMotifOptions,
            isCalculating,
            hasCalculated,
            totalGrossAmount,
            totalTaxableCNPS,
            totalExempt,
            cnpsEmployeeDeduction,
            netAmount,
            summaryMessage,
            breakdown,
            errorMessage,
            formatCurrency,
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
    padding: 7rem 1rem 4rem 1rem;
    background: radial-gradient(circle at 50% 20%, #1a233d 0%, #0c101d 100%);
    color: var(--my-white, #ffffff);
    overflow: hidden;
}

.calculator-header {
    text-align: center;
    max-width: 650px;
    margin-bottom: 2.5rem;
    z-index: 2;
}

.calculator-header h1 {
    font-size: clamp(2rem, 5vw, 2.8rem);
    font-weight: 800;
    margin-bottom: 0.8rem;
    color: #ffffff;
    letter-spacing: -0.5px;
}

.calculator-header p {
    font-size: clamp(0.95rem, 2vw, 1.05rem);
    color: #a0aec0;
    line-height: 1.6;
}

/* ── Conteneur du formulaire (Glassmorphism) ── */
.form-wrapper {
    width: 100%;
    max-width: 720px;
    background: rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 2.5rem;
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
    z-index: 2;
}

.calc-form {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
}

/* Grilles & Dates */
.grid-2, .date-group {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    width: 100%;
}

/* Checkbox et Toggles */
.toggle-group {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 0.8rem 1rem;
}

.toggle-item {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    cursor: pointer;
    font-size: 0.95rem;
    color: #e2e8f0;
}

.toggle-item input[type="checkbox"] {
    width: 1.2rem;
    height: 1.2rem;
    accent-color: #32f459;
    cursor: pointer;
}

/* ── SURCHARGE DES COMPOSANTS BASE (Glassmorphism) ── */
:deep(.form-input),
:deep(.form-select) {
    background-color: rgba(0, 0, 0, 0.25) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 0.85rem 1.1rem !important;
    font-size: 0.95rem !important;
}

:deep(.form-input:focus),
:deep(.form-select:focus) {
    border-color: #32f459 !important;
    box-shadow: 0 0 0 3px rgba(50, 244, 89, 0.15) !important;
    background-color: rgba(0, 0, 0, 0.35) !important;
}

:deep(.input-label) {
    color: #cbd5e1 !important;
    margin-left: 0.2rem !important;
    margin-bottom: 0.4rem !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
}

:deep(.form-select) {
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23ffffff' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e") !important;
}

/* ── Bouton ── */
.submit-btn {
    width: 100%;
    padding: 1.1rem;
    border-radius: 14px;
    font-size: 1.05rem;
    font-weight: 700;
    margin-top: 0.5rem;
    transition: all 0.3s ease;
}

.submit-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(50, 244, 89, 0.25);
}

/* ── RÉSULTATS DU CALCUL ── */
.result-box {
    margin-top: 2.5rem;
    padding: 2rem;
    background: rgba(50, 244, 89, 0.04);
    border: 1px solid rgba(50, 244, 89, 0.3);
    border-radius: 18px;
    animation: fadeIn 0.4s ease-out;
}

.result-box.is-zero {
    background: rgba(239, 68, 68, 0.05);
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.result-box h3 {
    font-size: 1.05rem;
    color: #e2e8f0;
    margin-bottom: 0.4rem;
    font-weight: 500;
    text-align: center;
}

.result-box .amount {
    font-size: 2.6rem;
    font-weight: 800;
    color: #32f459;
    margin-bottom: 1rem;
    text-align: center;
    text-shadow: 0 0 25px rgba(50, 244, 89, 0.35);
}

.result-box.is-zero .amount {
    color: #f87171;
    text-shadow: none;
}

.summary-details {
    font-size: 0.95rem;
    color: #a0aec0;
    line-height: 1.6;
    text-align: center;
    margin-bottom: 1.8rem;
}

/* ── Synthèse Financière (Assiettes & Retenues) ── */
.financial-summary {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 1rem 1.25rem;
    margin-bottom: 1.5rem;
}

.summary-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.4rem 0;
    font-size: 0.95rem;
    color: #f8fafc;
}

.summary-row.sub-row {
    font-size: 0.88rem;
    color: #94a3b8;
    padding-left: 0.5rem;
}

.summary-row.deduction-row {
    border-top: 1px dashed rgba(255, 255, 255, 0.1);
    margin-top: 0.5rem;
    padding-top: 0.7rem;
    color: #fca5a5;
    font-weight: 600;
}

/* ── Liste détaillée par Indemnité ── */
.breakdown-list {
    margin-top: 1.5rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 1.5rem;
}

.breakdown-list h4 {
    font-size: 0.95rem;
    color: #f1f5f9;
    margin-bottom: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.breakdown-item {
    background: rgba(0, 0, 0, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.8rem;
}

.breakdown-item.is-negative {
    border-color: rgba(239, 68, 68, 0.35);
    background: rgba(239, 68, 68, 0.05);
}

.item-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.3rem;
}

.item-title {
    font-weight: 600;
    color: #ffffff;
    font-size: 0.95rem;
}

.item-amount {
    font-weight: 700;
    color: #32f459;
    font-size: 1.05rem;
}

.is-negative .item-amount {
    color: #f87171;
}

.item-desc {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-bottom: 0.6rem;
}

.item-badges {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.badge {
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.25rem 0.6rem;
    border-radius: 9999px;
    letter-spacing: 0.3px;
}

.badge-taxable {
    background: rgba(251, 191, 36, 0.15);
    color: #fcd34d;
    border: 1px solid rgba(251, 191, 36, 0.3);
}

.badge-exempt {
    background: rgba(50, 244, 89, 0.15);
    color: #32f459;
    border: 1px solid rgba(50, 244, 89, 0.3);
}

.disclaimer {
    display: block;
    font-size: 0.75rem;
    color: #64748b;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    margin-top: 1.5rem;
    padding-top: 1rem;
    line-height: 1.5;
    text-align: center;
}

/* ── Alertes ── */
.alert {
    padding: 1rem;
    border-radius: 12px;
    font-size: 0.95rem;
    font-weight: 500;
    text-align: center;
}
.alert.error {
    background: rgba(239, 68, 68, 0.15);
    color: #fca5a5;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

/* ── Animations et Décors ── */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ── Responsive Mobile ── */
@media (max-width: 768px) {
    .calculator-section { padding: 5.5rem 1rem 3rem 1rem; }
    .form-wrapper { padding: 1.5rem; }
    .grid-2, .date-group { grid-template-columns: 1fr; gap: 1rem; }
    .result-box .amount { font-size: 2.1rem; }
    .item-header { flex-direction: column; align-items: flex-start; gap: 0.2rem; }
}
</style>