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

        <div v-if="currentStep === 1" class="email-step-container">
            <div class="email-card glass-panel">
                <h2>Commencez votre simulation</h2>
                <p>Veuillez renseigner votre adresse e-mail pour accéder au simulateur de droits.</p>
                
                <div class="input-group">
                    <input 
                        type="email" 
                        v-model="userEmail" 
                        placeholder="votre.email@exemple.com" 
                        @keyup.enter="goToStep2"
                    />
                </div>
                
                <p v-if="emailError" class="error-text">{{ emailError }}</p>

                <button class="btn-primary" @click="goToStep2">
                    Accéder au simulateur
                </button>
            </div>
        </div>

        <div v-else-if="currentStep === 2" class="calculator-grid fade-in">
            <!-- Composant Formulaire (Gauche) -->
            <div class="left-col">
                <div v-if="errorMessage || lawStore.error" class="alert error" role="alert" aria-live="assertive">
                    <strong>Erreur :</strong> {{ errorMessage || lawStore.error }}
                </div>

                <LawCalculForm 
                    v-model="formData"
                    :isCalculating="isCalculating || lawStore.isLoading"
                    :errorMessage="errorMessage || lawStore.error"
                    :contractOptions="contractOptions"
                    :categorieOptions="categorieOptions"
                    :filteredMotifOptions="filteredMotifOptions"
                    @submit="handleCalculate"
                />
            </div>

            <!-- Composant Résultat (Droite) -->
            <div class="right-col">
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
        </div>
    </section>
</template>

