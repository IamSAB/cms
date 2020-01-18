const jwt = localStorage.getItem('jwt')

export const AuthModule = {

    state: {
        jwt
    },

    getters: {
        getJwt: (state) => state.jwt,
        jwtData: (state) => state.jwt ? JSON.parse(atob(state.jwt.split('.')[1])) : null,
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

        authenticate ({ commit }, { vm, credentials }) {
            return new Promise((resolve, reject) => {
                vm.$api.post('/security/authenticate', credentials)
                .then((response) => {
                    localStorage.setItem('jwt', response.data.jwt)
                    commit('authenticate', response.data.jwt)
                    resolve(response)
                })
                .catch((error) => {
                    reject(error)
                })
            })
        }
    }
}
