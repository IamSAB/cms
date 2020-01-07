<template>
    <Loader :status="status">
        Username: {{me.username}} <br>
        email: {{me.email}} <br>
        forename: {{me.forename}} <br>
        surname: {{me.surname}}
    </Loader>
</template>

<script>
import LoadDataMixin from '../mixins/LoadDataMixin.js'

export default {

    name: 'me',

    data () {
        return {
            me: {
                username: '',
                email: '',
                forename: '',
                surname: ''
            }
        }
    },

    methods: {

        load () {
            this.$api.post('/user/me')
                .then((response) => {
                    this.loaded('Sucess')
                    this.me = response.data
                })
                .catch((error) => {
                    this.error(':\'S', error)
                })
        }
    },

    mixins: [LoadDataMixin]
}
</script>
