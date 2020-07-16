<template>
  <b-container class="bg-light">
    <commonProfile />
  </b-container>
</template>

<script>
import commonProfile from '~/components/CommonProfile'

export default {
  layout: 'app-page',
  middleware: ['isauthenticated'],
  components: {
    commonProfile
  },
  data: () => {
    return {
    }
  }
}
</script>

<style>
</style>
