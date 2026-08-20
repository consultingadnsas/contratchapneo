<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>

<script lang="ts">
import { computed } from 'vue';
import { Bar } from 'vue-chartjs';
import {
  Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend
} from 'chart.js';

// Enregistrement spécifique pour le graphique en barres
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default {
    name:'demandChart',
    components: {
        Bar
    },
    props: {
        demandData: {
            type: Object,
            default: () => ({
            customContracts: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            revisions: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            })
        }
    },
    setup(props) {
        const chartData = computed(() => ({
            labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc'],
            datasets: [
                {
                label: 'Sur-Mesure',
                data: props.demandData.customContracts,
                backgroundColor: '#f59e0b', // Orange
                borderRadius: 4, // Bords arrondis pour le style
                barPercentage: 0.6,
                categoryPercentage: 0.8
                },
                {
                label: 'Révisions',
                data: props.demandData.revisions,
                backgroundColor: '#3b82f6', // Bleu
                borderRadius: 4,
                barPercentage: 0.6,
                categoryPercentage: 0.8
                }
            ]
        }));

        const chartOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                position: 'top',
                align: 'end',
                labels: {
                    usePointStyle: true,
                    boxWidth: 8,
                    color: '#64748b',
                    font: { family: 'Inter', size: 13, weight: 500 }
                }
                },
                tooltip: {
                backgroundColor: '#1e293b',
                padding: 12,
                cornerRadius: 8,
                titleFont: { family: 'Inter', size: 13 },
                bodyFont: { family: 'Inter', size: 14, weight: 'bold' }
                }
            },
            scales: {
                x: {
                grid: { display: false },
                border: { display: false },
                ticks: { color: '#94a3b8', font: { family: 'Inter' } }
                },
                y: {
                grid: { color: '#f1f5f9', strokeDasharray: [4, 4] }, // Lignes pointillées légères
                border: { display: false },
                ticks: {
                    color: '#94a3b8',
                    stepSize: 1, // On compte des unités (1, 2, 3 demandes...)
                    font: { family: 'Inter' }
                },
                beginAtZero: true
                }
            }
        };
        return {
            chartData,
            chartOptions
        }
    }
}
</script>