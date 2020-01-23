<template>
    <div>
        Username: {{me.username}} <br>
        email: {{me.email}} <br>
        forename: {{me.forename}} <br>
        surname: {{me.surname}}
    </div>
</template>

<script>

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

    mounted () {
        this.$api.get('/me')
            .then((response) => {
                this.me = response.data
            })
    }
}
</script>
