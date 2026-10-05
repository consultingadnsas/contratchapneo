<template>
    <section class="tunnel-section" aria-labelledby="tunnel-title">
        <div class="tunnel-container">
            <!-- Top bar -->
            <div class="tunnel-topbar">
                <button v-if="!submitted" type="button" class="back-link" @click="$emit('back')">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"></line><polyline points="12 19 5 12 12 5"></polyline></svg>
                    Retour
                </button>
                <span v-else class="back-link-placeholder"></span>
            </div>

            <div class="tunnel-layout">
                <!-- Main card -->
                <div class="tunnel-card">
                    <Transition name="step" mode="out-in">
                        <!-- FORMULAIRE -->
                        <form v-if="!submitted" key="form" class="step-body" novalidate @submit.prevent="submit">
                            <h2 id="tunnel-title" class="tunnel-title">Prenez rendez-vous pour votre diagnostic</h2>
                            <p class="tunnel-sub">Présentez-nous votre situation et choisissez le jour et l'heure qui vous conviennent.</p>

                            <div class="field-block">
                                <BaseInput
                                    v-model="form.fullname"
                                    label="Nom complet"
                                    placeholder="Ex : Awa Koné"
                                    autocomplete="name"
                                    required
                                />
                            </div>

                            <div class="field-block">
                                <BaseInput
                                    v-model="form.phone"
                                    type="tel"
                                    label="Numéro de téléphone"
                                    placeholder="Ex : +225 05 08 88 40 88"
                                    autocomplete="tel"
                                    required
                                />
                            </div>

                            <div class="field-block">
                                <BaseInput
                                    v-model="form.email"
                                    type="email"
                                    label="Adresse e-mail"
                                    placeholder="Ex : awa@exemple.com"
                                    autocomplete="email"
                                    :errorMessage="form.email && !emailOk ? 'Veuillez saisir une adresse e-mail valide.' : ''"
                                    required
                                />
                            </div>

                            <div class="field-block">
                                <BaseArea
                                    v-model="form.description"
                                    label="Décrivez votre problème"
                                    placeholder="Ex : On me propose de signer un contrat de bail commercial et plusieurs clauses me semblent floues…"
                                    :rows="5"
                                    required
                                />
                            </div>

                            <div class="two-cols">
                                <BaseInput
                                    v-model="form.date"
                                    type="date"
                                    label="Jour du rendez-vous"
                                    placeholder=""
                                    :min="today"
                                    :errorMessage="dateError"
                                    hint="Du lundi au vendredi, à partir d'aujourd'hui."
                                    required
                                />
                                <BaseSelect
                                    v-model="form.time"
                                    label="Heure"
                                    :placeholder="dateValid ? 'Choisir une heure' : 'Choisissez d\'abord un jour'"
                                    :disabled="!dateValid"
                                    hint="Créneaux de 9h à 17h30."
                                    required
                                >
                                    <option v-for="s in slots" :key="s.time" :value="s.time" :disabled="s.disabled">
                                        {{ s.time }}{{ s.disabled ? ' (indisponible)' : '' }}
                                    </option>
                                </BaseSelect>
                            </div>

                            <label class="consent">
                                <input v-model="form.consent" type="checkbox" />
                                <span>J'accepte que mes informations soient utilisées pour traiter ma demande. Mes échanges restent strictement confidentiels.</span>
                            </label>

                            <div class="tunnel-actions">
                                <button type="submit" class="btn-primary" :disabled="!canSubmit">
                                    Confirmer mon rendez-vous
                                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
                                </button>
                            </div>
                        </form>

                        <!-- CONFIRMATION -->
                        <div v-else key="done" class="step-body confirm">
                            <div class="check-circle">
                                <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
                            </div>
                            <h2 class="tunnel-title">Votre demande est enregistrée !</h2>
                            <p class="tunnel-sub">Un juriste vous contactera à l'heure convenue. Une confirmation vous sera envoyée à <strong class="email-strong">{{ form.email }}</strong>.</p>

                            <ul class="recap-list">
                                <li><span>Contact</span><strong>{{ form.fullname }}</strong></li>
                                <li><span>Téléphone</span><strong>{{ form.phone }}</strong></li>
                                <li><span>Rendez-vous</span><strong>{{ dateLabel }} à {{ form.time }}</strong></li>
                            </ul>

                            <button type="button" class="btn-primary" @click="$emit('back')">Retour à l'accueil du diagnostic</button>
                        </div>
                    </Transition>
                </div>

                <!-- Side info -->
                <aside class="tunnel-aside">
                    <h3>Besoin d'aide immédiate ?</h3>
                    <p>Nos juristes sont joignables directement.</p>

                    <div class="aside-loc">
                        <h4>Côte d'Ivoire</h4>
                        <a href="tel:+2250508884088" class="aside-btn">+225 05 08 88 40 88</a>
                        <a href="https://wa.me/2250508884088" target="_blank" rel="noopener" class="aside-btn wa">WhatsApp</a>
                    </div>
                    <div class="aside-loc">
                        <h4>Bénin</h4>
                        <a href="tel:+2290157218391" class="aside-btn">+229 01 57 21 83 91</a>
                        <a href="https://wa.me/2290157218391" target="_blank" rel="noopener" class="aside-btn wa">WhatsApp</a>
                    </div>
                </aside>
            </div>
        </div>
    </section>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue';
