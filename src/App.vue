<template>
    <div>
        <nav class="uk-navbar-container" uk-navbar>
            <div class="uk-navbar-left">
                <ul class="uk-navbar-nav">
                    <li><router-link to="/">Home</router-link></li>
                    <li><router-link to="/about">About</router-link></li>
                </ul>
            </div>
            <div class="uk-navbar-right">
                <template v-if="isAuthenticated">
                    <div class="uk-navbar-item">Logged in!</div>
                    <ul class="uk-navbar-nav">
                        <li><router-link to="/me">Me</router-link></li>
                        <li><a @click="logout">Logout</a></li>
                    </ul>
                </template>
                <ul v-else class="uk-navbar-nav">
                    <li><router-link to="/login">Login</router-link></li>
                    <li><router-link to="/register">Register</router-link></li>
                </ul>
            </div>
        </nav>
        <div class="uk-section">
            <div class="uk-container">
            <router-view />
            </div>
        </div>
    </div>
</template>

<script>
export default {

    computed: {
        isAuthenticated () {
            return localStorage.getItem('access_token') != null
        }
    },

    methods: {
        logout () {
            window.localStorage.removeItem('access_token')
        }
    }
}
</script>
