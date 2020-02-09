<template>
    <div>
        <ValidationObserver v-slot="{ invalid }" ref="observer">
        <form @submit.prevent="register" class="uk-form-stacked" uk-margin>
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
                <ValidationProvider vid="email" name="Email" rules="required" v-slot="{ errors, classes }">
                <label class="uk-form-label">Email</label>
                <div class="uk-form-controls">
                    <input type="email" class="uk-input" v-model="user.email" :class="classes">
                    <ValidationErrors :errors="errors"/>
                </div>
                </ValidationProvider>
            </div>
            <div>
                <ValidationProvider vid="password" name="Passoword" rules="required" v-slot="{ errors, classes }">
                <label class="uk-form-label">Password</label>
                <div class="uk-form-controls">
                    <input type="password" class="uk-input" v-model="user.password" :class="classes">
                    <ValidationErrors :errors="errors"/>
                </div>
                </ValidationProvider>
            </div>
            <div>
                <ValidationProvider vid="confirm" name="Password confirmation" rules="required|confirmed:password" v-slot="{ errors, classes }">
                <label class="uk-form-label">Confirm password</label>
                <div class="uk-form-controls">
                    <input type="password" class="uk-input" v-model="user.confirm" :class="classes">
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
                <button type="submit" class="uk-button uk-button-primary uk-margin-top" :disabled="invalid">Register</button>
            </div>
        </form>
        </ValidationObserver>
    </div>
</template>

<script>
import { ValidationObserver, ValidationProvider, extend, configure, setInteractionMode } from 'vee-validate'
import { required, email, alpha_num as alphaNum, confirmed, alpha } from 'vee-validate/dist/rules'
import ValidationErrors from '@/components/ValidationErrors'

setInteractionMode('eager')

extend('required', required)
extend('alphaNum', alphaNum)
extend('alpha', alpha)
extend('email', email)
extend('confirmed', confirmed)

configure({
  classes: {
    valid: 'uk-form-success',
    invalid: 'uk-form-danger'
  }
})

export default {

    name: 'user-register',

    props: {
        admin: {
            type: Boolean,
            default: false
        }
    },

    data () {
        return {
            user: {
                username: '',
                email: '',
                forename: '',
                surname: '',
                password: '',
                confirm: ''
            }
        }
    },

    methods: {
        register () {
            this.$publicApi.put('/user', this.user)
                .then(res => {
                    if (this.admin === true) {
                        this.UI.notify('Successful registration. You will receive a mail to activate your account.')
                        this.$router.push('login')
                    } else {
                        this.UI.notification('User registered. An email was sent for account activation.')
                    }
                })
                .catch(error => {
                    this.$refs.observer.setErrors(error.response.data.errors)
                })
        }
    },

    components: {
        ValidationProvider,
        ValidationObserver,
        ValidationErrors
    }
}
</script>
