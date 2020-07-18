<template>
  <section>
    <b-navbar toggleable="lg">
      <b-navbar-brand to="/">
        <Logo />
      </b-navbar-brand>
    </b-navbar>
    <b-container class="page-content">
      <b-row no-gutters class="justify-content-center flex-fill">
        <b-col cols="12" class="d-flex align-items-center justify-content-center">
          <Nuxt />
        </b-col>
      </b-row>
    </b-container>
  </section>
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
.container {
  margin: 0 auto;
  min-height: calc(100vh - 84px);
  display: flex;
  padding-bottom: 84px;
}
</style>
