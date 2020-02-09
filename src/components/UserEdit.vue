<template>
    <div>
        <ValidationObserver v-slot="{ invalid }" ref="observer">
        <form @submit.prevent="save" class="uk-form-stacked" uk-margin>
            <div>
                <ValidationProvider vid="username" name="Username" rules="required|alphaNum" v-slot="{ errors, classes }">
                <label class="uk-form-label">Username</label>
                <div class="uk-form-controls">
                    <input type="text" class="uk-input" v-model="user.username" :class="classes">
                    <ValidationErrors :errors="errors"/>
                </div>
                </ValidationProvider>
            </div>
            <div>
                <ValidationProvider vid="forename" name="Forename" rules="required|alpha" v-slot="{ errors, classes }">
                <label class="uk-form-label">Forename</label>
                <div class="uk-form-controls">
                    <input type="text" class="uk-input" v-model="user.forename" :class="classes">
                    <ValidationErrors :errors="errors"/>
                </div>
                </ValidationProvider>
            </div>
            <div>
                <ValidationProvider vid="surname" name="Surname" rules="required|alpha" v-slot="{ errors, classes }">
                <label class="uk-form-label">Surname</label>
                <div class="uk-form-controls">
                    <input type="text" class="uk-input" v-model="user.surname" :class="classes">
                    <ValidationErrors :errors="errors"/>
                </div>
                </ValidationProvider>
            </div>
            <div>
                <button type="submit" class="uk-button uk-button-primary uk-margin-top" :disabled="invalid">Save</button>
            </div>
        </form>
        </ValidationObserver>
    </div>
</template>

<script>
import { ValidationObserver, ValidationProvider, extend, configure, setInteractionMode } from 'vee-validate'
import { required, alpha_num as alphaNum, alpha } from 'vee-validate/dist/rules'
import ValidationErrors from '@/components/ValidationErrors'

setInteractionMode('eager')

extend('required', required)
extend('alphaNum', alphaNum)
extend('alpha', alpha)

configure({
  classes: {
    valid: 'uk-form-success',
    invalid: 'uk-form-danger'
  }
})

export default {

    name: 'user-edit',

    props: {
        user: {
            type: Object,
            default: () => ({
                id: null,
                username: '',
                surname: '',
                forename: ''
            })
        }
    },

    methods: {
        save () {
            if (this.user.id === null) {
                this.$securedApi.put('/user', this.user)
                    .then(res => {
                        this.UI.notification('Created user.')
                    })
            } else {
                this.$securedApi.post(`/user/${this.user.id}`, this.user)
                    .then(res => {
                        this.$store.updateCurrentUser()
                        this.UI.notification('Saved user.')
                    })
            }
        }
    },

    components: {
        ValidationObserver,
        ValidationProvider,
        ValidationErrors
    }
}
</script>
