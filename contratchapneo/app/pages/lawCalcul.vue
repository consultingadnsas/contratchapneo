<template>
    <section class="calculator-section">
        <navbar />

        <div class="calculator-header">
            <div class="badge-legal">
                <span>⚖️ Conforme CCI Côte d'Ivoire & Code du Travail</span>
            </div>
            <h1>Simulateur de Droits de Rupture</h1>
            <p>
                Estimation officielle en temps réel selon le Code du Travail (Loi n° 2015-532), 
                la Convention Collective Interprofessionnelle (CCI de 1977) et le CGI.
            </p>
        </div>

        <!-- ==========================================
             GRILLE 2 COLONNES (STYLE RÉFÉRENCE)
             ========================================== -->
        <div class="calculator-grid">
            
            <!-- ──────────────────────────────────────────
                 COLONNE GAUCHE : FORMULAIRE DE SAISIE
                 ────────────────────────────────────────── -->
            <div class="panel-card panel-left">
                <div class="panel-header">
                    <div class="panel-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 15.75V18m-7.5-6.75h.008v.008H8.25v-.008Zm0 2.25h.008v.008H8.25V13.5Zm0 2.25h.008v.008H8.25v-.008Zm0 2.25h.008v.008H8.25V18Zm2.498-6.75h.007v.008h-.007v-.008Zm0 2.25h.007v.008h-.007V13.5Zm0 2.25h.007v.008h-.007v-.008Zm0 2.25h.007v.008h-.007V18Zm2.504-6.75h.008v.008h-.008v-.008Zm0 2.25h.008v.008h-.008V13.5Zm0 2.25h.008v.008h-.008v-.008Zm0 2.25h.008v.008h-.008V18Zm2.498-6.75h.008v.008h-.008v-.008Zm0 2.25h.008v.008h-.008V13.5ZM8.25 6h7.5v2.25h-7.5V6ZM12 2.25c-1.892 0-3.758.11-5.593.322C5.307 2.7 4.5 3.65 4.5 4.757V19.5a2.25 2.25 0 0 0 2.25 2.25h10.5a2.25 2.25 0 0 0 2.25-2.25V4.757c0-1.108-.806-2.057-1.907-2.185A48.507 48.507 0 0 0 12 2.25Z" />
                        </svg>
                    </div>
                    <h3>Paramètres du Contrat & Salaires</h3>
                </div>

                <form @submit.prevent="handleCalculate" class="calc-form">
                    
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
                            label="Catégorie Pro"
                            :options="categorieOptions"
                            required
                        />
                    </div>

                    <BaseSelect
                        v-model="formData.motif"
                        id="motif"
                        label="Motif de la rupture"
                        :options="filteredMotifOptions"
                        required
                    />

                    <div class="grid-2">
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
                            label="Date de rupture"
                            required
                        />
                    </div>

                    <!-- Options CDI -->
                    <template v-if="formData.contractType === 'cdi'">
                        <div class="grid-2">
                            <BaseInput
                                v-model="formData.baseSalary"
                                id="baseSalary"
                                type="number"
                                min="0"
                                label="Salaire de base (FCFA)"
                                placeholder="250000"
                                required
                            />
                            <BaseInput
                                v-model="formData.averageSalary"
                                id="averageSalary"
                                type="number"
                                min="0"
                                label="Salaire moyen (12 mois)"
                                placeholder="310000"
                                required
                            />
                        </div>

                        <div class="toggle-card" v-if="formData.motif !== 'faute_lourde' && formData.motif !== 'deces'">
                            <label class="toggle-label">
                                <input type="checkbox" v-model="formData.preavisExecute" />
                                <span>Le préavis a été exécuté / travaillé par le salarié</span>
                            </label>
                        </div>
                    </template>

                    <!-- Options CDD -->
                    <template v-if="formData.contractType === 'cdd'">
                        <BaseInput
                            v-model="formData.totalGrossSalary"
                            id="totalGrossSalary"
                            type="number"
                            min="0"
                            label="Rémunération brute totale perçue (FCFA)"
                            placeholder="3000000"
                            required
                        />
                        <BaseInput
                            v-if="formData.motif === 'rupture_anticipee'"
                            v-model="formData.remainingMonths"
                            id="remainingMonths"
                            type="number"
                            min="1"
                            label="Mois restants jusqu'au terme prévu"
                            placeholder="3"
                            required
                        />
                    </template>

                    <div class="grid-2">
                        <BaseInput
                            v-model="formData.daysWorkedInLastMonth"
                            id="daysWorkedInLastMonth"
                            type="number"
                            min="0"
                            max="30"
                            label="Jours travaillés (mois de sortie)"
                            placeholder="15"
                        />
                        <BaseInput
                            v-model="formData.remainingLeaveDays"
                            id="remainingLeaveDays"
                            type="number"
                            min="0"
                            step="0.5"
                            label="Congés payés restants (jours)"
                            placeholder="15"
                        />
                    </div>

                    <div class="toggle-card">
                        <label class="toggle-label">
                            <input type="checkbox" v-model="formData.isDeclaredCNPS" />
                            <span>Travailleur déclaré CNPS (Retenue 6,3 % active)</span>
                        </label>
                    </div>

                    <div v-if="errorMessage" class="alert error">{{ errorMessage }}</div>

                    <!-- Bouton en bas du panneau gauche -->
                    <main-button 
                        label="Calculer mes droits & indemnités"
                        :isLoading="isCalculating"
                        type="submit"
                        class="submit-btn"
                    />
                </form>
            </div>

            <!-- ──────────────────────────────────────────
                 COLONNE DROITE : RÉSULTAT DU CALCUL
                 ────────────────────────────────────────── -->
            <div class="panel-card panel-right">
                <div class="panel-header">
                    <div class="panel-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6a7.5 7.5 0 1 0 7.5 7.5h-7.5V6Z" />
                            <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 10.5H21A7.5 7.5 0 0 0 13.5 3v7.5Z" />
                        </svg>
                    </div>
                    <h3>Estimation du Solde de Tout Compte</h3>
                </div>

                <!-- A) ÉTAPE INITIALE (AVANT CALCUL) -->
                <div v-if="!hasCalculated" class="empty-state">
                    <div class="empty-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                        </svg>
                    </div>
                    <h4>En attente de simulation</h4>
                    <p>Renseignez les paramètres de votre contrat à gauche puis lancez le calcul pour afficher l'estimation officielle de vos droits.</p>
                </div>

                <!-- B) RÉSULTATS GÉNÉRÉS -->
                <div v-else class="results-wrapper">
                    
                    <!-- 1. La carte en surbrillance verte au centre (Style Zakat Amount) -->
                    <div class="highlight-card" :class="{ 'is-zero': netAmount <= 0 }">
                        <span class="highlight-label">Total Net Estimé à Percevoir</span>
                        <div class="big-amount">{{ formatCurrency(netAmount) }}</div>
                        <p class="highlight-subtitle">{{ summaryMessage }}</p>
                        <div class="status-badge">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor" class="badge-icon">
                                <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" />
                            </svg>
                            <span>Conforme Code du Travail & Art. 117 CGI</span>
                        </div>
                    </div>

                    <!-- 2. Synthèse financière sous forme de liste épurée -->
                    <div class="summary-table">
                        <div class="summary-row main-row">
                            <span>Total Brut Global</span>
                            <strong>{{ formatCurrency(totalGrossAmount) }}</strong>
                        </div>
                        <div class="summary-row">
                            <span>Assiette salariale (Imposable & CNPS)</span>
                            <span>{{ formatCurrency(totalTaxableCNPS) }}</span>
                        </div>
                        <div class="summary-row">
                            <span>Assiette indemnitaire (Exonérée Art. 117)</span>
                            <span>{{ formatCurrency(totalExempt) }}</span>
                        </div>
                        <div class="summary-row deduction" v-if="formData.isDeclaredCNPS && cnpsEmployeeDeduction > 0">
                            <span>(-) Retenue salariale CNPS (6,3 %)</span>
                            <span>- {{ formatCurrency(cnpsEmployeeDeduction) }}</span>
                        </div>
                        <div class="summary-row info" v-else-if="!formData.isDeclaredCNPS && totalTaxableCNPS > 0">
                            <span>(i) Statut CNPS : Non déclaré</span>
                            <span>0 FCFA</span>
                        </div>
                    </div>

                    <!-- 3. Liste détaillée par rubrique -->
                    <div class="breakdown-list" v-if="breakdown.length > 0">
                        <h4>Détail des rubriques :</h4>
                        <div v-for="(item, index) in breakdown" :key="index" class="breakdown-item" :class="{ 'is-negative': item.amount < 0 }">
                            <div class="item-head">
                                <span class="item-name">{{ item.label }}</span>
                                <span class="item-val">{{ formatCurrency(item.amount) }}</span>
                            </div>
                            <p class="item-note">{{ item.description }}</p>
                            <div class="item-tags">
                                <span class="tag" :class="item.taxable ? 'tag-tax' : 'tag-free'">
                                    {{ item.taxable ? 'Imposable ITS/IGR' : 'Exonéré Art. 117' }}
                                </span>
                                <span class="tag" :class="item.cnps ? 'tag-cnps' : 'tag-free'">
                                    {{ item.cnps ? 'Soumise CNPS' : 'Exonéré CNPS' }}
                                </span>
                            </div>
                        </div>
                    </div>

                    <!-- 4. Encadré en bas : "Important Notes" (Style référence) -->
                    <div class="legal-notes-card">
                        <h4>Notes Légales Importantes</h4>
                        <ul>
                            <li><strong>Exonération Art. 117 CGI :</strong> Les indemnités légales de rupture (licenciement, retraite, décès) sont totalement exonérées d'impôts sur le revenu et de cotisations CNPS.</li>
                            <li><strong>Retenue CNPS 6,3 % :</strong> Appliquée uniquement sur l'assiette salariale soumise (plafonnée à 3 375 000 FCFA/mois selon le Décret n° 2015-680).</li>
                            <li><strong>Base de calcul :</strong> Cette estimation est produite selon le barème officiel conventionnel et ne tient pas compte des accords d'entreprise plus favorables éventuels.</li>
                        </ul>
                    </div>

                </div>
            </div>

        </div>
    </section>
