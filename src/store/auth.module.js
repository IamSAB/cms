const jwt = localStorage.getItem('jwt')

export const AuthModule = {

    state: {
        jwt
    },

    getters: {
        jwt: state => state.jwt,
        isAuthenticated: state => state.jwt != null
    },

    mutations: {

        authenticate (state, jwt) {
            state.jwt = jwt
        },

        logout (state) {
            state.jwt = null
        }
    },

    actions: {

        login ({ commit }, { vm, credentials }) {
            return new Promise((resolve, reject) => {
                vm.$api.post('/auth', credentials)
                .then((response) => {
                    localStorage.setItem('jwt', response.data.access_token)
                    commit('authenticate', response.data.access_token)
                    vm.$notify('Successfully logged in.')
                    resolve()
                })
                .catch((error) => {
                    vm.$notify(error.response.data.description, 'danger')
                    reject(error)
                })
            })
        }
    }
}
