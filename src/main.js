import Vue from 'vue'
import { store } from './store'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import { publicApi, securedApi } from './axios'
import UIkit from 'uikit'

Vue.config.productionTip = false

Vue.use(VueAxios, axios)

Vue.prototype.$publicApi = publicApi
Vue.prototype.$securedApi = securedApi

Vue.prototype.UI = UIkit
Vue.prototype.$util = UIkit.util

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')
