import Loader from '../components/Loader.vue'

export default {

    data () {
        return {
            status: 0
        }
    },

    created () {
        this.load()
    },

    watch: {
        '$route': 'load'
    },

    methods: {

        load () {
            return {}
        },

        loaded (msg) {
            this.status = 1
            window.UIkit.notification({
                message: msg,
                status: '',
                pos: 'top-right',
                timeout: 5000
            })
        },

        error (msg, error) {
            this.status = 2
            console.log(error)
            window.UIkit.notification({
                message: `${msg} [${error}]`,
                status: 'danger',
                pos: 'top-right',
                timeout: 5000
            })
        }
    },

    components: {
        Loader
    }
}
