<template>
  <section>
    <Navbar />
    <b-container fluid="" class="bg-light page-content">
      <b-row no-gutters class="justify-content-center">
        <b-col cols="12" md="10">
          <Nuxt />
        </b-col>
      </b-row>
    </b-container>
  </section>
</template>

<script>
import Navbar from '~/components/app-navbar'

export default {
  components: {
    Navbar
  }
}
</script>

<style scoped>
.container {
  margin: 0 auto;
  min-height: calc(100vh - 84px);
  display: flex;
}
.page-content {
  margin-top: 84px;
}
</style>
