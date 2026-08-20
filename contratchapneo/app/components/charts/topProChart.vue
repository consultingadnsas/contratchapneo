<template>
  <PolarArea :data="chartData" :options="chartOptions" />
</template>

<script lang="ts">
import { computed } from 'vue';
import { PolarArea } from 'vue-chartjs';
import { Chart as ChartJS, RadialLinearScale, ArcElement, Tooltip, Legend } from 'chart.js';

// Enregistrement des éléments spécifiques au Polar Area
ChartJS.register(RadialLinearScale, ArcElement, Tooltip, Legend);

export default {
    name:'topProChart',
    components:{
        PolarArea
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
                label: 'Sollicitations',
                data: props.topData.data,
                // Une belle palette de nuances émeraude et turquoise
                backgroundColor: [
                'rgba(20, 184, 166, 0.8)', 
                'rgba(45, 212, 191, 0.7)', 
                'rgba(94, 234, 212, 0.6)', 
                'rgba(153, 246, 228, 0.5)', 
                'rgba(204, 251, 241, 0.4)'
                ],
                borderColor: '#ffffff',
                borderWidth: 2
            }]
        }));

        const chartOptions = {
            responsive: true, 
            maintainAspectRatio: false,
            scales: {
                r: {
                ticks: { display: false }, // Cache les chiffres sur les cercles intérieurs
                grid: { color: '#f1f5f9' } // Cercles de fond subtils
                }
            },
            plugins: {
                legend: { 
                position: 'right',
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
        return {
            chartData,
            chartOptions
        }
    }
}
  
</script>