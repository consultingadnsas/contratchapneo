<template>
    <div class="panel-card panel-left">
        <div class="panel-header">
            <h3>Paramètres du Contrat & Salaires</h3>
        </div>

        <form @submit.prevent="$emit('submit')" class="calc-form">
            <div class="grid-2">
                <BaseSelect v-model="modelValue.contractType" id="contractType" label="Type de Contrat" :options="contractOptions" required />
                <BaseSelect v-model="modelValue.categoriePro" id="categoriePro" label="Catégorie Pro" :options="categorieOptions" required />
            </div>

            <BaseSelect v-model="modelValue.motif" id="motif" label="Motif de la rupture" :options="filteredMotifOptions" required />

            <div class="grid-2">
                <BaseInput v-model="modelValue.startDate" id="startDate" type="date" label="Date d'embauche" required />
                <BaseInput v-model="modelValue.endDate" id="endDate" type="date" label="Date de rupture" required />
            </div>

            <template v-if="modelValue.contractType === 'cdi'">
                <div class="grid-2">
                    <BaseInput v-model="modelValue.baseSalary" id="baseSalary" type="number" min="0" label="Salaire de base (FCFA)" placeholder="250000" required />
                    <BaseInput v-model="modelValue.averageSalary" id="averageSalary" type="number" min="0" label="Salaire moyen (12 mois)" placeholder="310000" required />
                </div>
                <div class="toggle-card" v-if="modelValue.motif !== 'faute_lourde' && modelValue.motif !== 'deces'">
                    <label class="toggle-label">
                        <input type="checkbox" v-model="modelValue.preavisExecute" />
                        <span>Le préavis a été exécuté / travaillé par le salarié</span>
                    </label>
                </div>
            </template>

            <template v-if="modelValue.contractType === 'cdd'">
                <BaseInput v-model="modelValue.totalGrossSalary" id="totalGrossSalary" type="number" min="0" label="Rémunération brute totale perçue (FCFA)" placeholder="3000000" required />
                
                <BaseInput v-if="modelValue.motif === 'rupture_anticipee_employeur'" v-model="modelValue.remainingMonths" id="remainingMonths" type="number" min="1" label="Mois restants jusqu'au terme prévu" placeholder="3" required />
                
                <BaseInput v-if="modelValue.motif === 'rupture_anticipee_salarie'" v-model="modelValue.employerDamages" id="employerDamages" type="number" min="0" label="Dommages réclamés par l'employeur (FCFA) - Optionnel" placeholder="150000" />
            </template>

            <div class="grid-2">
                <BaseInput v-model="modelValue.daysWorkedInLastMonth" id="daysWorkedInLastMonth" type="number" min="0" max="30" label="Jours travaillés (mois de sortie)" placeholder="15" />
                <BaseInput v-model="modelValue.remainingLeaveDays" id="remainingLeaveDays" type="text" inputmode="decimal" label="Congés payés restants (jours)" placeholder="15,5" />
            </div>

            <div class="toggle-card">
                <label class="toggle-label">
                    <input type="checkbox" v-model="modelValue.isDeclaredCNPS" />
                    <span>Travailleur déclaré CNPS (Retenue 6,3 % active)</span>
                </label>
            </div>

            <div v-if="errorMessage" class="alert error">{{ errorMessage }}</div>

            <main-button label="Calculer mes droits & indemnités" :isLoading="isCalculating" type="submit" class="submit-btn" />
        </form>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';
import BaseInput from '../input/BaseInput.vue';
import BaseSelect from '../input/BaseSelect.vue';
import mainButton from '../buttons/mainButton.vue';

export default defineComponent({
    name: 'LawCalculForm',
    components: { BaseInput, BaseSelect, mainButton },
    props: {
        modelValue: { type: Object as PropType<any>, required: true },
        isCalculating: { type: Boolean, default: false },
        errorMessage: { type: String, default: '' },
        contractOptions: { type: Array, required: true },
        categorieOptions: { type: Array, required: true },
        filteredMotifOptions: { type: Array, required: true }
    },
    emits: ['submit', 'update:modelValue']
});
</script>

<style scoped>
.panel-card { background: rgba(255, 255, 255, 0.025); backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 24px; padding: 2.2rem; box-shadow: 0 20px 50px rgba(0, 0, 0, 0.35); }
.panel-header { display: flex; align-items: center; gap: 0.8rem; border-bottom: 1px solid rgba(255, 255, 255, 0.08); padding-bottom: 1.2rem; margin-bottom: 1.5rem; }
.panel-header h3 { font-size: 1.15rem; font-weight: 700; color: #f8fafc; margin: 0; }
.calc-form { display: flex; flex-direction: column; gap: 1.25rem; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; width: 100%; }
.toggle-card { background: rgba(0, 0, 0, 0.25); border: 1px solid rgba(255, 255, 255, 0.07); border-radius: 12px; padding: 0.9rem 1.1rem; }
.toggle-label { display: flex; align-items: center; gap: 0.8rem; cursor: pointer; font-size: 0.9rem; color: #cbd5e1; }
.toggle-label input[type="checkbox"] { width: 1.15rem; height: 1.15rem; accent-color: #32f459; cursor: pointer; }
:deep(.form-input), :deep(.form-select) { background-color: rgba(0, 0, 0, 0.3) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; color: white !important; border-radius: 12px !important; padding: 0.8rem 1rem !important; font-size: 0.92rem !important; }
:deep(.form-input:focus), :deep(.form-select:focus) { border-color: #32f459 !important; box-shadow: 0 0 0 3px rgba(50, 244, 89, 0.15) !important; }
:deep(.input-label) { color: #94a3b8 !important; margin-bottom: 0.35rem !important; font-size: 0.85rem !important; font-weight: 500 !important; }
.submit-btn { width: 100%; padding: 1.15rem; border-radius: 14px; font-size: 1.02rem; font-weight: 700; margin-top: 0.8rem; transition: all 0.3s ease; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3); }
.submit-btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 15px 30px rgba(50, 244, 89, 0.25); }
.alert { padding: 0.9rem; border-radius: 12px; font-size: 0.9rem; font-weight: 500; text-align: center; }
.alert.error { background: rgba(239, 68, 68, 0.15); color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.3); }
@media (max-width: 992px) { .grid-2 { grid-template-columns: 1fr; } .panel-card { padding: 1.5rem; } }
</style>