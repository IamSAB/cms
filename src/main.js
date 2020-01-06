import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'

Vue.config.productionTip = false
Vue.use(VueAxios, axios)

Vue.prototype.$api = axios.create({
  baseURL: '/api/',
  timeout: 1000,
  headers: {
    'Authorization': 'JWT ' + window.localStorage.getItem('access_token')
  }
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
