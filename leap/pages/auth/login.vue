<template>
  <section class="d-flex flex-fill">
    <b-container>
      <b-row align-v="center">
        <auth
          action="login"
        />
      </b-row>
    </b-container>
  </section>
</template>

<script>
import auth from '~/components/auth'

export default {
  middleware ({ store, redirect }) {
    if (store.getters.is_authenticated) {
      store.dispatch('post_login_routing')
    }
  },
  layout: 'auth',
  components: {
    auth
  }
}
</script>
<style>
</style>
