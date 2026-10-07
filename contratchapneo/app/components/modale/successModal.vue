<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="icon-container">
        <component :is="CheckCircleIcon" class="success-icon" />
      </div>
      <h3 class="modal-title">{{ title }}</h3>
      <p class="modal-message">{{ message }}</p>
      <button class="btn-primary" @click="$emit('close')">Continuer</button>
    </div>
  </div>
</template>

<script lang="ts">
import { markRaw } from 'vue';
import { CheckCircleIcon } from '@heroicons/vue/24/outline';

export default {
  name: 'SuccessModal',
  props: {
    title: {
      type: String,
      default: 'Succès'
    },
    message: {
      type: String,
      default: 'L\'opération a été effectuée avec succès.'
    }
  },
  setup() {
    return {
      CheckCircleIcon: markRaw(CheckCircleIcon)
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.4); display: flex; align-items: center; justify-content: center;
  z-index: 9999; animation: fadeIn 0.2s ease-out;
}

.modal-content {
  background: #ffffff; padding: 2rem; border-radius: 20px; text-align: center;
  width: 90%; max-width: 400px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  display: flex; flex-direction: column; align-items: center; gap: 1rem;
}

.icon-container {
  background: #dcfce7; color: #16a34a; width: 64px; height: 64px;
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  margin-bottom: 0.5rem;
}

.success-icon {
  width: 32px; height: 32px;
}

.modal-title {
  font-size: 1.4rem; font-weight: 700; color: #1e293b; margin: 0;
}

.modal-message {
  font-size: 1rem; color: #64748b; margin: 0; line-height: 1.5;
}

.btn-primary {
  margin-top: 1rem; background: #2563eb; color: #ffffff; padding: 0.8rem 2rem;
  border: none; border-radius: 50px; font-weight: 600; cursor: pointer; transition: 0.2s;
  width: 100%;
}
.btn-primary:hover {
  background: #1d4ed8;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
