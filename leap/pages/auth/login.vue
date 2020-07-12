<template>
  <b-container class="Container">
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
  data () {
    return {
    }
  },
  components: {
    auth
  },
  methods: {
    loginUser (loginInfo) {
      const payload = { ...loginInfo }
      delete payload.role
      this.$store.dispatch('login', payload)
    }
  }
}
</script>
<style>
.Container {
  margin-top: 10vh;
}
</style>
