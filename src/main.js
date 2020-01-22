import Vue from 'vue'
import { store } from './store'
import axios from 'axios'
import VueAxios from 'vue-axios'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'

Vue.config.productionTip = false

Vue.use(VueAxios, axios)

let config = {
    baseURL: '/api/',
    timeout: 1000
}

const api = axios.create(config)

api.interceptors.request.use((config) => {
    store.commit('setPending')
    const accessToken = store.getters.accessToken
    if (accessToken) {
        config.headers = {
            Authorization: 'Bearer' + accessToken
        }
    }
    return config
}, (error) => {
    store.commit('setError', error)
    return Promise.reject(error)
})

api.interceptors.response.use((response) => {
    store.commit('setSuccess')
    setTimeout(() => {
        store.commit('setInactive')
    }, 3000)
    return response
}, (error) => {
    store.commit('setError', error)
    setTimeout(() => {
        store.commit('setInactive')
    }, 3000)
    return Promise.reject(error)
})

Vue.prototype.$api = api
Vue.prototype.$notify = (msg, status = 'success') => {
    window.UIkit.notification({
        message: msg,
        status: status,
        pos: 'bottom-right',
        timeout: 3000
    })
}

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
