<template>
    <div class="uk-section">
        <h1 class="uk-text-center uk-margin-large">Account</h1>
        <div class="uk-container uk-container-xsmall">
            <div class="uk-grid-divider" uk-grid>
                <div class="uk-width-3-5@m">
                    <UserEdit :user="currentUser" />
                </div>
                <div class="uk-width-2-5@m">
                    <ChangePassword :id="currentUser.id" />
                    <hr>
                    <ChangeEmail :id="currentUser.id" :email="currentUser.email" />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import UserEdit from '@/components/UserEdit'
import ChangePassword from '@/components/ChangePassword'
import ChangeEmail from '@/components/ChangeEmail'
import { mapState } from 'vuex'

export default {

    name: 'me',

    computed: {
        ...mapState({
            currentUser: state => state.security.currentUser
        })
    },

    components: {
        UserEdit,
        ChangePassword,
        ChangeEmail
    }
}
</script>
