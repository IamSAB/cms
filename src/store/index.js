import Vue from 'vue'
import Vuex from 'vuex'

import { AuthModule } from './auth.module'
import { XHRStatusModule } from './xhrstatus.module'

Vue.use(Vuex)

export const store = new Vuex.Store({
    modules: {
        auth: AuthModule,
        status: XHRStatusModule
    }
})
