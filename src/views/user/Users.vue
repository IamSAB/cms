<template>
    <div>
        <ul class="uk-iconnav">
            <li><a @click="edit(user.id)" uk-icon="plus"></a></li>
            <template>
                <li><a @click="status(2)" uk-icon="ban"></a></li>
                <li><a @click="status(1)" uk-icon="check"></a></li>
            </template>
        </ul>
        <table class="uk-table uk-table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Forename</th>
                    <th>Surname</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in users" :key="user.id">
                    <td><input type="ckeckbox" class="uk-checkbox" name="selected"></td>
                    <td>{{ user.username }}</td>
                    <td>{{ user.email }}</td>
                    <td>{{ user.forename }}</td>
                    <td>{{ user.surname }}</td>
                    <td>
                        <ul class="uk-iconnav">
                            <li><a @click="edit(user.id)" uk-icon="file-edit"></a></li>
                            <li><a @click="remove(user.id)" uk-icon="trash"></a></li>
                        </ul>
                    </td>
                </tr>
            </tbody>
        </table>
        <div ref="modal-edit" class="uk-modal-full" uk-modal>
            <div class="uk-modal-dialog">
                <button class="uk-modal-close-full uk-close-large" type="button" uk-close></button>
                <div class="uk-section" v-if="user">
                    <div class="uk-container">
                        <ul class="uk-iconnav">
                            <li><a @click="prev(user.id)" uk-icon="icon: chevron-left"></a></li>
                            <li><a @click="next(user.id)" uk-icon="icon: chevron-right"></a></li>
                        </ul>
                        <div class="uk-child-width-1-3@m" uk-grid>
                            <div>
                                <UserEdit :data="user"/>
                            </div>
                            <div>
                                <ChangePassword :id="user.id"/>
                                <ChangeEmail :id="user.id" :email="user.email"/>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div ref="modal-register" class="uk-modal-full" uk-modal>
            <div class="uk-modal-dialog">
                <button class="uk-modal-close-full uk-close-large" type="button" uk-close></button>
                <div class="uk-section" v-if="user">
                    <div class="uk-container">
                        <UserRegister :admin="true"/>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import UserEdit from '@/components/UserEdit'
import ChangePassword from '@/components/ChangePassword'
import ChangeEmail from '@/components/ChangeEmail'

export default {

    data () {
        return {
            selected: [],
            users: [],
            user: null
        }
    },

    mounted () {
        this.$securedApi.get('/users')
        .then(response => {
            this.users = response.data.users
        })
        this.modalRegister = this.UI.modal(this.$refs.modalRegister)
        this.modalEdit = this.UI.modal(this.$refs.modalEdit)
    },

    methods: {

        prev (id) {
            const index = this.findUserIndex(id)
            if (index === 0) {
                this.user = this.users[this.users.length - 1]
            } else {
                this.user = this.users[index - 1]
            }
        },

        next (id) {
            const index = this.findUserIndex(id)
            if (index === this.users.length - 1) {
                this.user = this.users[0]
            } else {
                this.user = this.users[index + 1]
            }
        },

        findUserIndex (id) {
            return this.users.findIndex(user => user.id === id)
        },

        register () {
            this.registerModal.show()
        },

        edit (id) {
            this.user = this.users.find(user => user.id === id)
            this.modalEdit.show()
        },

        remove (id) {
            this.$api.delete(`/user/${id}`)
        }
    },

    components: {
        UserEdit,
        ChangePassword,
        ChangeEmail
    }
}
</script>
