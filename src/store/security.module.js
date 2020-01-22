const accessToken = localStorage.getItem('access_token')
const refreshToken = localStorage.getItem('refresh_token')

export const Security = {

    state: {
        accessToken,
        refreshToken

    },

    getters: {
        accessToken: (state) => state.accessToken,
        refreshToken: (state) => state.refreshToken,
        refreshTokenData: (state) => state.refreshToken ? JSON.parse(atob(state.refreshToken.split('.')[1])) : null,
        accessTokenData: (state) => state.accessToken ? JSON.parse(atob(state.accessToken.split('.')[1])) : null,
        isAuthenticated: state => state.accessToken != null
    },

    mutations: {

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

        login ({ commit }, { vm, credentials }) {
            return new Promise((resolve, reject) => {
                vm.$api.post('/security/login', credentials)
                .then((response) => {
                    commit('accessToken', response.data.access_token)
                    commit('refreshToken', response.data.refresh_token)
                    resolve(response)
                })
                .catch((error) => {
                    reject(error)
                })
            })
        },

        refresh ({ commit }, { vm, credentials }) {
            return new Promise((resolve, reject) => {
                vm.$api.post('/security/refresh', credentials)
                .then((response) => {
                    commit('accessToken', response.data.access_token)
                    resolve(response)
                })
                .catch((error) => {
                    reject(error)
                })
            })
        },

        freshlogin ({ commit }, { vm, credentials }) {
            return new Promise((resolve, reject) => {
                vm.$api.post('/security/freshlogin', credentials)
                .then((response) => {
                    commit('accessToken', response.data.access_token)
                    resolve(response)
                })
                .catch((error) => {
                    reject(error)
                })
            })
        }
    }
}
