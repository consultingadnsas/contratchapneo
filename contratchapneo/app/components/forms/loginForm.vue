<template>
    <form class="login-form">

        <h3>Se connecter</h3>

        <template v-if="steps==1">
            <radioButtonVue 
                :v-model="registrationForm.user_type"
            />
        </template>

        <formButton label="Se connecter" :isLoading="true"/>
    </form>
</template>

<script>
import formButton from '../buttons/formButton.vue';
import radioButtonVue from '../buttons/radioButton.vue';
import BaseInputVue from '../input/BaseInput.vue';

import type {User} from '../../stores/authStore'
import {ref} from 'vue';

export default {

    components:{
        BaseInputVue,
        radioButtonVue,
        formButton
    },

    setup(props, {emit}){
        
        const steps = ref<number>(1);

        const registrationForm = reactive<User>({
            id: '',
            username: '',
            first_name: '',
            last_name: '',
            password: '',
            email: '',
            phone_number: '',
            user_type: ''
        })

        return {
            steps,
            registrationForm
        }


    }

}
</script>

<style scoped>

.login-form{
    width: 100%;
}

</style>