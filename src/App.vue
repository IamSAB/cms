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
                <div v-if="hasXHR" class="uk-navbar-item">
                    <div v-if="isPending">
                        <div uk-spinner></div>
                    </div>
                    <div v-else-if="isSuccess">
                        <div class="uk-text-success">
                            <span uk-icon="check"></span>
                            {{ status.msg }}
                        </div>
                    </div>
                    <div v-else>
                        <div class="uk-text-danger">
                            <span uk-icon="close"></span>
                            {{ status.code }}
                            {{ status.msg }}
                        </div>
                    </div>
                </div>
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
import { mapMutations, mapState, mapGetters } from 'vuex'

export default {

    computed: {
        ...mapGetters([
            'isAuthenticated',
            'hasXHR',
            'isPending',
            'isSuccess'
        ]),
        ...mapState([
            'status'
        ])
    },

    methods: {
        ...mapMutations([
            'logout'
        ])
    }
}
</script>
