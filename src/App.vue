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
                        <a uk-toggle="#login">Login</a>
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

        <router-view />

        <div id="login" ref="login" uk-modal>
            <div class="uk-modal-dialog">
                <form class="uk-form-stacked" @submit.prevent="login">
                    <div class="uk-modal-body">
                        <h2 class="uk-modal-title">Login</h2>
                        <div class="uk-form-label">Identity</div>
                        <div class="uk-form-controls">
                            <input type="text" class="uk-input" v-model="identity">
                        </div>
                        <div class="uk-form-label">Password</div>
                        <div class="uk-form-controls">
                            <input type="password" class="uk-input" v-model="password">
                        </div>
                    </div>
                    <div class="uk-modal-footer uk-text-right" uk-margin>
                        <a uk-toggle="#forgotpassword" class="uk-button text">Forgot password</a>
                        <button class="uk-button uk-button-default uk-modal-close" type="button">Cancel</button>
                        <button class="uk-button uk-button-primary">Login</button>
                    </div>
                </form>
            </div>
        </div>

        <div ref="forgotpassword" uk-modal>
            <div class="uk-modal-dialog">
                <form class="uk-form-stacked" @submit.prevent="forgotpassword">
                    <h2 class="uk-modal-title">Forgot password</h2>
                    <div class="uk-modal-body">
                        <div class="uk-form-label">Email</div>
                        <div class="uk-form-controls">
                            <input type="email" class="uk-input" v-model="email">
                        </div>
                    </div>
                    <div class="uk-modal-footer uk-text-right">
                        <button class="uk-button uk-button-default uk-modal-close" type="button">Cancel</button>
                        <button class="uk-button uk-button-primary">Send</button>
                    </div>
                </form>
            </div>
        </div>

        <div ref="relogin" uk-modal>
            <div class="uk-modal-dialog">
                <form class="uk-form-stacked" @submit.prevent="$emit('relogin')">
                    <div class="uk-modal-body">
                        <h2 class="uk-modal-title">Relogin</h2>
                        <p>Your refresh token has expired. You must relogin, to obtain a new access token.</p>
                        <div class="uk-form-label">Identity</div>
                        <div class="uk-form-controls">
                            <input type="text" class="uk-input" :value="currentIdentity" disabled>
                        </div>
                        <div class="uk-form-label">Password</div>
                        <div class="uk-form-controls">
                            <input type="password" class="uk-input" v-model="password">
                        </div>
                    </div>
                    <div class="uk-modal-footer uk-text-right">
                        <button class="uk-button uk-button-default uk-modal-close" type="button">Cancel</button>
                        <button class="uk-button uk-button-primary">Relogin</button>
                    </div>
                </form>
            </div>
        </div>

        <div ref="freshlogin" uk-modal>
            <div class="uk-modal-dialog">
                <form class="uk-form-stacked" @submit.prevent="$emit('freshlogin')">
                    <div class="uk-modal-body">
                        <h2 class="uk-modal-title">Fresh login</h2>
                        <div class="uk-form-label">Identity</div>
                        <div class="uk-form-controls">
                            <input type="text" class="uk-input" :value="currentIdentity" disabled>
                        </div>
                        <div class="uk-form-label">Password</div>
                        <div class="uk-form-controls">
                            <input type="password" class="uk-input" v-model="password">
                        </div>
                    </div>
                    <div class="uk-modal-footer uk-text-right">
                        <button class="uk-button uk-button-default uk-modal-close" type="button">Cancel</button>
                        <button class="uk-button uk-button-primary">Login</button>
                    </div>
                </form>
            </div>
        </div>

        <div ref="resetpassword" uk-modal>
            <div class="uk-modal-dialog">
                <form class="uk-form-stacked" @submit.prevent="$emit('resetpassword')">
                    <h2 class="uk-modal-title">Reset password</h2>
                    <div class="uk-modal-body">
                        <div class="uk-form-label">New password</div>
                        <div class="uk-form-controls">
                            <input type="password" class="uk-input" v-model="password">
                        </div>
                    </div>
                    <div class="uk-modal-footer uk-text-right">
                        <button class="uk-button uk-button-default uk-modal-close" type="button">Cancel</button>
                        <button class="uk-button uk-button-primary">Change</button>
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
            identity: '',
            password: '',
            email: ''
        }
    },

    computed: {
        ...mapGetters([
            'currentIdentity',
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
        this.$securedApi.interceptors.request.use(request => {
            if (this.isAuthenticated) {
                let promise = Promise.resolve()
                const now = Math.floor(Date.now() / 1000)
                if (this.refreshTokenData.exp < now) {
                    console.log('Refresh token expired')
                    promise = new Promise((resolve, reject) => {
                        const modal = this.UI.modal(this.$refs.relogin)
                        modal.show()
                        this.$once('relogin', () => {
                            this.$store.dispatch('login', {
                                    identity: this.currentIdentity,
                                    password: this.password
                                }).then(res => {
                                    this.UI.notification('Successful relogin.', 'success')
                                    modal.hide()
                                    resolve(res)
                                })
                        })
                    })
                } else if (this.accessTokenData.exp < now) {
                    console.log('Access token expired')
                    promise = new Promise((resolve, reject) => {
                        this.$store.dispatch('refresh')
                            .then(res => {
                                this.UI.notification('Successful login refresh.', 'success')
                                resolve(res)
                            })
                            .catch(err => reject(err))
                    })
                }
                return new Promise((resolve, reject) => {
                    promise.then(() => {
                            request.headers = {
                                Authorization: 'Bearer ' + this.accessToken
                            }
                            resolve(request)
                        })
                        .catch(err => reject(err))
                })
            } else {
                return request
            }
        })

        this.$securedApi.interceptors.response.use(null, error => new Promise((resolve, reject) => {
            if (this.isAuthenticated && error.response.status === 401 && error.response.data.msg === 'Fresh token required') {
                let modal = this.UI.modal(this.$refs.freshlogin)
                modal.show()
                this.$once('freshlogin', () => {
                    this.$store.dispatch('freshlogin', {
                            identity: this.currentIdentity,
                            password: this.password
                        })
                        .then(res => {
                            this.UI.notification('Successful fresh login.', 'success')
                            modal.hide()
                            this.$http.request(error.request)
                                .then(r => resolve(r))
                                .catch(e => reject(e))
                        })
                        .catch(err => reject(err))
                })
            } else {
                reject(error)
            }
        }))

        if (this.$route.query.activate_account) {
            this.$publicApi.post('/activate', { params: { token: this.$route.query.activate_account } })
                .then(res => {
                    this.UI.notification('Successful account activation.', 'success')
                    this.$router.push({ name: 'login' })
                })
        }
        if (this.$route.query.change_email) {
            this.$publicApi.get('/email', { params: { token: this.$route.query.change_email } })
                .then(res => {
                    this.UI.notification('Successful email change.', 'success')
                    this.$store.updateCurrentUser()
                    this.$router.push({ name: 'me' })
            })
        }
        if (this.$route.query.reset_password) {
            let modal = this.UI.modal(this.$refs.resetpassword)
            this.password = ''
            modal.show()
            this.$once('resetpassword', () => {
                this.$publicApi.post('/security/password', {
                    password: this.password,
                    token: this.$route.query.reset_password
                })
                .then((res) => {
                    modal.hide()
                    this.UI.notification('Successful password reset.', 'success')
                    this.$router.push({ name: 'login' })
                })
            })
        }
    },

    methods: {

        forgotpassword () {
            this.$publicApi.get('/security/password', {
                identity: this.identity
            })
            .then(res => {
                this.UI.notification('Please check your email inbox to reset your password.', 'success')
                this.UI.modal(this.$refs.forgotpassword).hide()
            })
        },

        login () {
            const modal = this.UI.modal(this.$refs.login)
            this.$store.dispatch('login', {
                    identity: this.identity,
                    password: this.password
                }).then(res => {
                    this.UI.notification('Successful login.', 'success')
                    modal.hide()
                    this.$router.push({ name: 'me' })
                })
        },

        logout () {
            this.identity = ''
            this.$store.commit('logout')
            this.UI.notification('Succesful logout.', 'success')
        }

    }
}
</script>
