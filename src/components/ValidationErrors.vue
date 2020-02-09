<template>
    <div class="uk-margin" v-if="hasErrors">
        <div v-for="(message, index) in errors" :key="index" class="uk-alert uk-alert-danger" uk-alert>
            <p>{{ message }}</p>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ValidationErrors',
    props: {
        errors: {
            type: Array,
            required: true
        }
    },
    methods: {
        hasErrors () {
            return this.errors.length > 0
        }
    }
}
</script>
