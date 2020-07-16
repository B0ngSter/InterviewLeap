<template>
  <b-container>
    <b-row align-v="center">
      <auth
        action="signup"
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
