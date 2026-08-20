<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>

<script lang="ts">
import { computed } from 'vue';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default {
    name:'packChart',
    components: {
        Bar
    },
    props: {
         chartDataArray: { 
            type: Array as () => number[], 
            default: () => [0,0,0,0,0,0,0,0,0,0,0,0] 
        }
    },

    setup(props) {
        const chartData = computed(() => ({
        labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc'],
        datasets: [{
            label: 'Packs vendus',
            data: props.chartDataArray,
            backgroundColor: '#6366f1', // Indigo clair
            borderRadius: 6,
            barPercentage: 0.5
        }]
        }));

        const chartOptions = {
        responsive: true, maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: { backgroundColor: '#1e293b', padding: 12, cornerRadius: 8 }
        },
        scales: {
            x: { grid: { display: false }, border: { display: false }, ticks: { color: '#94a3b8', font: { family: 'Inter' } } },
            y: { grid: { color: '#f1f5f9', strokeDasharray: [4, 4] }, border: { display: false }, ticks: { color: '#94a3b8', stepSize: 1, font: { family: 'Inter' } }, beginAtZero: true }
        }
        };
        return {
            chartData,
            chartOptions
        };
    }
}
</script>