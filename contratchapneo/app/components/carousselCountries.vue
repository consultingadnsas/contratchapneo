<template>
    <div class="ohada-marquee">
        <div class="marquee-track">
            <div class="marquee-item" v-for="(country, index) in ohadaCountries" :key="'A'+index">
                <img :src="`https://flagcdn.com/${country.code}.svg`" class="flag-icon" :alt="country.name" />
                <span class="country-name">{{ country.name }}</span>
            </div>
            <div class="marquee-item" v-for="(country, index) in ohadaCountries" :key="'B'+index">
                <img :src="`https://flagcdn.com/${country.code}.svg`" class="flag-icon" :alt="country.name" />
                <span class="country-name">{{ country.name }}</span>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
export default {
    name: 'CarousselCountries',
    setup() {
        // Liste des pays de l'OHADA avec leurs codes ISO
        const ohadaCountries = [
            { name: 'Bénin', code: 'bj' },
            { name: 'Burkina Faso', code: 'bf' },
            { name: 'Cameroun', code: 'cm' },
            { name: 'Centrafrique', code: 'cf' },
            { name: 'Comores', code: 'km' },
            { name: 'Congo', code: 'cg' },
            { name: 'RDC', code: 'cd' },
            { name: 'Côte d\'Ivoire', code: 'ci' },
            { name: 'Gabon', code: 'ga' },
            { name: 'Guinée', code: 'gn' },
            { name: 'Guinée-Bissau', code: 'gw' },
            { name: 'Guinée Équatoriale', code: 'gq' },
            { name: 'Mali', code: 'ml' },
            { name: 'Niger', code: 'ne' },
            { name: 'Sénégal', code: 'sn' },
            { name: 'Tchad', code: 'td' },
            { name: 'Togo', code: 'tg' }
        ];

        return {
            ohadaCountries
        };
    }
};
</script>

<style scoped>
/* ── BANDEAU DÉFILANT DES PAYS OHADA ── */
.ohada-marquee {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    padding: 12px 0;
    overflow: hidden;
    display: flex;
    z-index: 20;
}

.marquee-track {
    display: flex;
    width: max-content;
    animation: scroll-marquee 35s linear infinite;
}

.marquee-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0 2.5rem;
    white-space: nowrap;
}

.flag-icon {
    width: 24px;
    height: 18px;
    object-fit: cover;
    border-radius: 3px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.country-name {
    color: #ffffff; /* Couleur de base */
    font-weight: 600;
    letter-spacing: 0.5px;
    transition: color 0.3s ease;
}

@keyframes scroll-marquee {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); } 
}
</style>