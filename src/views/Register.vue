<template>
    <div class="uk-flex uk-flex-center">
        <form class="uk-form-stacked">
            <div>
                <label class="uk-form-label">Username</label>
                <div class="uk-form-controls">
                    <input type="text" class="uk-input" v-model="username">
                </div>
            </div>
            <div>
                <label class="uk-form-label">Email</label>
                <div class="uk-form-controls">
                    <input type="email" class="uk-input" v-model="email">
                </div>
            </div>
            <div>
                <div class="uk-form-label">Password</div>
                <div class="uk-form-controls">
                    <input type="password" class="uk-input" v-model="password">
                </div>
            </div>
            <div>
                <div class="uk-form-label">Passwort bestätigen</div>
                <div class="uk-form-controls">
                    <input type="password" class="uk-input" v-model="confirm">
                </div>
            </div>
            <div>
                <label class="uk-form-label">Vorname</label>
                <div class="uk-form-controls">
                    <input type="text" class="uk-input" v-model="forename">
                </div>
            </div>
            <div>
                <label class="uk-form-label">Nachname</label>
                <div class="uk-form-controls">
                    <input type="text" class="uk-input" v-model="surname">
                </div>
            </div>
            <div>
                <input type="submit" value="Registrieren" class="uk-button" @click.prevent="register">
            </div>
        </form>
    </div>
</template>

<script>
export default {

    name: 'register',

    data () {
        return {
            username: '',
            email: '',
            forename: '',
            surname: '',
            password: '',
            confirm: ''
        }
    },

    methods: {
        register () {
            this.$api.post('/user/register', this.$data)
                .then((response) => {
                    window.UIkit.notification(response.data.msg)
                    this.$router.push('login')
                })
                .catch((error) => {
                    console.log('Error', error)
                })
        }
    }
}
</script>
