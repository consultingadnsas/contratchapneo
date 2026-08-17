<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="admin-modal-box modal-sm">
      <div class="modal-body text-center">
        <div class="warning-icon">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <h4 class="mt-2">Supprimer ce code ?</h4>
        <p class="gray-text">Cette action est irréversible. Les clients ne pourront plus l'utiliser.</p>
      </div>
      <div class="modal-footer justify-center">
        <button type="button" class="btn-secondary" @click="$emit('close')" :disabled="isSubmitting">Annuler</button>
        <button type="button" class="btn-danger" @click="$emit('confirm')" :disabled="isSubmitting">
           {{ isSubmitting ? 'Suppression...' : 'Oui, supprimer' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'AdminCouponDeleteModal',
  props: {
    isSubmitting: { type: Boolean, default: false }
  },
  emits: ['close', 'confirm']
});
</script>

<style scoped>
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(4px);
  display: flex; justify-content: center; align-items: center; z-index: 1000;
}
.admin-modal-box {
  background: #ffffff; border-radius: 16px; width: 100%; max-width: 500px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); overflow: hidden;
  animation: adminSlideUp 0.3s ease-out forwards;
}
.modal-sm { max-width: 400px; }
@keyframes adminSlideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.modal-body { padding: 1.5rem; display: flex; flex-direction: column; gap: 1rem; }
.text-center { text-align: center; }
.warning-icon { color: #ef4444; display: flex; justify-content: center; }
.warning-icon svg { width: 48px; height: 48px; }
.mt-2 { margin-top: 0.5rem; margin-bottom: 0; color: #0f172a; font-weight: 700; font-size: 1.2rem; }
.gray-text { color: #64748b; font-size: 0.95rem; margin: 0; }
.modal-footer { display: flex; gap: 0.8rem; padding: 1rem 1.5rem; border-top: 1px solid #e2e8f0; background: #f8fafc; }
.justify-center { justify-content: center; }
.btn-secondary { background: #ffffff; color: #475569; border: 1px solid #cbd5e1; padding: 0.6rem 1.2rem; border-radius: 8px; font-weight: 600; cursor: pointer; }
.btn-secondary:hover:not(:disabled) { background: #f1f5f9; }
.btn-danger { background: #ef4444; color: white; border: none; padding: 0.6rem 1.2rem; border-radius: 8px; font-weight: 600; cursor: pointer; }
.btn-danger:hover:not(:disabled) { background: #dc2626; }
</style>