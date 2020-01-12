const XHRStatus = {
    Inactive: 'inactive',
    Pending: 'pending',
    Success: 'success',
    Error: 'error'
}

export const XHRStatusModule = {

    state: {
        xhrstatus: XHRStatus.Inactive
    },

    getters: {
        hasXHR: state => state.xhrstatus !== XHRStatus.Inactive,
        isPending: state => state.xhrstatus === XHRStatus.Pending,
        isSuccess: state => state.xhrstatus === XHRStatus.Success
    },

    mutations: {

        setInactive (state) {
            state.xhrstatus = XHRStatus.Inactive
        },

        setPending (state) {
            state.xhrstatus = XHRStatus.Pending
        },

        setSuccess (state) {
            state.xhrstatus = XHRStatus.Success
        },

        setError (state) {
            state.xhrstatus = XHRStatus.Error
        }

    }
}
