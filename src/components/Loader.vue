<template>
    <div>
        <div v-if="status == 0" class="uk-flex uk-flex-center">
            <div uk-spinner="ratio: 3"></div>
        </div>
        <slot v-else-if="status == 1"></slot>
        <div v-else class="uk-flex uk-flex-center">
            <h3 class="uk-text-muted">Fehler beim Laden</h3>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        status: {
            type: Number,
            required: true
        }
    }
}
</script>