import BaseInput from '../input/BaseInput.vue';
import BaseArea from '../input/BaseArea.vue';
import BaseSelect from '../input/BaseSelect.vue';

defineEmits<{ (e: 'back'): void }>();

const submitted = ref(false);

const form = reactive({
    fullname: '',
    phone: '',
    email: '',
    description: '',
    date: '',
    time: '',
    consent: false
});

/* ---------- Date du jour (locale, calculée côté client) ---------- */
const pad = (n: number) => String(n).padStart(2, '0');
const toIso = (d: Date) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;

const today = ref('');
const now = ref(new Date());
onMounted(() => {
    now.value = new Date();
    today.value = toIso(now.value);
});

/* ---------- Validation de la date : pas dans le passé, jours ouvrés uniquement ---------- */
const dateError = computed(() => {
    if (!form.date) return '';
    if (today.value && form.date < today.value) return 'Vous ne pouvez pas choisir une date passée.';
    const wd = new Date(form.date + 'T12:00:00').getDay();
    if (wd === 0 || wd === 6) return 'Les rendez-vous ont lieu du lundi au vendredi.';
    return '';
});
const dateValid = computed(() => !!form.date && !dateError.value);

/* ---------- Créneaux : 9h → 17h30 (les heures déjà passées sont désactivées aujourd'hui) ---------- */
const slots = computed(() => {
    const out: { time: string; disabled: boolean }[] = [];
    const isToday = form.date === today.value;
    const nowMinutes = now.value.getHours() * 60 + now.value.getMinutes();
    for (let h = 9; h < 18; h++) {
        for (const m of [0, 30]) {
            out.push({
                time: `${pad(h)}h${pad(m)}`,
                disabled: isToday && h * 60 + m <= nowMinutes
            });
        }
    }
    return out;
});

/* Changer de jour réinitialise l'heure choisie */
watch(() => form.date, () => { form.time = ''; });

const emailOk = computed(() => /^\S+@\S+\.\S+$/.test(form.email));

const canSubmit = computed(() =>
    !!form.fullname.trim() &&
    !!form.phone.trim() &&
    emailOk.value &&
    form.description.trim().length >= 10 &&
    dateValid.value &&
    !!form.time &&
    form.consent
);

/* Statique : aucune requête envoyée, on affiche simplement la confirmation */
const submit = () => {
    if (!canSubmit.value) return;
    submitted.value = true;
    if (typeof window !== 'undefined') window.scrollTo({ top: 0, behavior: 'smooth' });
};

/* ---------- Récap ---------- */
const dateLabel = computed(() => {
    if (!form.date) return '';
    return new Date(form.date + 'T12:00:00').toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' });
});
</script>

<style scoped>
.tunnel-section {
    padding: 7rem 2rem 5rem;
    background: #ffffff;
}

.tunnel-container {
    max-width: 1050px;
    margin: 0 auto;
}

.tunnel-topbar {
    display: flex;
    align-items: flex-start;
    margin-bottom: 1rem;
    min-height: 32px;
}

.back-link {
    display: inline-flex;
    width: fit-content;
    align-items: flex-start;
    gap: 0.5rem;
    background: none;
    border: none;
    color: #64748b;
    font-weight: 600;
    font-size: 0.95rem;
    cursor: pointer;
    padding: 0.4rem 0.2rem;
    transition: color 0.2s, transform 0.2s;
}
.back-link:hover { color: #10507e; transform: translateX(-3px); }

.tunnel-layout {
    display: grid;
    grid-template-columns: 1fr 300px;
    gap: 2rem;
    align-items: start;
}

/* ---------- Card ---------- */
.tunnel-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 28px;
    padding: 2.5rem;
    box-shadow: 0 15px 40px rgba(15, 23, 42, 0.05);
}

.step-body { min-height: 360px; }

