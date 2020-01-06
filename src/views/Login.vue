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
                <div class="uk-form-label">Password</div>
                <div class="uk-form-controls">
                    <input type="password" class="uk-input" v-model="password">
                </div>
            </div>
            <div>
                <input type="submit" value="Login" class="uk-input" @click.prevent="login">
            </div>
        </form>
    </div>
</template>

<script>
export default {

    name: 'login',

    data () {
        return {
            username: '',
            password: ''
        }
    },

    methods: {
        login () {
            this.$api.post('/auth', this.$data)
                .then((response) => {
                    window.UIkit.notification('Success')
                    window.localStorage.setItem('access_token', response.data.access_token)
                })
                .catch((error) => {
                    console.log(error)
                })
        }
    }
}
</script>
