<template>
    <div class="uk-section">
        <div class="uk-container uk-container-xsmall">
            <UserRegister/>
        </div>
    </div>
</template>

<script>
import UserRegister from '@/components/UserRegister'

export default {

    name: 'register',

    components: {
        UserRegister
    }
}
</script>