</template>

<script lang="ts">
// ==========================================================
// AUCUN CHANGEMENT SUR TA LOGIQUE SCRIPT TS !
// CONSERVE TOUT TON BLOC VUE ORIGINAL EXACTEMENT ICI.
// ==========================================================
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
            preavisExecute: false,
            isDeclaredCNPS: true
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

        const getPreavisMonths = (categorie: string, yearsOfSeniority: number): number => {
            if (categorie === 'ouvrier') {
                if (yearsOfSeniority < 1) return 8 / 30;
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
            } else {
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

                if (formData.value.contractType === 'cdi') {
                    const baseSalary = Number(formData.value.baseSalary);
                    const avgSalary = Number(formData.value.averageSalary);

                    if (baseSalary <= 0 || avgSalary <= 0) {
                        errorMessage.value = "Veuillez renseigner des salaires mensuels valides.";
                        return;
                    }

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

                    const currentYearMonths = end.getMonth() + 1;
                    const gratificationAmount = (baseSalary / 12) * currentYearMonths;
                    breakdown.value.push({
                        label: "Gratification annuelle (Prorata temporis)",
                        amount: gratificationAmount,
                        description: `Prorata conventionnel pour présence sur l'année civile en cours (${currentYearMonths} mois).`,
                        taxable: true,
                        cnps: true
                    });

                    if (formData.value.motif === 'faute_lourde') {
                        summaryMessage.value = "La faute lourde prive le salarié de l'indemnité de préavis et de l'indemnité légale de licenciement (Art. 18.16 CT). Seuls les congés payés et la gratification restent dus.";
                    } 
                    else if (formData.value.motif === 'demission') {
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
                    else {
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
                else if (formData.value.contractType === 'cdd') {
                    const totalGross = Number(formData.value.totalGrossSalary);
                    if (totalGross <= 0) {
                        errorMessage.value = "Veuillez renseigner un montant de salaires bruts perçus valide.";
                        return;
                    }

                    const approxMonthly = (totalGross / Math.max(1, (diffDays / 30.416)));

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

                breakdown.value.forEach(item => {
                    totalGrossAmount.value += item.amount;
                    if (item.cnps) {
                        totalTaxableCNPS.value += item.amount;
                    } else {
                        totalExempt.value += item.amount;
                    }
                });

                if (formData.value.isDeclaredCNPS) {
                    const baseCNPSPlafonnee = Math.max(0, Math.min(totalTaxableCNPS.value, 3375000));
                    cnpsEmployeeDeduction.value = baseCNPSPlafonnee * 0.063;
                } else {
                    cnpsEmployeeDeduction.value = 0;
                }

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
/* ==========================================================
   LAYOUT EN 2 COLONNES (ADAPTATION DE L'IMAGE DE RÉFÉRENCE)
   THEME : DARK GLASSMORPHISM + ACCENTS #32F459
   ========================================================== */

.calculator-section {
    position: relative;
    width: 100%;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 7rem 1.5rem 5rem 1.5rem;
    background: radial-gradient(circle at 50% 15%, #18223c 0%, #0a0e1a 100%);
    color: #ffffff;
    overflow-x: hidden;
}

/* ── Header Titre ── */
.calculator-header {
    text-align: center;
    max-width: 680px;
    margin-bottom: 2.8rem;
    z-index: 2;
}

.badge-legal {
    display: inline-flex;
    align-items: center;
    background: rgba(50, 244, 89, 0.1);
    border: 1px solid rgba(50, 244, 89, 0.25);
    padding: 0.35rem 1rem;
    border-radius: 999px;
    margin-bottom: 1.2rem;
}

.badge-legal span {
    font-size: 0.8rem;
    font-weight: 600;
    color: #32f459;
    letter-spacing: 0.4px;
}

.calculator-header h1 {
    font-size: clamp(2.1rem, 5vw, 2.8rem);
    font-weight: 800;
    margin-bottom: 0.7rem;
    color: #ffffff;
    letter-spacing: -0.5px;
}

.calculator-header p {
    font-size: 0.98rem;
    color: #94a3b8;
    line-height: 1.6;
}

/* ── LA GRILLE 2 COLONNES CÔTE À CÔTE ── */
.calculator-grid {
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 2rem;
    width: 100%;
    max-width: 1200px;
    z-index: 2;
    align-items: start;
}

/* ── Style commun des 2 grandes cartes (Glassmorphism) ── */
.panel-card {
    background: rgba(255, 255, 255, 0.025);
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    padding: 2.2rem;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.35);
}

.panel-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 1.2rem;
    margin-bottom: 1.5rem;
}

.panel-icon {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    background: rgba(50, 244, 89, 0.12);
    color: #32f459;
    display: flex;
    align-items: center;
    justify-content: center;
}

.panel-icon svg {
    width: 20px;
    height: 20px;
}

.panel-header h3 {
    font-size: 1.15rem;
    font-weight: 700;
    color: #f8fafc;
    margin: 0;
}

/* ── GAUCHE : Formulaire de Saisie ── */
.calc-form {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
}

.grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    width: 100%;
}

.toggle-card {
    background: rgba(0, 0, 0, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
}

.toggle-label {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    cursor: pointer;
    font-size: 0.9rem;
    color: #cbd5e1;
}

.toggle-label input[type="checkbox"] {
    width: 1.15rem;
    height: 1.15rem;
    accent-color: #32f459;
    cursor: pointer;
}

/* Surcharges champs Base */
:deep(.form-input),
:deep(.form-select) {
    background-color: rgba(0, 0, 0, 0.3) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 0.8rem 1rem !important;
    font-size: 0.92rem !important;
}

:deep(.form-input:focus),
:deep(.form-select:focus) {
    border-color: #32f459 !important;
    box-shadow: 0 0 0 3px rgba(50, 244, 89, 0.15) !important;
}

:deep(.input-label) {
    color: #94a3b8 !important;
    margin-bottom: 0.35rem !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

.submit-btn {
    width: 100%;
    padding: 1.15rem;
    border-radius: 14px;
    font-size: 1.02rem;
    font-weight: 700;
    margin-top: 0.8rem;
    transition: all 0.3s ease;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}

.submit-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 15px 30px rgba(50, 244, 89, 0.25);
}

/* ── DROITE : Panneau Résultat ── */

/* A) État initial (Vide) */
.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #64748b;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
}

.empty-icon {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.03);
    border: 1px dashed rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #475569;
}

.empty-icon svg { width: 30px; height: 30px; }

.empty-state h4 {
    font-size: 1.1rem;
    color: #cbd5e1;
    margin: 0;
}

.empty-state p {
    font-size: 0.9rem;
    max-width: 320px;
    line-height: 1.5;
    margin: 0;
}

/* B) Section Résultats (Style image de référence) */
.results-wrapper {
    display: flex;
    flex-direction: column;
    gap: 1.8rem;
    animation: fadeIn 0.4s ease;
}

/* 1. Encadré vert lumineux "Zakat Amount" équivalent */
.highlight-card {
    background: linear-gradient(135deg, rgba(50, 244, 89, 0.12) 0%, rgba(21, 108, 169, 0.15) 100%);
    border: 1px solid rgba(50, 244, 89, 0.35);
    border-radius: 20px;
    padding: 2rem 1.5rem;
    text-align: center;
    box-shadow: 0 10px 30px rgba(50, 244, 89, 0.08);
}

.highlight-card.is-zero {
    background: rgba(239, 68, 68, 0.08);
    border-color: rgba(239, 68, 68, 0.35);
}

.highlight-label {
    font-size: 0.88rem;
    font-weight: 600;
    color: #a7f3d0;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    display: block;
    margin-bottom: 0.6rem;
}

.big-amount {
    font-size: clamp(2.2rem, 4vw, 2.8rem);
    font-weight: 800;
    color: #32f459;
    margin-bottom: 0.8rem;
    text-shadow: 0 0 30px rgba(50, 244, 89, 0.35);
}

.highlight-card.is-zero .big-amount {
    color: #f87171;
    text-shadow: none;
}

.highlight-subtitle {
    font-size: 0.88rem;
    color: #cbd5e1;
    max-width: 90%;
    margin: 0 auto 1.2rem auto;
    line-height: 1.5;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(50, 244, 89, 0.2);
    border: 1px solid rgba(50, 244, 89, 0.4);
    color: #32f459;
    padding: 0.4rem 1rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 700;
}

.badge-icon {
    width: 16px;
    height: 16px;
}

/* 2. Tableau de synthèse financière */
.summary-table {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding: 1.2rem 0;
}

.summary-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.92rem;
    color: #cbd5e1;
}

.summary-row.main-row {
    font-size: 1.05rem;
    color: #ffffff;
    font-weight: 600;
}

.summary-row.deduction {
    color: #fca5a5;
    font-weight: 600;
}

.summary-row.info {
    color: #fcd34d;
    font-size: 0.85rem;
}

/* 3. Détail des rubriques */
.breakdown-list h4 {
    font-size: 0.9rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin: 0 0 1rem 0;
}

.breakdown-item {
    background: rgba(0, 0, 0, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.7rem;
}

.breakdown-item.is-negative {
    border-color: rgba(239, 68, 68, 0.3);
    background: rgba(239, 68, 68, 0.05);
}

.item-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.3rem;
}

.item-name {
    font-weight: 600;
    color: #ffffff;
    font-size: 0.92rem;
}

.item-val {
    font-weight: 700;
    color: #32f459;
    font-size: 0.98rem;
}

.is-negative .item-val { color: #f87171; }

.item-note {
    font-size: 0.82rem;
    color: #94a3b8;
    margin: 0 0 0.6rem 0;
    line-height: 1.4;
}

.item-tags {
    display: flex;
    gap: 0.4rem;
}

.tag {
    font-size: 0.7rem;
    font-weight: 600;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
}

.tag-tax { background: rgba(251, 191, 36, 0.12); color: #fcd34d; border: 1px solid rgba(251, 191, 36, 0.25); }
.tag-cnps { background: rgba(56, 189, 248, 0.12); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.25); }
.tag-free { background: rgba(50, 244, 89, 0.12); color: #32f459; border: 1px solid rgba(50, 244, 89, 0.25); }

/* 4. Encadré "Important Notes" au bas de la colonne de droite */
.legal-notes-card {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 16px;
    padding: 1.4rem;
}

.legal-notes-card h4 {
    font-size: 0.95rem;
    color: #f8fafc;
    margin: 0 0 0.8rem 0;
}

.legal-notes-card ul {
    margin: 0;
    padding-left: 1.2rem;
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
}

.legal-notes-card li {
    font-size: 0.82rem;
    color: #94a3b8;
    line-height: 1.5;
}

.legal-notes-card strong {
    color: #cbd5e1;
}

/* ── Alertes ── */
.alert {
    padding: 0.9rem;
    border-radius: 12px;
    font-size: 0.9rem;
    font-weight: 500;
    text-align: center;
}
.alert.error {
    background: rgba(239, 68, 68, 0.15);
    color: #fca5a5;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ── RESPONSIVE MOBILE & TABLETTE (Bascule sur 1 colonne) ── */
@media (max-width: 992px) {
    .calculator-grid {
        grid-template-columns: 1fr;
        gap: 2.5rem;
    }
    .calculator-section {
        padding: 5.5rem 1rem 3rem 1rem;
    }
    .panel-card {
        padding: 1.5rem;
    }
    .grid-2 {
        grid-template-columns: 1fr;
    }
}
</style>