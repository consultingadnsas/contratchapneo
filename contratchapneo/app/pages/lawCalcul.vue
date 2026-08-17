<template>
    <section class="calculator-section">
        <navbar />

        <div class="calculator-header">
            <h1>Calcul des Droits</h1>
            <p>
                Estimation officielle en temps réel selon le Code du Travail (Loi n° 2015-532), 
                la Convention Collective Interprofessionnelle (CCI de 1977) et le CGI.
            </p>
        </div>

        <div class="calculator-grid">
            
            <!-- Composant Formulaire (Gauche) -->
            <LawCalculForm 
                v-model="formData"
                :isCalculating="isCalculating"
                :errorMessage="errorMessage"
                :contractOptions="contractOptions"
                :categorieOptions="categorieOptions"
                :filteredMotifOptions="filteredMotifOptions"
                @submit="handleCalculate"
            />

            <!-- Composant Résultat (Droite) -->
            <LawCalculResult 
                :hasCalculated="hasCalculated"
                :netAmount="netAmount"
                :totalGrossAmount="totalGrossAmount"
                :totalTaxableCNPS="totalTaxableCNPS"
                :totalExempt="totalExempt"
                :cnpsEmployeeDeduction="cnpsEmployeeDeduction"
                :isDeclaredCNPS="formData.isDeclaredCNPS"
                :summaryMessage="summaryMessage"
                :breakdown="breakdown"
            />

        </div>
    </section>
</template>

<script lang="ts">
import { ref, computed, watch, defineComponent } from 'vue';
import navbar from '../components/navigation/navbar.vue';
import LawCalculForm from '../components/forms/lawcalculForm.vue';
import LawCalculResult from '../components/sections/lawcalculResult.vue';

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
        navbar,
        LawCalculForm,
        LawCalculResult
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

            // ⚡️ CORRECTION : Le bloc TRY englobe désormais TOUT le traitement
            try {
                await new Promise(resolve => setTimeout(resolve, 300));

                if (!formData.value.startDate || !formData.value.endDate) {
                    errorMessage.value = "Veuillez renseigner les dates d'embauche et de rupture.";
                    return; // Le bloc finally sera maintenant bien exécuté après ce return !
                }

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
                // ⚡️ GARANTIE ABSOLUE : isCalculating repasse TOUJOURS à false !
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
            handleCalculate
        };
    }
});
</script>

<style scoped>
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

.calculator-header {
    text-align: center;
    max-width: 680px;
    margin-bottom: 2.8rem;
    z-index: 2;
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

.calculator-grid {
    display: grid;
    grid-template-columns: 1.05fr 0.95fr;
    gap: 2rem;
    width: 100%;
    max-width: 1200px;
    z-index: 2;
    align-items: start;
}

@media (max-width: 992px) {
    .calculator-grid {
        grid-template-columns: 1fr;
        gap: 2.5rem;
    }
    .calculator-section {
        padding: 5.5rem 1rem 3rem 1rem;
    }
}
</style>