<script lang="ts">
import { ref, computed, watch, defineComponent } from 'vue';
import navbar from '../components/navigation/navbar.vue';
import LawCalculForm from '../components/forms/lawcalculForm.vue';
import LawCalculResult from '../components/sections/lawcalculResult.vue';
// ⚡️ 1. IMPORT DU STORE
import { useLawCalculStore } from '../stores/lawCalculStore'; 

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
        // ⚡️ 2. INITIALISATION DU STORE
        const lawStore = useLawCalculStore();

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
                { name: "Rupture d'un commun accord (Amiable)", value: "commun_accord_cdd" },
                { name: "Rupture anticipée abusive par l'employeur", value: "rupture_anticipee_employeur" },
                { name: "Rupture anticipée par l'employé (Démission CDD)", value: "rupture_anticipee_salarie" },
                { name: "Rupture pour faute lourde ou force majeure", value: "cdd_faute" }
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
            employerDamages: '', 
            daysWorkedInLastMonth: '0',
            remainingLeaveDays: '0',
            preavisExecute: false,
            isDeclaredCNPS: true
        });

        const currentStep = ref(1);
        const userEmail = ref('');
        const emailError = ref('');

        const isValidEmail = (email: string) => {
            const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return regex.test(email);
        };

        const goToStep2 = () => {
            emailError.value = '';
            if (!userEmail.value) {
                emailError.value = "L'adresse e-mail est requise.";
                return;
            }
            if (!isValidEmail(userEmail.value)) {
                emailError.value = "Veuillez entrer une adresse e-mail valide.";
                return;
            }
            currentStep.value = 2;
        };

        // ⚡️ 3. SYNCHRONISATION DU CHARGEMENT AVEC LE STORE
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

            try {
                // Petit délai pour l'effet de chargement UI
                await new Promise(resolve => setTimeout(resolve, 300));

                if (!formData.value.startDate || !formData.value.endDate) {
                    errorMessage.value = "Veuillez renseigner les dates d'embauche et de rupture.";
                    return;
                }

                const start = new Date(formData.value.startDate);
                const end = new Date(formData.value.endDate);

                if (end <= start) {
                    errorMessage.value = "La date de fin doit être postérieure à la date d'embauche.";
                    return;
                }

                // ⚡️ 1. MAPPAGE ET SAUVEGARDE BACKEND VIA LE STORE
                const motifMap: Record<string, string> = {
                    'licenciement_normal': 'Licenciement_Sans_Faute',
                    'faute_lourde': 'Licenciement_Faute_Lourde',
                    'demission': 'Demission',
                    'retraite': 'Retraite',
                    'deces': 'Deces',
                    'fin_cdd': 'Fin_CDD',
                    'commun_accord_cdd': 'Commun_Accord_CDD',
                    'rupture_anticipee_employeur': 'Rupture_Anticipee_Employeur',
                    'rupture_anticipee_salarie': 'Rupture_Anticipee_Employe',
                    'cdd_faute': 'Faute_Lourde_CDD'
                };

                const catMap: Record<string, string> = {
                    'ouvrier': 'Ouvrier_Manoeuvre',
                    'employe': 'Employe_Qualifie',
                    'maitrise': 'Agent_Maitrise',
                    'cadre': 'Cadre_Assimile'
                };

                const rawLeaveDays = String(formData.value.remainingLeaveDays || '0').replace(',', '.');
                const remainingLeaves = Math.max(0, Number(rawLeaveDays) || 0);

                const payload = {
                    email: userEmail.value,
                    type_contrat: formData.value.contractType.toUpperCase(),
                    motif_rupture: motifMap[formData.value.motif] || 'Licenciement_Sans_Faute',
                    categorie_pro: catMap[formData.value.categoriePro] || 'Employe_Qualifie',
                    date_embauche: formData.value.startDate,
                    date_rupture: formData.value.endDate,
                    salaire_base: Number(formData.value.baseSalary) || Number(formData.value.totalGrossSalary) || 0,
                    surtaux_accords: 0,
                    salaires_12_mois: formData.value.averageSalary ? [Number(formData.value.averageSalary)] : [],
                    preavis_effectue: formData.value.preavisExecute,
                    jours_conges_acquis: remainingLeaves
                };

                // On envoie au backend pour l'historique
                await lawStore.calculateDroits(payload);

                // Si le backend a renvoyé des résultats, on s'en sert pour l'affichage
                if (lawStore.resultats) {
                    const srv: any = lawStore.resultats;

                    // Remise à zéro des tableaux/totaux
                    breakdown.value = [];
                    totalGrossAmount.value = 0;
                    totalTaxableCNPS.value = 0;
                    totalExempt.value = 0;

                    // Construire le breakdown à partir des clés renvoyées par le serveur
                    if (srv.indemnite_conges && Number(srv.indemnite_conges) !== 0) {
                        const amt = Number(srv.indemnite_conges);
                        breakdown.value.push({ label: "Indemnité Congés (serveur)", amount: amt, description: "Indemnité compensatrice de congés calculée côté serveur.", taxable: true, cnps: true });
                    }
                    if (srv.indemnite_preavis && Number(srv.indemnite_preavis) !== 0) {
                        const amt = Number(srv.indemnite_preavis);
                        breakdown.value.push({ label: "Indemnité Préavis (serveur)", amount: amt, description: "Indemnité compensatrice de préavis calculée côté serveur.", taxable: true, cnps: true });
                    }
                    if (srv.indemnite_licenciement && Number(srv.indemnite_licenciement) !== 0) {
                        const amt = Number(srv.indemnite_licenciement);
                        breakdown.value.push({ label: "Indemnité Licenciement (serveur)", amount: amt, description: "Indemnité légale/CCI calculée côté serveur.", taxable: false, cnps: false });
                    }

                    // Totaux
                    breakdown.value.forEach((item: any) => {
                        totalGrossAmount.value += item.amount;
                        if (item.cnps) totalTaxableCNPS.value += item.amount;
                        else if (item.amount > 0) totalExempt.value += item.amount;
                    });

                    // Calcul de la déduction CNPS côté front (affichage)
                    if (formData.value.isDeclaredCNPS) {
                        const baseCNPSPlafonnee = Math.max(0, Math.min(totalTaxableCNPS.value, 3375000));
                        cnpsEmployeeDeduction.value = baseCNPSPlafonnee * 0.063;
                    } else {
                        cnpsEmployeeDeduction.value = 0;
                    }

                    netAmount.value = totalGrossAmount.value - cnpsEmployeeDeduction.value;
                    summaryMessage.value = "Résultats fournis par le serveur";
                    hasCalculated.value = true;
                    // On sort pour éviter le double calcul frontend
                    isCalculating.value = false;
                    return;
                }

                // ⚡️ 2. CALCUL FRONTEND POUR L'AFFICHAGE DÉTAILLÉ
                const diffDays = (end.getTime() - start.getTime()) / (1000 * 3600 * 24);
                const yearsOfSeniority = diffDays / 365.25;
                const daysWorked = Math.max(0, Math.min(30, Number(formData.value.daysWorkedInLastMonth) || 0));

                // ── LOGIQUE CDI ──
                if (formData.value.contractType === 'cdi') {
                    const baseSalary = Number(formData.value.baseSalary);
                    const avgSalary = Number(formData.value.averageSalary);

                    if (daysWorked > 0) {
                        const presenceAmount = (baseSalary / 30) * daysWorked;
                        breakdown.value.push({
                            label: "Salaire de présence (Mois de sortie)", amount: presenceAmount,
                            description: `Prorata pour ${daysWorked} jour(s) travaillé(s) dans le mois de rupture.`,
                            taxable: true, cnps: true
                        });
                    }

                    if (remainingLeaves > 0) {
                        const leaveAmount = (baseSalary / 26) * remainingLeaves;
                        breakdown.value.push({
                            label: "Indemnité Compensatrice de Congés Payés (ICCP)", amount: leaveAmount,
                            description: `Calculée sur votre solde de ${remainingLeaves} jours ouvrables acquis et non consommés.`,
                            taxable: true, cnps: true
                        });
                    }

                    const currentYearMonths = end.getMonth() + 1;
                    const gratificationAmount = (baseSalary / 12) * currentYearMonths;
                    breakdown.value.push({
                        label: "Gratification annuelle (Prorata temporis)", amount: gratificationAmount,
                        description: `Prorata conventionnel pour présence sur l'année civile en cours (${currentYearMonths} mois).`,
                        taxable: true, cnps: true
                    });

                    if (formData.value.motif === 'faute_lourde') {
                        summaryMessage.value = "La faute lourde prive le salarié de l'indemnité de préavis et de l'indemnité légale de licenciement (Art. 18.16 CT). Seuls les congés payés et la gratification restent dus.";
                    } 
                    else if (formData.value.motif === 'demission') {
                        if (!formData.value.preavisExecute) {
                            const monthsPreavis = getPreavisMonths(formData.value.categoriePro, yearsOfSeniority);
                            const retenuePreavis = -(avgSalary * monthsPreavis);
                            breakdown.value.push({
                                label: "Retenue pour Préavis non exécuté (Dû par le salarié)", amount: retenuePreavis,
                                description: `Art. 18.11 CT : En cas de démission, le préavis non travaillé est redevable par le salarié à l'employeur (${monthsPreavis} mois).`,
                                taxable: true, cnps: true
                            });
                        }
                        summaryMessage.value = "La démission n'ouvre pas droit à l'indemnité de licenciement. Un préavis non exécuté par le salarié démissionnaire est déduit de son solde.";
                    }
                    else {
                        if (!formData.value.preavisExecute && formData.value.motif !== 'deces') {
                            const monthsPreavis = getPreavisMonths(formData.value.categoriePro, yearsOfSeniority);
                            const preavisAmount = avgSalary * monthsPreavis;
                            breakdown.value.push({
                                label: "Indemnité Compensatrice de Préavis (ICP)", amount: preavisAmount,
                                description: `Préavis de rupture non exécuté (${monthsPreavis} mois conformément au barème légal de votre catégorie).`,
                                taxable: true, cnps: true
                            });
                        }

                        if (yearsOfSeniority >= 1) {
                            let tranche1 = Math.min(yearsOfSeniority, 5) * 0.30 * avgSalary;
                            let tranche2 = yearsOfSeniority > 5 ? Math.min(yearsOfSeniority - 5, 5) * 0.35 * avgSalary : 0;
                            let tranche3 = yearsOfSeniority > 10 ? (yearsOfSeniority - 10) * 0.40 * avgSalary : 0;
                            
                            const legalIndemnity = tranche1 + tranche2 + tranche3;
                            let indemLabel = formData.value.motif === 'retraite' ? "Indemnité de Départ à la Retraite (Art. 78 CCI)" : 
                                             formData.value.motif === 'deces' ? "Indemnité de Décès versée aux ayants droit (Art. 44 CCI)" : 
                                             "Indemnité Légale de Licenciement (IL)";

                            breakdown.value.push({
                                label: indemLabel, amount: legalIndemnity,
                                description: `Ancienneté continue de ${yearsOfSeniority.toFixed(2)} ans (Barème CCI Art. 42).`,
                                taxable: false, cnps: false
                            });
                            summaryMessage.value = `Ancienneté validée : ${yearsOfSeniority.toFixed(2)} ans. Conformément à l'Art. 117 du CGI, l'indemnité légale de rupture est 100 % exonérée d'impôts et de CNPS.`;
                        } else {
                            summaryMessage.value = `Ancienneté estimée : ${(yearsOfSeniority * 12).toFixed(1)} mois. Le minimum légal de 1 an d'ancienneté continue requis pour l'indemnité de rupture n'est pas atteint.`;
                        }
                    }
                } 
                // ── LOGIQUE CDD ──
                else if (formData.value.contractType === 'cdd') {
                    const totalGross = Number(formData.value.totalGrossSalary);
                    const approxMonthly = (totalGross / Math.max(1, (diffDays / 30.416)));

                    if (daysWorked > 0) {
                        const presenceAmount = (approxMonthly / 30) * daysWorked;
                        breakdown.value.push({
                            label: "Salaire de présence (Mois de sortie)", amount: presenceAmount,
                            description: `Prorata pour ${daysWorked} jour(s) de travail sur le dernier mois.`,
                            taxable: true, cnps: true
                        });
                    }

                    if (remainingLeaves > 0) {
                        const leaveAmount = (approxMonthly / 26) * remainingLeaves;
                        breakdown.value.push({
                            label: "Indemnité Compensatrice de Congés Payés (ICCP)", amount: leaveAmount,
                            description: `Calculée sur votre solde de ${remainingLeaves} jours ouvrables non pris.`,
                            taxable: true, cnps: true
                        });
                    }

                    if (formData.value.motif === 'fin_cdd' || formData.value.motif === 'commun_accord_cdd') {
                        const precarite = totalGross * 0.03;
                        breakdown.value.push({
                            label: "Indemnité de Fin de Contrat (Prime de Précarité - 3%)", amount: precarite,
                            description: "Art. 15.8 du Code du Travail : 3 % de la somme totale des rémunérations brutes perçues au cours du contrat.",
                            taxable: true, cnps: true
                        });
                        summaryMessage.value = formData.value.motif === 'commun_accord_cdd' 
                            ? "Dans le cadre d'une rupture d'un commun accord (amiable), la prime légale de précarité de 3 % reste due, sauf renonciation expresse des deux parties."
                            : "Le contrat ayant pris fin à sa date d'échéance sans poursuite en CDI, vous percevez la prime légale de précarité de 3 %.";
                    } 
                    else if (formData.value.motif === 'rupture_anticipee_employeur') {
                        const monthsLeft = Number(formData.value.remainingMonths) || 0;
                        const dommages = approxMonthly * monthsLeft;
                        breakdown.value.push({
                            label: "Dommages & Intérêts (Rupture Anticipée Employeur)", amount: dommages,
                            description: `Art. 15.9 : Rémunérations totales que vous auriez perçues jusqu'au terme prévu (${monthsLeft} mois restants).`,
                            taxable: false, cnps: false
                        });
                        summaryMessage.value = "La rupture anticipée et abusive par l'employeur oblige au versement indemnitaire de la totalité des mois restants jusqu'au terme du CDD.";
                    } 
                    else if (formData.value.motif === 'rupture_anticipee_salarie') {
                        const dommagesSalarie = Number(formData.value.employerDamages) || 0;
                        if (dommagesSalarie > 0) {
                            breakdown.value.push({ 
                                label: "Dommages & Intérêts dus à l'employeur", amount: -dommagesSalarie,
                                description: "Art. 15.9 : Compensation du préjudice subi par l'employeur suite à la rupture anticipée non justifiée par l'employé.", 
                                taxable: false, cnps: false 
                            });
                        }
                        summaryMessage.value = "La rupture anticipée par l'employé annule le droit à la prime de précarité de 3 %. L'employeur est en droit de réclamer des dommages-intérêts réparant son préjudice.";
                    }
                    else {
                        summaryMessage.value = "En cas de faute lourde ou de force majeure, la prime de précarité de 3 % de fin de CDD n'est pas due.";
                    }
                }

                // ⚡️ 3. FINALISATION DES TOTAUX
                breakdown.value.forEach(item => {
                    totalGrossAmount.value += item.amount;
                    if (item.cnps) {
                        totalTaxableCNPS.value += item.amount;
                    } else {
                        if (item.amount > 0) totalExempt.value += item.amount;
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

            } catch (error: any) {
                errorMessage.value = lawStore.error || "Une erreur technique est survenue lors de la communication avec le serveur.";
            } finally {
                isCalculating.value = false;
            }
        };

        const serverResultsAvailable = computed(() => !!lawStore.resultats);

        return {
            formData,
            contractOptions,
            currentStep,
            userEmail,
            emailError,
            goToStep2,
            categorieOptions,
            filteredMotifOptions,
            isCalculating,
            lawStore,
            serverResultsAvailable,
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
/* ⚡️ STYLES POUR L'ÉTAPE 1 (EMAIL) */
.email-step-container {
    display: flex;
    justify-content: center;
    width: 100%;
    z-index: 2;
    margin-top: 2rem;
}

.email-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 3rem;
    width: 100%;
    max-width: 500px;
    text-align: center;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
}

.email-card h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: #ffffff;
}

.email-card p {
    color: #94a3b8;
    font-size: 0.95rem;
    margin-bottom: 2rem;
}

.input-group input {
    width: 100%;
    padding: 1rem 1.2rem;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    background: rgba(0, 0, 0, 0.2);
    color: white;
    font-size: 1rem;
    outline: none;
    transition: border-color 0.3s ease;
    margin-bottom: 1rem;
}

.input-group input:focus {
    border-color: #068cec; /* Reprend le bleu de ton shape-bottom-right */
}

.error-text {
    color: #ff4757 !important;
    font-size: 0.85rem !important;
    margin-top: -0.5rem;
    margin-bottom: 1.5rem !important;
}

.btn-primary {
    background: #068cec;
    color: white;
    border: none;
    padding: 1rem;
    border-radius: 12px;
    font-size: 1rem;
    font-weight: 600;
    width: 100%;
    cursor: pointer;
    transition: transform 0.2s ease, background 0.3s ease;
}

.btn-primary:hover {
    background: #0570bd;
    transform: translateY(-2px);
}

.fade-in {
    animation: fadeIn 0.4s ease-out forwards;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
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

.left-col { }
.right-col { position: relative; }

.alert.error {
    background: rgba(255,69,103,0.08);
    border: 1px solid rgba(255,69,103,0.18);
    color: #ff4757;
    padding: 0.8rem 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
}

/* Éléments de fond (Cercles floutés) */
.bg-shape { position: absolute; border-radius: 50%; filter: blur(100px); z-index: 1; opacity: 0.45; pointer-events: none; }
.shape-top-left { top: -5%; left: -5%; width: 450px; height: 450px; background: radial-gradient(circle, #32f459 0%, transparent 70%); }
.shape-bottom-right { bottom: -5%; right: -5%; width: 500px; height: 500px; background: radial-gradient(circle, #068cec 0%, transparent 70%); }

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