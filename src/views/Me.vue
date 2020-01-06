<template>
<div>
    <div v-if="loaded">
        Username: {{me.username}} <br>
        email: {{me.email}} <br>
        forename: {{me.forename}} <br>
        surname: {{me.surname}}
    </div>
    <div v-else>
        Could not load your data.
    </div>
    </div>
</template>

<script>
export default {

    name: 'me',

    data () {
        return {
            loaded: false,
            me: {
                username: '',
                email: '',
                forename: '',
                surname: ''
            }
        }
    },

    mounted () {
        this.$api.post('/user/me')
                .then((response) => {
                    window.UIkit.notification('Loaded')
                    this.loaded = true
                    this.me = response.data
                })
                .catch((error) => {
                    console.log(error)
                })
    }
}
</script>
