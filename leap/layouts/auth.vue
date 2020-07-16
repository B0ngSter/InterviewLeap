<template>
  <section>
    <b-navbar toggleable="lg">
      <b-navbar-brand to="/">
        <Logo />
      </b-navbar-brand>
    </b-navbar>
    <b-container fluid="" class="page-content">
      <b-row no-gutters class="justify-content-center">
        <b-col cols="12" md="10">
          <Nuxt />
        </b-col>
      </b-row>
    </b-container>
  </section>
</template>
<style scoped>
.page-content {
  margin-top: 104px;
}
</style>
