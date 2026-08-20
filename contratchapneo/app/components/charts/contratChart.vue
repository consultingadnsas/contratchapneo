<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>

<script lang="ts">
import { computed } from 'vue';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default {
    name:'contratChart',
    components:{
        Bar
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
                backgroundColor: '#8b5cf6', // Violet
                borderRadius: 4,
                barPercentage: 0.6
            }]
            })
        );

        const chartOptions = {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y', // 👈 C'est ce qui rend le graphique horizontal
            plugins: {
                legend: { display: false },
                tooltip: { backgroundColor: '#1e293b', padding: 12, cornerRadius: 8 }
            },
            scales: {
                x: { 
                grid: { color: '#f1f5f9', strokeDasharray: [4, 4] }, 
                border: { display: false }, 
                ticks: { color: '#94a3b8', stepSize: 1, font: { family: 'Inter' } },
                beginAtZero: true 
                },
                y: { 
                grid: { display: false }, 
                border: { display: false }, 
                ticks: { color: '#1e293b', font: { family: 'Inter', weight: 600 } } 
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