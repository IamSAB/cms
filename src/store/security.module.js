import { publicApi, securedApi } from '../axios'

const accessToken = localStorage.getItem('access_token')
const refreshToken = localStorage.getItem('refresh_token')
const currentUserJSON = localStorage.getItem('current_user')
const currentUser = currentUserJSON ? JSON.parse(currentUserJSON) : null

export const Security = {

    state: {
        accessToken,
        refreshToken,
        currentUser
    },

    getters: {
        accessToken: (state) => state.accessToken,
        refreshToken: (state) => state.refreshToken,
        refreshTokenData: (state) => state.refreshToken ? JSON.parse(atob(state.refreshToken.split('.')[1])) : null,
        accessTokenData: (state) => state.accessToken ? JSON.parse(atob(state.accessToken.split('.')[1])) : null,
        currentIdentity: (state, getters) => getters.accessTokenData ? getters.accessTokenData.identity : '',
        isAuthenticated: state => state.accessToken != null
    },

    mutations: {

        setCurrentUser (state, user) {
            localStorage.setItem('current_user', JSON.stringify(user))
            state.currentUser = user
        },

        accessToken (state, accessToken) {
            localStorage.setItem('access_token', accessToken)
            state.accessToken = accessToken
        },

        refreshToken (state, refreshToken) {
            localStorage.setItem('refresh_token', refreshToken)
            state.refreshToken = refreshToken
        },

        logout (state) {
            state.accessToken = null
            state.refreshToken = null
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
        }
    },

    actions: {

        updateCurrentUser ({ commit, getters }) {
            return new Promise((resolve, reject) => {
                securedApi.get(`/user/${getters.accessTokenData.user_claims.id}`)
                    .then(res => {
                        commit('setCurrentUser', res.data)
                        resolve(res)
                    })
                    .catch(err => reject(err))
            })
        },

        login ({ commit, dispatch }, credentials) {
            return new Promise((resolve, reject) => {
                publicApi.post('/login', credentials)
                .then((response) => {
                    commit('accessToken', response.data.access_token)
                    commit('refreshToken', response.data.refresh_token)
                    dispatch('updateCurrentUser')
                        .then(res => resolve(res))
                        .catch(err => reject(err))
                })
                .catch(err => reject(err))
            })
        },

        refresh ({ commit, dispatch, state }) {
            return new Promise((resolve, reject) => {
                publicApi.post('/refresh', {
                        refresh_token: state.refreshToken
                    }, {
                        headers: {
                            Authorization: 'Bearer ' + state.refreshToken
                        }
                    })
                    .then(response => {
                        commit('accessToken', response.data.access_token)
                        dispatch('updateCurrentUser')
                            .then(res => resolve(res))
                            .catch(err => reject(err))
                    })
                    .catch(error => reject(error))
            })
        },

        freshlogin ({ commit, dispatch }, credentials) {
            return new Promise((resolve, reject) => {
                publicApi.post('/freshlogin', credentials)
                .then((response) => {
                    commit('accessToken', response.data.access_token)
                    dispatch('updateCurrentUser')
                        .then(res => resolve(res))
                        .catch(err => reject(err))
                })
                .catch((error) => {
                    reject(error)
                })
            })
        }
    }
}
