<template>
  <Line :data="chartData" :options="chartOptions" />
</template>

<script lang="ts">
import { computed } from 'vue';
import { Line } from 'vue-chartjs';
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement,
  LineElement, Title, Tooltip, Legend, Filler
} from 'chart.js';

// Enregistrement spécifique pour la courbe
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler);

export default {
  name: 'RevenueChart',
  components: {
    Line
  },
  props: {
    revenueData: {
      type: Array as () => number[],
      default: () => [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }
  },
  setup(props) {
    const formatCurrency = (val: number) => Number(val).toLocaleString('fr-FR');

    const chartData = computed(() => ({
      labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc'],
      datasets: [{
        label: 'Revenus',
        data: props.revenueData,
        borderColor: '#8b5cf6', // Violet
        borderWidth: 3,
        tension: 0.4, // Courbe lisse
        fill: true,
        backgroundColor: (context: any) => {
          const chart = context.chart;
          const { ctx, chartArea } = chart;
          if (!chartArea) return null;
          
          const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
          gradient.addColorStop(0, 'rgba(139, 92, 246, 0.4)');
          gradient.addColorStop(1, 'rgba(139, 92, 246, 0.0)');
          return gradient;
        },
        pointBackgroundColor: '#ffffff',
        pointBorderColor: '#8b5cf6',
        pointBorderWidth: 2,
        pointRadius: 0, // Points invisibles par défaut
        pointHoverRadius: 6 // Le point grossit quand on passe la souris dans la zone
      }]
    }));

    const chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      
      // ⚡️ C'EST ICI QUE LA MAGIE OPÈRE POUR LE SURVOL
      interaction: {
        mode: 'index',
        intersect: false, // N'oblige pas la souris à toucher exactement la ligne
      },
      
      plugins: {
        legend: { display: false },
        // ⚡️ STYLISATION DE LA BULLE QUI APPARAÎT (TOOLTIP)
        tooltip: {
          backgroundColor: '#1e293b',
          titleFont: { family: 'Inter', size: 13, weight: 'normal' },
          titleColor: '#cbd5e1',
          bodyFont: { family: 'Inter', size: 15, weight: 'bold' },
          bodyColor: '#ffffff',
          padding: 12,
          cornerRadius: 8,
          displayColors: false, // Cache le petit carré de couleur inutile à côté du prix
          callbacks: {
            // Personnalise le texte affiché
            label: (context: any) => `${formatCurrency(context.parsed.y)} FCFA`
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          border: { display: false },
          ticks: { color: '#94a3b8', font: { family: 'Inter' } }
        },
        y: { 
          display: false, 
          grid: { display: false },
          // On s'assure que le graphique démarre bien à 0 pour ne pas couper la courbe
          beginAtZero: true 
        }
      }
    };

    // ⚡️ Ne pas oublier d'exporter les variables pour le template
    return {
      chartData,
      chartOptions
    };
  }
};
</script>