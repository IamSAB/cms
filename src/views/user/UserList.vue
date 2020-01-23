<template>
    <div>
        <table class="uk-table uk-table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Forename</th>
                    <th>Surname</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in users" :key="user.id">
                    <td>{{ user.id }}</td>
                    <td>{{ user.username }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.forename }}</td>
                    <td>{{ user.surname }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
export default {

    data () {
        return {
            users: 'user'
        }
    },

    mounted () {
        this.$api.get('/users')
        .then(response => {
            this.users = response.data.users
        })
    }
}
</script>
