const XHRStatus = {
    Inactive: 0,
    Pending: 1,
    Success: 2,
    RequestError: 3,
    RepsonseError: 4,
    ClientError: 5,
    ServerError: 6,
    UnkownError: 7
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

        setUnknownError (state) {
            state.xhrstatus = XHRStatus.UnkownError
        },

        setRequestError (state) {
            state.xhrstatus = XHRStatus.RequestError
        },

        setResponseError (state) {
            state.xhrstatus = XHRStatus.ResponseError
        },

        setClientError (state) {
            state.xhrstatus = XHRStatus.ClientError
        },

        setServerError (state) {
            state.xhrstatus = XHRStatus.ServerError
        }

    }
}
