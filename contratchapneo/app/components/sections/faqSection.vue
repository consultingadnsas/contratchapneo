<template>
  <section class="faq-support-section">
    
    <!-- EN-TÊTE FAQ -->
    <div class="faq-header">
      <h2 class="title">Questions Fréquemment Posées</h2>
      <p class="subtitle">Tout ce que vous devez savoir sur nos contrats et nos services juridiques.</p>
    </div>

    <!-- LISTE DES QUESTIONS (ACCORDÉON EN 2 COLONNES) -->
    <div class="faq-accordion">
      <div 
        class="faq-item" 
        v-for="(faq, index) in faqs" 
        :key="index"
        :class="{ 'is-open': faq.isOpen }"
      >
        <button class="faq-question" @click="toggleFaq(index)">
          <span class="question-text">{{ faq.question }}</span>
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            fill="none" 
            viewBox="0 0 24 24" 
            stroke-width="2" 
            stroke="currentColor" 
            class="chevron-icon"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
          </svg>
        </button>
        
        <div class="faq-answer-wrapper">
          <div class="faq-answer">
            <p>{{ faq.answer }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- BLOC CONTACT (Bandeau horizontal) -->
    <div class="support-contact-block">
      <div class="contact-text">
        <h3>Vous avez d'autres questions spécifiques ?</h3>
        <p>Contactez-nous pour être guidé par nos experts.</p>
      </div>

      <div class="action-buttons">
        <!-- Bouton Appel -->
        <a href="tel:+2250779101170" class="contact-btn btn-call">
          <span class="pulse-dot"></span>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 0 0 2.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 0 1-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 0 0-1.091-.852H4.5A2.25 2.25 0 0 0 2.25 4.5v2.25Z" />
          </svg>
          <span class="btn-text">Appeler ici</span>
        </a>

        <!-- Bouton WhatsApp (Icône seule) -->
        <a href="https://wa.me/2250779101170" target="_blank" rel="noopener noreferrer" class="contact-btn btn-whatsapp icon-only" title="Discuter sur WhatsApp">
          <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" viewBox="0 0 16 16">
            <path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c-.003 1.398.366 2.76 1.062 3.964L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z"/>
          </svg>
        </a>
      </div>
    </div>

  </section>
</template>

<script lang="ts">
import { ref } from 'vue';

export default {
  name: 'FaqSupport',
  setup() {
    const faqs = ref([
      { question: "Les modèles de contrats sont-ils conformes au droit OHADA ?", answer: "Absolument. Tous nos contrats sont rédigés et rigoureusement vérifiés par des experts juridiques qualifiés pour garantir leur parfaite conformité avec la législation OHADA en vigueur.", isOpen: false },
      { question: "Comment vais-je recevoir mon contrat après le paiement ?", answer: "Dès la validation de votre paiement, vous pourrez télécharger immédiatement votre contrat depuis la page de confirmation. Un lien de téléchargement vous sera également envoyé par email.", isOpen: false },
      { question: "Sous quel format les contrats sont-ils fournis ?", answer: "Nos modèles sont fournis au format Microsoft Word (.docx). Vous pouvez ainsi les modifier facilement pour les adapter aux spécificités de votre entreprise.", isOpen: false },
      { question: "Proposez-vous des services de rédaction sur-mesure ?", answer: "Oui. Si nos modèles standards ne couvrent pas vos besoins, vous pouvez faire une demande de rédaction sur-mesure ou d'audit contractuel directement depuis notre plateforme.", isOpen: false },
      { question: "Le paiement en ligne est-il totalement sécurisé ?", answer: "Oui, la sécurité est notre priorité. Nous utilisons des passerelles de paiement certifiées (Mobile Money et cartes bancaires) qui cryptent vos données de bout en bout.", isOpen: false },
      { question: "Puis-je obtenir de l'aide pour remplir mon contrat ?", answer: "Bien sûr. Nos modèles incluent des annotations pour vous guider. Si vous avez besoin d'une assistance supplémentaire, vous pouvez réserver une session de conseil avec nos juristes partenaires.", isOpen: false }
    ]);

    const toggleFaq = (index: number) => {
      faqs.value.forEach((faq, i) => {
        if (i === index) {
          faq.isOpen = !faq.isOpen;
        } else {
          faq.isOpen = false; 
        }
      });
    };

    return { faqs, toggleFaq };
  }
}
</script>

<style scoped>
/* ── Variables & Conteneur Principal ────────────────────────── */
.faq-support-section {
  --color-primary: #156ca9;
  --color-primary-light: #e0f2fe;
  --color-success: #25D366; 
  --color-dark: #1e293b;
  --color-gray: #64748b;
  --border-color: #e2e8f0;

  width: 100%;
  max-width: 1200px; /* Élargi pour les 2 colonnes */
  margin: 0 auto;
  padding: 3rem 1.5rem;
  font-family: 'Inter', sans-serif;
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

/* ── En-tête FAQ ───────────────────────────────────────────── */
.faq-header { text-align: center; }
.title { font-size: clamp(1.8rem, 4vw, 2.2rem); font-weight: 800; color: var(--color-dark); margin: 0 0 0.8rem 0; }
.subtitle { font-size: 1.05rem; color: var(--color-gray); margin: 0; }

/* ── Liste Accordéon (GRILLE 2 COLONNES) ───────────────────── */
.faq-accordion {
  display: grid;
  grid-template-columns: 1fr; /* Mobile: 1 colonne */
  gap: 1.5rem;
  align-items: start; /* Évite que la case d'à côté s'étire quand on en ouvre une */
}

@media (min-width: 768px) {
  .faq-accordion {
    grid-template-columns: repeat(2, 1fr); /* Bureau: 2 colonnes */
  }
}

.faq-item {
  background-color: #ffffff;
  border: 1px solid var(--border-color);
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
}
.faq-item:hover { border-color: var(--color-primary); }
.faq-item.is-open { border-color: var(--color-primary); box-shadow: 0 10px 20px rgba(21, 108, 169, 0.08); }

.faq-question {
  width: 100%; display: flex; justify-content: space-between; align-items: center;
  padding: 1.2rem 1.5rem; background: transparent; border: none; cursor: pointer; text-align: left;
}
.question-text { font-size: 1.05rem; font-weight: 700; color: var(--color-dark); padding-right: 1.5rem; transition: color 0.3s; }
.faq-item.is-open .question-text { color: var(--color-primary); }

.chevron-icon { width: 20px; height: 20px; color: var(--color-gray); transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1); flex-shrink: 0; }
.faq-item.is-open .chevron-icon { transform: rotate(180deg); color: var(--color-primary); }

.faq-answer-wrapper { display: grid; grid-template-rows: 0fr; transition: grid-template-rows 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
.faq-item.is-open .faq-answer-wrapper { grid-template-rows: 1fr; }
.faq-answer { overflow: hidden; }
.faq-answer p { padding: 0 1.5rem 1.2rem 1.5rem; margin: 0; color: var(--color-gray); line-height: 1.6; font-size: 0.95rem; }

/* ── Bloc Contact (Tout sur la même ligne) ─────────────────── */
.support-contact-block {
  background-color: var(--color-primary-light);
  border-radius: 20px;
  padding: 2rem 2.5rem;
  display: flex;
  flex-direction: column; /* Mobile: empilé */
  align-items: center;
  text-align: center;
  gap: 1.5rem;
}

@media (min-width: 992px) {
  .support-contact-block {
    flex-direction: row; /* Bureau: Sur la même ligne */
    justify-content: space-between;
    text-align: left;
  }
}

.contact-text h3 { font-size: 1.3rem; font-weight: 800; color: var(--color-primary); margin: 0 0 0.4rem 0; }
.contact-text p { font-size: 0.95rem; color: var(--color-primary); margin: 0; }

.action-buttons {
  display: flex;
  flex-direction: row; /* Boutons toujours alignés horizontalement */
  align-items: center;
  gap: 1rem;
}

/* Boutons */
.contact-btn {
  display: flex; justify-content: center; align-items: center; gap: 0.75rem;
  padding: 0.85rem 1.5rem; border-radius: 50px; text-decoration: none;
  font-weight: 700; font-size: 0.95rem; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease, opacity 0.3s ease;
}
.contact-btn:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15); }

/* Spécificités des boutons */
.btn-call { background-color: #ffffff; color: var(--color-primary); }

.btn-whatsapp { background-color: var(--color-success); color: #ffffff; }
.btn-whatsapp:hover { background-color: #1ea952; }

/* Pastille WhatsApp (Icône uniquement) */
.icon-only {
  padding: 0;
  width: 50px;
  height: 50px;
  border-radius: 50%; /* Bouton parfaitement rond */
  justify-content: center;
}

.size-6 { width: 20px; height: 20px; }

/* Animation Point Vert */
.pulse-dot { width: 10px; height: 10px; background-color: var(--color-success); border-radius: 50%; position: relative; }
.pulse-dot::after { content: ''; position: absolute; width: 100%; height: 100%; background-color: var(--color-success); border-radius: 50%; top: 0; left: 0; animation: ping 2s cubic-bezier(0, 0, 0.2, 1) infinite; }
@keyframes ping { 75%, 100% { transform: scale(2.5); opacity: 0; } }
</style>