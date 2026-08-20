<template>
  <Doughnut :data="chartData" :options="chartOptions" />
</template>

<script lang="ts">
import { computed } from 'vue';
import { Doughnut } from 'vue-chartjs';
import { Chart as ChartJS, Tooltip, Legend, ArcElement } from 'chart.js';

// Enregistrement spécifique pour le donut
ChartJS.register(Tooltip, Legend, ArcElement);

export default{
    name: 'StatutCharts',
    components: {
        Doughnut
    },
    props:{
        statusStats: {
            type: Object,
            default: () => ({ successful: 0, pending: 0, failed: 0 })
        }
    },

    setup(props){
        const chartData = computed(() => ({
            labels: ['Payé', 'En attente', 'Annulé / Échoué'],
            datasets: [{
                data: [props.statusStats.successful || 0, props.statusStats.pending || 0, props.statusStats.failed || 0],
                backgroundColor: ['#10b981', '#f59e0b', '#64748b'], // Vert, Orange, Gris
                borderWidth: 0,
                hoverOffset: 6
            }]
        }));

        const chartOptions = {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '78%', // Épaisseur du donut
            plugins: {
                legend: {
                position: 'bottom',
                labels: {
                    usePointStyle: true, // Cercles au lieu de carrés
                    padding: 20,
                    color: '#64748b',
                    font: { family: 'Inter', size: 13, weight: 500 }
                }
                },
                tooltip: {
                backgroundColor: '#1e293b',
                padding: 12,
                cornerRadius: 8
                }
            }
        };
        return {
            chartData,
            chartOptions
        };
    }
}
</script>