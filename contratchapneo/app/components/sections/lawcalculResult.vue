<template>
    <div class="panel-card panel-right">
        <div class="panel-header">
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
                <div class="summary-row deduction" v-if="isDeclaredCNPS && cnpsEmployeeDeduction > 0">
                    <span>(-) Retenue salariale CNPS (6,3 %)</span>
                    <span>- {{ formatCurrency(cnpsEmployeeDeduction) }}</span>
                </div>
                <div class="summary-row info" v-else-if="!isDeclaredCNPS && totalTaxableCNPS > 0">
                    <span>(i) Statut CNPS : Non déclaré</span>
                    <span>0 FCFA</span>
                </div>
            </div>

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

            <div class="legal-notes-card">
                <h4>Notes Légales Importantes</h4>
                <ul>
                    <li><strong>Exonération Art. 117 CGI :</strong> Les indemnités légales de rupture sont exonérées d'impôts et de CNPS.</li>
                    <li><strong>Retenue CNPS 6,3 % :</strong> Appliquée uniquement sur l'assiette salariale soumise (plafonnée à 3 375 000 FCFA/mois).</li>
                    <li><strong>Base de calcul :</strong> Cette estimation est produite selon le barème officiel conventionnel.</li>
                </ul>
            </div>

        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';

interface BreakdownItem {
    label: string;
    amount: number;
    description: string;
    taxable: boolean;
    cnps: boolean;
}

export default defineComponent({
    name: 'LawCalculResult',
    props: {
        hasCalculated: { type: Boolean, required: true },
        netAmount: { type: Number, required: true },
        totalGrossAmount: { type: Number, required: true },
        totalTaxableCNPS: { type: Number, required: true },
        totalExempt: { type: Number, required: true },
        cnpsEmployeeDeduction: { type: Number, required: true },
        isDeclaredCNPS: { type: Boolean, required: true },
        summaryMessage: { type: String, required: true },
        breakdown: { type: Array as PropType<BreakdownItem[]>, required: true }
    },
    setup() {
        const formatCurrency = (value: number): string => {
            return new Intl.NumberFormat('fr-FR').format(Math.round(value)) + ' FCFA';
        };
        return { formatCurrency };
    }
});
</script>

<style scoped>
.panel-card { background: rgba(255, 255, 255, 0.025); backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 24px; padding: 2.2rem; box-shadow: 0 20px 50px rgba(0, 0, 0, 0.35); }
.panel-header { display: flex; align-items: center; gap: 0.8rem; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 1.2rem; margin-bottom: 1.5rem; }
.panel-header h3 { font-size: 1.15rem; font-weight: 700; color: #f8fafc; margin: 0; }
.empty-state { text-align: center; padding: 4rem 2rem; color: #64748b; display: flex; flex-direction: column; align-items: center; gap: 1rem; }
.empty-icon { width: 60px; height: 60px; border-radius: 50%; background: rgba(255, 255, 255, 0.03); border: 1px dashed rgba(255, 255, 255, 0.1); display: flex; align-items: center; justify-content: center; color: #475569; }
.empty-icon svg { width: 30px; height: 30px; }
.empty-state h4 { font-size: 1.1rem; color: #cbd5e1; margin: 0; }
.empty-state p { font-size: 0.9rem; max-width: 320px; line-height: 1.5; margin: 0; }
.results-wrapper { display: flex; flex-direction: column; gap: 1.8rem; animation: fadeIn 0.4s ease; }
.highlight-card { background: linear-gradient(135deg, rgba(50, 244, 89, 0.12) 0%, rgba(21, 108, 169, 0.15) 100%); border: 1px solid rgba(50, 244, 89, 0.35); border-radius: 20px; padding: 2rem 1.5rem; text-align: center; box-shadow: 0 10px 30px rgba(50, 244, 89, 0.08); }
.highlight-card.is-zero { background: rgba(239, 68, 68, 0.08); border-color: rgba(239, 68, 68, 0.35); }
.highlight-label { font-size: 0.88rem; font-weight: 600; color: #a7f3d0; text-transform: uppercase; letter-spacing: 0.8px; display: block; margin-bottom: 0.6rem; }
.big-amount { font-size: clamp(2.2rem, 4vw, 2.8rem); font-weight: 800; color: #32f459; margin-bottom: 0.8rem; text-shadow: 0 0 30px rgba(50, 244, 89, 0.35); }
.highlight-card.is-zero .big-amount { color: #f87171; text-shadow: none; }
.highlight-subtitle { font-size: 0.88rem; color: #cbd5e1; max-width: 90%; margin: 0 auto 1.2rem auto; line-height: 1.5; }
.status-badge { display: inline-flex; align-items: center; gap: 0.5rem; background: rgba(50, 244, 89, 0.2); border: 1px solid rgba(50, 244, 89, 0.4); color: #32f459; padding: 0.4rem 1rem; border-radius: 999px; font-size: 0.82rem; font-weight: 700; }
.badge-icon { width: 16px; height: 16px; }
.summary-table { display: flex; flex-direction: column; gap: 0.8rem; border-top: 1px solid rgba(255, 255, 255, 0.08); border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding: 1.2rem 0; }
.summary-row { display: flex; justify-content: space-between; font-size: 0.92rem; color: #cbd5e1; }
.summary-row.main-row { font-size: 1.05rem; color: #ffffff; font-weight: 600; }
.summary-row.deduction { color: #fca5a5; font-weight: 600; }
.summary-row.info { color: #fcd34d; font-size: 0.85rem; }
.breakdown-list h4 { font-size: 0.9rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.6px; margin: 0 0 1rem 0; }
.breakdown-item { background: rgba(0, 0, 0, 0.25); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 0.7rem; }
.breakdown-item.is-negative { border-color: rgba(239, 68, 68, 0.3); background: rgba(239, 68, 68, 0.05); }
.item-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem; }
.item-name { font-weight: 600; color: #ffffff; font-size: 0.92rem; }
.item-val { font-weight: 700; color: #32f459; font-size: 0.98rem; }
.is-negative .item-val { color: #f87171; }
.item-note { font-size: 0.82rem; color: #94a3b8; margin: 0 0 0.6rem 0; line-height: 1.4; }
.item-tags { display: flex; gap: 0.4rem; }
.tag { font-size: 0.7rem; font-weight: 600; padding: 0.2rem 0.6rem; border-radius: 6px; }
.tag-tax { background: rgba(251, 191, 36, 0.12); color: #fcd34d; border: 1px solid rgba(251, 191, 36, 0.25); }
.tag-cnps { background: rgba(56, 189, 248, 0.12); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.25); }
.tag-free { background: rgba(50, 244, 89, 0.12); color: #32f459; border: 1px solid rgba(50, 244, 89, 0.25); }
.legal-notes-card { background: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 16px; padding: 1.4rem; }
.legal-notes-card h4 { font-size: 0.95rem; color: #f8fafc; margin: 0 0 0.8rem 0; }
.legal-notes-card ul { margin: 0; padding-left: 1.2rem; display: flex; flex-direction: column; gap: 0.6rem; }
.legal-notes-card li { font-size: 0.82rem; color: #94a3b8; line-height: 1.5; }
.legal-notes-card strong { color: #cbd5e1; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
@media (max-width: 992px) { .panel-card { padding: 1.5rem; } }
</style>