<template>
  <b-container>
    <b-row align-v="center">
      <auth
        action="login"
      />
    </b-row>
  </b-container>
</template>

<script>
import auth from '~/components/auth'

export default {
  layout: 'auth',
  components: {
    auth
  }
}
</script>
<style>
</style>