.tunnel-title {
    font-size: clamp(1.5rem, 3vw, 2rem);
    font-weight: 800;
    color: #0f172a;
    margin: 0 0 0.5rem;
    line-height: 1.2;
}
.tunnel-sub {
    color: #64748b;
    font-size: 1.05rem;
    margin: 0 0 2rem;
    line-height: 1.5;
}

/* ---------- Layout du formulaire (les champs sont stylés par les composants Base*) ---------- */
.two-cols {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.25rem;
    margin-bottom: 1rem;
}
.field-block { margin-bottom: 1rem; width: 100%; }


/* ---------- Consent ---------- */
.consent {
    display: flex; gap: 0.75rem; align-items: flex-start;
    margin-top: 1.5rem;
    font-size: 0.88rem; color: #64748b; line-height: 1.5;
    cursor: pointer;
}
.consent input { margin-top: 0.2rem; accent-color: #10507e; width: 18px; height: 18px; flex-shrink: 0; }

/* ---------- Actions ---------- */
.tunnel-actions { margin-top: 2rem; display: flex; justify-content: flex-end; }

.btn-primary {
    background-color: #10507e;
    color: #ffffff;
    border: none;
    padding: 1rem 2.2rem;
    font-size: 1.05rem;
    font-weight: 600;
    font-family: inherit;
    border-radius: 50px;
    cursor: pointer;
    box-shadow: 0 10px 20px rgba(16, 80, 126, 0.15);
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
}
.btn-primary:hover:not(:disabled) { transform: translateY(-3px) scale(1.02); background-color: #0c426b; box-shadow: 0 15px 25px rgba(16, 80, 126, 0.25); }
.btn-primary:disabled { background: #cbd5e1; box-shadow: none; cursor: not-allowed; }

/* ---------- Confirmation ---------- */
.confirm { text-align: center; display: flex; flex-direction: column; align-items: center; }
.check-circle {
    width: 84px; height: 84px; border-radius: 50%;
    background: #dcfce7; color: #16a34a;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 1.5rem;
    animation: pop 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
@keyframes pop { from { transform: scale(0); } to { transform: scale(1); } }
.recap-list {
    list-style: none; padding: 0; margin: 0 0 2rem;
    width: 100%; max-width: 440px;
    background: #f8fafc; border-radius: 20px; border: 1px solid #f1f5f9;
}
.recap-list li { display: flex; justify-content: space-between; gap: 1rem; padding: 0.9rem 1.4rem; border-bottom: 1px solid #f1f5f9; text-align: right; }
.recap-list li:last-child { border-bottom: none; }
.recap-list span { color: #64748b; text-align: left; }
.recap-list strong { color: #0f172a; text-transform: capitalize; }
.email-strong { text-transform: none; }

/* ---------- Aside ---------- */
.tunnel-aside {
    background: linear-gradient(145deg, #10507e 0%, #0c3e62 100%);
    border-radius: 28px;
    padding: 2rem 1.6rem;
    color: #fff;
    position: sticky;
    top: 1.5rem;
}
.tunnel-aside h3 { margin: 0 0 0.4rem; font-size: 1.25rem; font-weight: 800; }
.tunnel-aside > p { margin: 0 0 1.5rem; color: #cbd5e1; font-size: 0.95rem; }
.aside-loc { margin-bottom: 1.4rem; display: flex; flex-direction: column; gap: 0.5rem; }
.aside-loc h4 { margin: 0; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.6px; opacity: 0.8; }
.aside-btn {
    display: block; text-align: center; text-decoration: none;
    background: #fff; color: #10507e; font-weight: 700; font-size: 0.95rem;
    padding: 0.75rem 1rem; border-radius: 50px;
    transition: transform 0.25s ease;
}
.aside-btn.wa { background: #25D366; color: #fff; }
.aside-btn:hover { transform: translateY(-2px); }

/* ---------- Transition ---------- */
.step-enter-active, .step-leave-active { transition: opacity 0.25s ease, transform 0.25s ease; }
.step-enter-from { opacity: 0; transform: translateX(20px); }
.step-leave-to { opacity: 0; transform: translateX(-20px); }

/* ---------- Responsive ---------- */
@media (max-width: 899px) {
    .tunnel-section { padding: 5rem 1.2rem 3rem; }
    .tunnel-layout { grid-template-columns: 1fr; }
    .tunnel-card { padding: 1.6rem 1.2rem; border-radius: 22px; }
    .tunnel-aside { position: static; }
    .two-cols { grid-template-columns: 1fr; gap: 0; }
    .step-body { min-height: 0; }
    .tunnel-actions .btn-primary { width: 100%; justify-content: center; }
}
</style>