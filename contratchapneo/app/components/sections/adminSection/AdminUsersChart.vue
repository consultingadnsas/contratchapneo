<template>
  <div class="charts-row">
    <!-- Graphique Répartition (Doughnut) -->
    <div class="chart-container">
      <h4 class="chart-title">Répartition des utilisateurs</h4>
      <div class="chart-wrapper">
        <Doughnut :data="doughnutData" :options="commonOptions" />
      </div>
    </div>

    <!-- Graphique Évolution (Line) -->
    <div class="chart-container evolution-container">
      <h4 class="chart-title">Évolution des inscriptions</h4>
      <div class="chart-wrapper">
        <Line :data="lineData" :options="commonOptions" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { computed } from 'vue';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Title, Filler } from 'chart.js';
import { Doughnut, Line } from 'vue-chartjs';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Title, Filler);

export default {
  name: 'AdminUsersChart',
  components: { Doughnut, Line },
  props: {
    users: {
      type: Array,
      required: true
    }
  },
  setup(props) {
    const doughnutData = computed(() => {
      const activePack = props.users.filter((u: any) => u.has_active_pack).length;
      const hadPack = props.users.filter((u: any) => u.has_pack && !u.has_active_pack).length;
      const noPack = props.users.filter((u: any) => !u.has_pack).length;

      return {
        labels: ['Pack Actif', 'Pack Expiré', 'Aucun pack'],
        datasets: [
          {
            backgroundColor: ['#166534', '#eab308', '#94a3b8'],
            data: [activePack, hadPack, noPack]
          }
        ]
      };
    });

    const lineData = computed(() => {
      // Trier les utilisateurs par date d'inscription
      const sortedUsers = [...props.users].filter(u => u.date_joined).sort((a: any, b: any) => new Date(a.date_joined).getTime() - new Date(b.date_joined).getTime());
      
      // Regrouper par mois/année (ex: "Sept 2023")
      const countsByMonth: Record<string, number> = {};
      
      sortedUsers.forEach((u: any) => {
        const date = new Date(u.date_joined);
        const monthYear = date.toLocaleDateString('fr-FR', { month: 'short', year: 'numeric' });
        if (!countsByMonth[monthYear]) countsByMonth[monthYear] = 0;
        countsByMonth[monthYear]++;
      });

      return {
        labels: Object.keys(countsByMonth),
        datasets: [
          {
            label: 'Nouvelles inscriptions',
            borderColor: '#3b82f6',
            backgroundColor: 'rgba(59, 130, 246, 0.2)',
            data: Object.values(countsByMonth),
            tension: 0.3,
            fill: true
          }
        ]
      };
    });

    const commonOptions = {
      responsive: true,
      maintainAspectRatio: false
    };

    return { doughnutData, lineData, commonOptions };
  }
}
</script>

<style scoped>
.charts-row {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 2rem;
  width: 100%;
  justify-content: center;
}
.chart-container {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  margin-top: 1rem;
  width: 100%;
  max-width: 400px;
  flex: 1;
  min-width: 300px;
}
.evolution-container {
  max-width: 600px;
}
.chart-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1rem;
  text-align: center;
}
.chart-wrapper {
  height: 250px;
  position: relative;
}
</style>