<template>
    <div>
        <ValidationObserver v-slot="{ invalid }" ref="observer">
        <form @submit.prevent="change" class="uk-form-stacked" uk-margin>
            <div>
                <label class="uk-form-label">Email</label>
                <div class="uk-form-controls">
                    <input type="email" class="uk-input" :value="email" disabled>
                </div>
            </div>
            <div>
                <ValidationProvider vid="email" name="Email" rules="required|email" v-slot="{ errors, classes }">
                <label class="uk-form-label">New email</label>
                <div class="uk-form-controls">
                    <input type="email" class="uk-input" v-model="newEmail" :class="classes">
                    <ValidationErrors :errors="errors"/>
                </div>
                </ValidationProvider>
            </div>
            <div>
                <button type="submit" class="uk-button uk-button-primary" :disabled="invalid">Change</button>
            </div>
        </form>
        </ValidationObserver>
    </div>
</template>
<script>
import { ValidationObserver, ValidationProvider, extend, configure, setInteractionMode } from 'vee-validate'
import { required, email } from 'vee-validate/dist/rules'
import ValidationErrors from '@/components/ValidationErrors'

setInteractionMode('eager')

extend('required', required)
extend('email', email)

configure({
  classes: {
    valid: 'uk-form-success',
    invalid: 'uk-form-danger'
  }
})
export default {

    name: 'email',

    props: {
        id: {
            type: Number,
            required: true
        },
        email: {
            type: String,
            required: true
        }
    },

    data () {
        return {
            newEmail: ''
        }
    },

    methods: {
        change () {
            this.$securedApi.post(`/user/${this.id}/email`, { email: this.newEmail })
                .then(res => {
                    this.UI.notification('Changed email.')
                })
                .catch(err => {
                    this.$refs.observer.setErrors(err.response.data.errors)
                })
        }
    },

    components: {
        ValidationObserver,
        ValidationProvider,
        ValidationErrors
    }
}
</script>
