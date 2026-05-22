<template>
    <div class="view-modale" @click.self="$emit('close')">

        <div class="modal-content">

            <button class="close-btn" @click="$emit('close')">
            ✕
            </button>

            <client-only>
                <vue-pdf-embed
                    :source="pdfSource"
                    class="pdf-preview"
                />
            </client-only>

        </div>

    </div>
</template>

<script setup>
import { ref } from 'vue';
import VuePdfEmbed from 'vue-pdf-embed';

const pdfSource = ref('/lettre de motivation Angui.pdf');
</script>

<style scoped>

.view-modale {
  position: fixed;
  inset: 0;

  background: rgba(0,0,0,0.7);

  display: flex;
  justify-content: center;
  align-items: center;

  z-index: 999;
}

.modal-content {
  position: relative;

  width: 90%;
  max-width: 900px;

  height: 90vh;

  background: white;
  border-radius: 12px;

  overflow: hidden;
}

.close-btn {
  position: absolute;

  top: 10px;
  right: 10px;

  z-index: 10;

  width: 35px;
  height: 35px;

  border: none;
  border-radius: 50%;

  background: black;
  color: white;

  cursor: pointer;
}

.pdf-preview {
  width: 100%;
  height: 100%;
  overflow: auto;
}

</style>