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
                    <li>
                        <a uk-toggle="target: #login">Login</a>
                    </li>
                    <li><router-link to="/register">Register</router-link></li>
                </ul>
                <div v-if="hasXHR" class="uk-navbar-item">
                    <div v-if="isPending">
                        <div uk-spinner></div>
                    </div>
                    <div v-else-if="isSuccess">
                        <div class="uk-text-success">
                            <span uk-icon="check"></span>
                        </div>
                    </div>
                    <div v-else>
                        <div class="uk-text-danger">
                            <span uk-icon="close"></span>
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

        <div id="login" ref="login" uk-modal>
            <div class="uk-modal-dialog uk-modal-body">
                <button class="uk-modal-close-default" type="button" uk-close></button>
                <h2 class="uk-modal-title">Login</h2>
                <form class="uk-form-stacked">
                    <div>
                        <div class="uk-form-label">Username</div>
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
                    <div class="uk-margin-top" uk-margin>
                        <button class="uk-button uk-button-default uk-modal-close" type="button">Close</button>
                        <button @click="login" class="uk-button uk-button-primary" type="button">Login</button>
                    </div>
                </form>
            </div>
        </div>

        <div ref="freshlogin" uk-modal>
            <div class="uk-modal-dialog uk-modal-body">
                <h2 class="uk-modal-title">Fresh login</h2>
                <form class="uk-form-stacked">
                    <div>
                        <div class="uk-form-label">Password</div>
                        <div class="uk-form-controls">
                            <input type="password" class="uk-input" v-model="password">
                        </div>
                    </div>
                    <div class="uk-margin-top">
                        <button @click="$emit('freshlogin')" class="uk-button uk-button-default" type="button">Login</button>
                    </div>
                </form>
            </div>
        </div>

    </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {

    data () {
        return {
            username: '',
            password: ''
        }
    },

    computed: {
        ...mapGetters([
            'accessToken',
            'refreshToken',
            'isAuthenticated',
            'accessTokenData',
            'refreshTokenData',
            'hasXHR',
            'isPending',
            'isSuccess'
        ])
    },

    mounted () {
        const freshloginModal = window.UIkit.modal(this.$refs.freshlogin)
        this.$api.interceptors.response.use(null, (error) => new Promise((resolve, reject) => {
            if (error.response.status === 401 & this.isAuthenticated) {
                this.modal.show()
                this.$once('freshlogin', () => {
                    this.$store.dispatch('freshlogin', {
                        vm: this,
                        credentials: {
                            username: this.jwtData.username,
                            password: this.password
                        }
                    })
                    .then(response => {
                        let config = error.config
                        config.baseURL = ''
                        config.headers.Authorization = 'Bearer' + this.accessToken
                        this.$http.request(config)
                        .then(response => {
                            freshloginModal.hide()
                            resolve(response)
                        })
                        .catch(error => reject(error))
                    })
                    .catch((error) => reject(error))
                })
            }
        }))
    },

    methods: {

        login () {
            const loginModal = window.UIkit.modal(this.$refs.login)
            this.$store.dispatch('login', {
                vm: this,
                credentials: {
                    username: this.username,
                    password: this.password
                }
            })
            .then((response) => {
                this.password = ''
                loginModal.hide()
                this.$notify('Successfully logged in.')
            })
            .catch((error) => {
                this.$notify(error.response.data.name, 'danger')
            })
        },

        logout () {
            this.username = ''
            this.$store.commit('logout')
            this.$router.push('about')
            this.$notify('Successfully logged out.')
        }

    }
}
</script>
