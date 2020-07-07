<template>
  <b-container fluid="">
    <b-row no-gutters>
      <b-navbar variant="light" type="light" fixed="top">
        <b-navbar-brand to="/">
          <Logo />
        </b-navbar-brand>
      </b-navbar>
    </b-row>
    <b-row no-gutters class="mt-84">
      <b-col cols="12">
        <Nuxt />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import Logo from '~/components/Logo'
export default {
  components: {
    Logo
  }
}
</script>

<style scoped>
.mt-84 {
  padding-top: 84px;
}
</style>
