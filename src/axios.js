import axios from 'axios'
import { store } from './store'
import UIkit from 'uikit'

const XhrStatusRequestInterceptor = [config => {
    store.commit('setPending')
    return config
}, (error) => {
    store.commit('setRequestError')
    UIkit.notification('Could not send request.')
    return Promise.reject(error)
}]

const XhrStatusResponseInterceptor = [response => {
    store.commit('setSuccess')
    setTimeout(() => {
        store.commit('setInactive')
    }, 3000)
    return response
}, (error) => {
    if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.log(error.response)
        let msg = ''
        if (error.response.status >= 500) {
            store.commit('setServerError')
            msg = 'Server Error'
        } else if (error.response.status >= 400) {
            store.commit('setClientError')
            msg = 'Client Error'
        } else {
            store.commit('setUnknownError')
            msg = 'Unknown Error'
        }
        if (typeof error.response.data === 'string' || error.response.data instanceof String) {
            msg = error.response.data
        } else if (error.response.data.msg) {
            msg = error.response.data.msg
        }
        UIkit.notification(msg, 'danger')
    } else if (error.request) {
        // The request was made but no response was received
        // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
        // http.ClientRequest in node.js
        console.log(error.request)
        store.commit('setResponseError')
        UIkit.notification('Request sent, but no response received.', 'danger')
    } else {
        // Something happened in setting up the request that triggered an Error
        console.log(error)
        console.log('Error', error.message)
        store.commit('setUnknownError')
        UIkit.notification('Unknown error.', 'danger')
    }
    // console.log(error.config)
    setTimeout(() => {
        store.commit('setInactive')
    }, 3000)
    return Promise.reject(error)
}]

axios.interceptors.request.use(...XhrStatusRequestInterceptor)
axios.interceptors.response.use(...XhrStatusResponseInterceptor)
axios.defaults.timeout = 2000

export const publicApi = axios.create({
    baseURL: '/api/'
})
publicApi.interceptors.request.use(...XhrStatusRequestInterceptor)
publicApi.interceptors.response.use(...XhrStatusResponseInterceptor)

export const securedApi = axios.create({
    baseURL: '/api/'
})
securedApi.interceptors.request.use(...XhrStatusRequestInterceptor)
securedApi.interceptors.response.use(...XhrStatusResponseInterceptor)
