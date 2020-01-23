<template>
    <div class="uk-flex uk-flex-center">
        <ValidationObserver v-slot="{ invalid }">
        <form @submit.prevent="register" class="uk-form-stacked">
            <div>
                <ValidationProvider name="Username" rules="required|alphaNum" v-slot="{ errors, classes }">
                <label class="uk-form-label">Username</label>
                <div class="uk-form-controls">
                    <input type="text" class="uk-input" v-model="user.username" :class="classes">
                    <div><span v-for="(msg, i) in errors" :key="i">{{ msg }}</span></div>
                </div>
                </ValidationProvider>
            </div>
            <div>
                <ValidationProvider name="Email" rules="required" v-slot="{ errors, classes }">
                <label class="uk-form-label">Email</label>
                <div class="uk-form-controls">
                    <input type="email" class="uk-input" v-model="user.email" :class="classes">
                    <div><span v-for="(msg, i) in errors" :key="i">{{ msg }}</span></div>
                </div>
                </ValidationProvider>
            </div>
            <div>
                <ValidationProvider name="Passoword" rules="required" v-slot="{ errors, classes }" vid="password">
                <label class="uk-form-label">Password</label>
                <div class="uk-form-controls">
                    <input type="password" class="uk-input" v-model="user.password" :class="classes">
                    <div><span v-for="(msg, i) in errors" :key="i">{{ msg }}</span></div>
                </div>
                </ValidationProvider>
            </div>
            <div>
                <ValidationProvider name="Password confirmation" rules="required|confirmed:password" v-slot="{ errors, classes }">
                <label class="uk-form-label">Confirm password</label>
                <div class="uk-form-controls">
                    <input type="password" class="uk-input" v-model="user.confirm" :class="classes">
                    <div><span v-for="(msg, i) in errors" :key="i">{{ msg }}</span></div>
                </div>
                </ValidationProvider>
            </div>
            <div>
                <ValidationProvider name="Forename" rules="required|alpha" v-slot="{ errors, classes }">
                <label class="uk-form-label">Forename</label>
                <div class="uk-form-controls">
                    <input type="text" class="uk-input" v-model="user.forename" :class="classes">
                    <div><span v-for="(msg, i) in errors" :key="i">{{ msg }}</span></div>
                </div>
                </ValidationProvider>
            </div>
            <div>
                <ValidationProvider name="Surname" rules="required|alpha" v-slot="{ errors, classes }">
                <label class="uk-form-label">Surname</label>
                <div class="uk-form-controls">
                    <input type="text" class="uk-input" v-model="user.surname" :class="classes">
                    <div><span v-for="(msg, i) in errors" :key="i">{{ msg }}</span></div>
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

    name: 'user-edit',

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

    computed: {
        url () {
            return `/user/${this.$route.params.id}`
        }
    },

    mounted () {
        this.$api.get(this.url)
            .then(response => {
                console.log(response.data)
                this.user = response.data
            })
    },

    methods: {
        save () {
            this.$api.post(this.url, this.$data)
                .then((response) => {
                    window.UIkit.notification(response.data.msg)
                })
        }
    },

    components: {
        ValidationProvider,
        ValidationObserver
    }
}
</script>
