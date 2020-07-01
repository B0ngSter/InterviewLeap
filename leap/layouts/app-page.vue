<template>
  <div>
    <b-navbar variant="faded" type="light">
      <b-navbar-brand to="/">
        <Logo />
      </b-navbar-brand>
    </b-navbar>
    <Nuxt />
  </div>
</template>

<script>
import Logo from '~/components/Logo'
export default {
  components: {
    Logo
  }
}
</script>
