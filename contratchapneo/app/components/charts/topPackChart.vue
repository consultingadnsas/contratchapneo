<template>
  <Pie :data="chartData" :options="chartOptions" />
</template>

<script lang="ts">
import { computed } from 'vue';
import { Pie } from 'vue-chartjs';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

// Enregistrement des éléments spécifiques au Pie Chart
ChartJS.register(ArcElement, Tooltip, Legend);

export default {
    name:'topPackChart',
    components:{
        Pie
    },
    props: {
        topData: { 
            type: Object, 
            default: () => ({ labels: [], data: [] }) 
        } 
    },
    setup(props) {
        const chartData = computed(() => ({
            labels: props.topData.labels,
            datasets: [{
                label: 'Ventes',
                data: props.topData.data,
                // Une belle palette de nuances indigo et violettes
                backgroundColor: ['#4f46e5', '#6366f1', '#818cf8', '#a5b4fc', '#e0e7ff'],
                borderWidth: 2,
                borderColor: '#ffffff', // Bordure blanche pour détacher les parts
                hoverOffset: 8 // La part ressort quand on passe la souris
            }]
        }));

        const chartOptions = {
            responsive: true, 
            maintainAspectRatio: false,
            plugins: {
                legend: { 
                position: 'right', // Légende sur le côté pour ne pas écraser le graphique
                labels: {
                    usePointStyle: true,
                    padding: 15,
                    color: '#64748b',
                    font: { family: 'Inter', size: 12 }
                }
                },
                tooltip: { 
                backgroundColor: '#1e293b', 
                padding: 12, 
                cornerRadius: 8 
                }
            }
        };
        return{
            chartData,
            chartOptions
        }
    }
}
</script>