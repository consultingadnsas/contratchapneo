<template>
    <!-- ⚡️ NOUVEAU : On ajoute un ID unique pour cibler cet élément -->
    <div id="bordereau-pdf-content" class="pdf-container">
        <div class="bordereau-header">
            <h2>Bordereau de Simulation des Droits</h2>
            <p>Document généré le {{ currentDate }}</p>
        </div>
        
        <div class="bordereau-section">
            <h3>1. Détail des Indemnités</h3>
            <table class="bordereau-table">
                <thead>
                    <tr>
                        <th>Rubrique</th>
                        <th style="text-align: right;">Montant (FCFA)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(item, index) in breakdown" :key="index">
                        <td>
                            <strong>{{ item.label }}</strong><br>
                            <span style="font-size: 0.85em; color: #555;">{{ item.description }}</span>
                        </td>
                        <td style="text-align: right; white-space: nowrap;">
                            {{ formatCurrency(item.amount) }}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bordereau-section">
            <h3>2. Récapitulatif Global</h3>
            <table class="bordereau-table total-table">
                <!-- ⚡️ AJOUT DE LA BALISE TBODY ICI -->
                <tbody>
                    <tr>
                        <td>Total Brut</td>
                        <td style="text-align: right;">{{ formatCurrency(totalGrossAmount) }}</td>
                    </tr>
                    <tr v-if="cnpsEmployeeDeduction > 0">
                        <td>Retenue CNPS Salariale (6,3%)</td>
                        <td style="text-align: right; color: red;">- {{ formatCurrency(cnpsEmployeeDeduction) }}</td>
                    </tr>
                    <tr class="final-total">
                        <td>NET ESTIMÉ À PERCEVOIR</td>
                        <td style="text-align: right;">{{ formatCurrency(netAmount) }}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bordereau-footer">
            <p><strong>Note :</strong> {{ summaryMessage }}</p>
            <p style="font-size: 0.85em; margin-top: 20px; text-align: center;">
                Simulation générée à titre indicatif selon le Code du Travail de Côte d'Ivoire.
            </p>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType, computed } from 'vue';

interface BreakdownItem {
    label: string;
    amount: number;
    description: string;
    taxable: boolean;
    cnps: boolean;
}

export default defineComponent({
    name: 'LawCalculBordereau',
    props: {
        breakdown: { type: Array as PropType<BreakdownItem[]>, required: true },
        totalGrossAmount: { type: Number, required: true },
        cnpsEmployeeDeduction: { type: Number, required: true },
        netAmount: { type: Number, required: true },
        summaryMessage: { type: String, required: true }
    },
    setup() {
        const formatCurrency = (value: number): string => {
            return new Intl.NumberFormat('fr-FR').format(Math.round(value)) + ' FCFA';
        };

        const currentDate = computed(() => {
            return new Date().toLocaleDateString('fr-FR', {
                year: 'numeric', month: 'long', day: 'numeric',
                hour: '2-digit', minute: '2-digit'
            });
        });

        return { formatCurrency, currentDate };
    }
});
</script>

<style scoped>
/* ⚡️ NOUVEAU : Plus de @media print ! On positionne le conteneur hors écran */
.pdf-container {
    position: absolute;
    top: 0;
    left: 0;
    z-index: -999;
    opacity: 0.01; 
    pointer-events: none;
    width: 720px; /* Largeur fixe pour garantir de belles proportions sur le PDF A4 */
    box-sizing: border-box;
    background: #ffffff;
    color: #000000;
    padding: 40px;
    font-family: Arial, sans-serif;
}

.bordereau-header { text-align: center; margin-bottom: 2rem; border-bottom: 2px solid #000; padding-bottom: 1rem; }
.bordereau-header h2 { font-size: 24px; margin: 0 0 10px 0; color: #000; }
.bordereau-section { margin-bottom: 2rem; }
.bordereau-section h3 { font-size: 16px; border-bottom: 1px solid #ccc; padding-bottom: 5px; margin-bottom: 10px; color: #000; }

.bordereau-table { width: 100%; border-collapse: collapse; margin-bottom: 1rem; }
.bordereau-table th, .bordereau-table td { border: 1px solid #ddd; padding: 10px; text-align: left; }
.bordereau-table th { background-color: #f3f4f6; color: #000; }

.total-table { width: 60%; margin-left: auto; }
.final-total { font-weight: bold; font-size: 1.1em; background-color: #e5e7eb; }

.bordereau-footer { margin-top: 3rem; font-size: 0.9em; color: #333; }
.pdf-container, 
.pdf-container * {
    /* Écrase les couleurs par défaut invisibles de Tailwind */
    border-color: #e5e7eb !important; 
    outline-color: transparent !important;
    text-decoration-color: transparent !important;
    box-shadow: none !important;
}

/* On s'assure de garder la bonne couleur pour le tableau */
.bordereau-table th, 
.bordereau-table td { 
    border-color: #ddd !important; 
}
</style>