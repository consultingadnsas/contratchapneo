<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="admin-modal-box">
      <div class="modal-header">
        <h4>{{ mode === 'add' ? 'Nouveau Code Promo' : 'Modifier le Code Promo' }}</h4>
        <button type="button" class="close-btn" @click="$emit('close')">&times;</button>
      </div>
      
      <form @submit.prevent="handleSubmit" class="modal-body">
        <div class="form-group">
          <label>Code (Ex: JURISTE2026)</label>
          <input type="text" v-model="localForm.code" required class="form-control" />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Type de réduction</label>
            <select v-model="localForm.discount_type" class="form-control">
              <option value="percentage">Pourcentage (%)</option>
              <option value="fixed">Montant fixe (FCFA)</option>
            </select>
          </div>
          <div class="form-group">
            <label>Valeur</label>
            <input type="number" step="0.01" v-model="localForm.discount_value" required class="form-control" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Valide à partir du</label>
            <input type="datetime-local" v-model="localForm.valid_from" required class="form-control" />
          </div>
          <div class="form-group">
            <label>Valide jusqu'au</label>
            <input type="datetime-local" v-model="localForm.valid_to" required class="form-control" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Nombre d'utilisations max.</label>
            <input type="number" v-model="localForm.max_usages" required class="form-control" />
          </div>
          <div class="form-group toggle-group">
            <label class="toggle-label">
              <input type="checkbox" v-model="localForm.active" />
              Code Actif
            </label>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn-secondary" @click="$emit('close')" :disabled="isSubmitting">Annuler</button>
          <button type="submit" class="btn-primary" :disabled="isSubmitting">
            {{ isSubmitting ? 'Enregistrement...' : 'Enregistrer' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, type PropType } from 'vue';
import type { Coupon } from '../../stores/AdminCouponStore'; // Ajuste le chemin si besoin

export default defineComponent({
  name: 'AdminCouponFormModal',
  props: {
    mode: { type: String as PropType<'add' | 'edit'>, required: true },
    initialData: { type: Object as PropType<Coupon>, required: true },
    isSubmitting: { type: Boolean, default: false }
  },
  emits: ['close', 'submit'],
  setup(props, { emit }) {
    // Le composant étant monté à chaque ouverture grâce au v-if du parent, 
    // on l'initialise directement.
    const localForm = ref<Coupon>({ ...props.initialData });

    const handleSubmit = () => {
      emit('submit', localForm.value);
    };

    return { localForm, handleSubmit };
  }
});
</script>

<style scoped>
.modal-overlay {
  position: fixed; 
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(15, 23, 42, 0.6); 
  backdrop-filter: blur(4px);
  display: flex; 
  justify-content: center; 
  align-items: center; 
  z-index: 1000;
  padding: 1rem;
  box-sizing: border-box;
}

.admin-modal-box {
  background: #ffffff; 
  border-radius: 16px; 
  width: 100%; 
  max-width: 520px;
  max-height: calc(100vh - 2rem);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.15); 
  overflow: hidden;
  display: flex;
  flex-direction: column;
  animation: adminSlideUp 0.3s ease-out forwards;
  box-sizing: border-box;
}

@keyframes adminSlideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.modal-header {
  display: flex; 
  justify-content: space-between; 
  align-items: center;
  padding: 1.2rem 1.5rem; 
  border-bottom: 1px solid #e2e8f0;
  flex-shrink: 0;
}

.modal-header h4 { 
  margin: 0; 
  font-size: 1.15rem; 
  color: #0f172a; 
  font-weight: 700; 
}

.close-btn { 
  background: none; 
  border: none; 
  font-size: 1.5rem; 
  cursor: pointer; 
  color: #94a3b8; 
  transition: 0.2s; 
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
}

.close-btn:hover { 
  color: #0f172a; 
  background: #f1f5f9;
}

.modal-body { 
  padding: 1.5rem; 
  display: flex; 
  flex-direction: column; 
  gap: 1rem; 
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.modal-body::-webkit-scrollbar {
  width: 6px;
}
.modal-body::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}

.form-row { 
  display: flex; 
  gap: 1rem; 
}

.form-row .form-group { 
  flex: 1; 
  min-width: 0;
}

.form-group { 
  display: flex; 
  flex-direction: column; 
  gap: 0.4rem; 
}

.form-group label { 
  font-size: 0.85rem; 
  font-weight: 600; 
  color: #475569; 
}

.form-control { 
  padding: 0.65rem 0.85rem; 
  border: 1px solid #cbd5e1; 
  border-radius: 8px; 
  font-size: 0.95rem; 
  color: #1e293b; 
  transition: all 0.2s ease; 
  width: 100%;
  box-sizing: border-box;
}

.form-control:focus { 
  outline: none; 
  border-color: #3b82f6; 
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15); 
}

.toggle-group { 
  justify-content: center; 
  align-items: flex-start; 
  padding-top: 1.8rem; 
}

.toggle-label { 
  display: inline-flex; 
  align-items: center; 
  gap: 0.6rem; 
  cursor: pointer; 
  font-weight: 600; 
  color: #0f172a; 
  font-size: 0.9rem;
}

.toggle-label input { 
  width: 20px; 
  height: 20px; 
  accent-color: #0f172a; 
  cursor: pointer; 
}

.modal-footer { 
  display: flex; 
  justify-content: flex-end; 
  gap: 0.8rem; 
  padding: 1rem 1.5rem; 
  border-top: 1px solid #e2e8f0; 
  background: #f8fafc; 
  flex-shrink: 0;
}

.btn-secondary { 
  background: #ffffff; 
  color: #475569; 
  border: 1px solid #cbd5e1; 
  padding: 0.65rem 1.25rem; 
  border-radius: 8px; 
  font-weight: 600; 
  font-size: 0.9rem;
  cursor: pointer; 
  transition: 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-secondary:hover:not(:disabled) { 
  background: #f1f5f9; 
}

.btn-primary { 
  background: #0f172a; 
  color: white; 
  border: none; 
  padding: 0.65rem 1.25rem; 
  border-radius: 8px; 
  font-weight: 600; 
  font-size: 0.9rem;
  cursor: pointer; 
  transition: 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn-primary:hover:not(:disabled) { 
  background: #334155; 
}

.btn-primary:disabled,
.btn-secondary:disabled { 
  opacity: 0.6; 
  cursor: not-allowed; 
}

/* ========================================================
   RESPONSIVE MODALE : SMARTPHONES (<= 600px)
   ======================================================== */
@media (max-width: 600px) {
  .modal-overlay {
    padding: 0.75rem;
    align-items: flex-end; /* Style sheet / bottom sheet ergonomique sur mobile */
  }

  .admin-modal-box {
    max-height: 90vh;
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
  }

  .modal-header {
    padding: 1rem 1.25rem;
  }

  .modal-body {
    padding: 1.25rem;
    gap: 0.85rem;
  }

  .form-row {
    flex-direction: column;
    gap: 0.85rem;
  }

  .toggle-group {
    padding-top: 0.25rem;
  }

  .form-control {
    font-size: 16px; /* Empêche le zoom forcé iOS Safari */
    padding: 0.7rem 0.85rem;
  }

  .modal-footer {
    padding: 0.9rem 1.25rem;
    flex-direction: column-reverse;
    gap: 0.6rem;
  }

  .btn-primary, 
  .btn-secondary {
    width: 100%;
    min-height: 44px;
    padding: 0.75rem;
  }
}
</style>