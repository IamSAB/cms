<template>
    <div>
        <ValidationObserver v-slot="{ invalid }" ref="observer">
        <form @submit.prevent="change" class="uk-form uk-form-stacked" uk-margin>
            <div>
                <ValidationProvider vid="password" name="Passoword" rules="required" v-slot="{ errors, classes }">
                <label class="uk-form-label">New password</label>
                <div class="uk-form-controls">
                    <input type="password" class="uk-input" v-model="password" :class="classes">
                    <ValidationErrors :errors="errors"/>
                </div>
                </ValidationProvider>
            </div>
            <div>
                <ValidationProvider vid="confirm" name="Password confirmation" rules="required|confirmed:password" v-slot="{ errors, classes }">
                <label class="uk-form-label">Confirm password</label>
                <div class="uk-form-controls">
                    <input type="password" class="uk-input" v-model="confirm" :class="classes">
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
import { required, confirmed } from 'vee-validate/dist/rules'
import ValidationErrors from '@/components/ValidationErrors'

setInteractionMode('eager')

extend('required', required)
extend('confirmed', confirmed)

configure({
  classes: {
    valid: 'uk-form-success',
    invalid: 'uk-form-danger'
  }
})
export default {

    name: 'password',

    props: {
        id: {
            type: Number,
            required: true
        }
    },

    data: () => {
        return {
            password: '',
            confirm: ''
        }
    },

    methods: {
        change () {
            this.$securedApi.post(`/user/${this.id}/password`, {
                    password: this.password,
                    confirm: this.confirm
                })
                .then(res => {
                    this.UI.notification('Changed password.', 'success')
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
