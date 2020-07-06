<template>
  <b-container>
    <auth :submitForm="loginUser" login="true" />
  </b-container>
</template>

<script>
import auth from '~/components/auth'

export default {
  middleware: 'notAuthenticated',
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
