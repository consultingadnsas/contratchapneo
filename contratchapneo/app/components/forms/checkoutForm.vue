<template>
    <form class="w-full flex flex-col gap-2">
        <BaseInput label="Nom complet" name="name" type="text" placeholder="Entrez votre nom"/>
        <BaseInput label="Email" name="email" type="email" placeholder="Entrez votre adresse email"/>
        <BaseInput label="Numéro de téléphone" name="phoneNumber" type="tel" placeholder="Entrez votre numéro de téléphone"/>
        <checkoutButton label="Commander"/>
    </form>
</template>

<script>
import BaseInput from '../input/BaseInput.vue'
import checkoutButton from '../buttons/checkoutButton.vue'
import {ref} from 'vue'
export default {
    components:{
        BaseInput,
        checkoutButton
    }
}
</script>

<style>

</style>