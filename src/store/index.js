import Vue from 'vue'
import Vuex from 'vuex'

import { Security } from './security.module'
import { XHRStatusModule } from './xhrstatus.module'

Vue.use(Vuex)

export const store = new Vuex.Store({
    modules: {
        security: Security,
        status: XHRStatusModule
    }
})
