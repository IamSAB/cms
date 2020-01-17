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
                        <a href="#">Login</a>
                        <div class="uk-navbar-dropdown">
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
                                <div class="uk-margin-top">
                                    <button @click="login" class="uk-button uk-button-default" type="button">Login</button>
                                </div>
                            </form>
                        </div>
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

        <div ref="modal" uk-modal>
            <div class="uk-modal-dialog uk-modal-body">
                <p>You were too long inactive. Please refresh your login.</p>
                <form class="uk-form-stacked">
                    <div>
                        <div class="uk-form-label">Password</div>
                        <div class="uk-form-controls">
                            <input type="password" class="uk-input" v-model="password">
                        </div>
                    </div>
                    <div class="uk-margin-top">
                        <button @click="$emit('refresh')" class="uk-button uk-button-default" type="button">Refresh</button>
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
            'getJwt',
            'isAuthenticated',
            'jwtData',
            'hasXHR',
            'isPending',
            'isSuccess'
        ])
    },

    mounted () {
        this.modal = window.UIkit.modal(this.$refs.modal)
        this.$api.interceptors.response.use(null, (error) => new Promise((resolve, reject) => {
            if (error.response.status === 401 & this.isAuthenticated) {
                this.modal.show()
                this.$once('refresh', () => {
                    this.$store.dispatch('authenticate', {
                        vm: this,
                        credentials: {
                            username: this.jwtData.username,
                            password: this.password
                        }
                    })
                    .then(response => {
                        let config = error.config
                        config.baseURL = ''
                        config.headers.Authorization = this.getJwt
                        this.$http.request(config)
                        .then(response => {
                            this.modal.hide()
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
            this.$store.dispatch('authenticate', {
                vm: this,
                credentials: {
                    username: this.username,
                    password: this.password
                }
            })
            .then((response) => {
                this.password = ''
                this.$notify('Successfully authenticated.')
            })
            .catch((error) => {
                this.$notify(error.response.data.name, 'danger')
            })
        },

        logout () {
            this.$store.commit('logout')
            localStorage.removeItem('jwt')
            this.$router.push('about')
            this.$notify('Successfully logged out.')
        }

    }
}
</script>
