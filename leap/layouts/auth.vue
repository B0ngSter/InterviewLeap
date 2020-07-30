<template>
  <section>
    <b-navbar toggleable="lg">
      <b-navbar-brand to="/">
        <Logo />
      </b-navbar-brand>
    </b-navbar>
    <b-container class="page-content flex-column">
      <b-row no-gutters class="justify-content-center flex-fill">
        <b-col cols="12" class="d-flex align-items-center justify-content-center">
          <Nuxt />
        </b-col>
      </b-row>
      <b-row>
        <b-col align-self="end">
          <p class="text-right mr-5 mt-4 text-secondary bottom_text">
            <small>&copy; 2020 Stellar Software Technologies Pvt ltd</small>
          </p>
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
