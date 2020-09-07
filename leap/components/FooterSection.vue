<template>
  <section class="bg-dark text-white py-5">
    <b-container fluid>
      <b-row class="justify-content-center py-5">
        <b-col cols="11" md="7">
          <div class="d-flex flex-column flex-md-row">
            <Logo dark_long class="mx-0" />
            <b-button variant="outline-light" class="ml-auto mr-auto mr-md-0 mt-5 mt-md-0">Get Started</b-button>
          </div>
        </b-col>
        <b-col cols="11" md="7">
          <div class="pt-5 font-weight-bold d-flex flex-column flex-md-row">
            <div class="mb-5 mb-md-0 d-flex flex-column flex-md-row text-center">
              <nuxt-link to="/" class="mr-0 mr-md-3 text-white">Home</nuxt-link>
              <nuxt-link to="/candidate" class="mr-0 mr-md-3 text-white">For Candidates</nuxt-link>
              <nuxt-link to="/interviewer" class="mr-0 mr-md-3 text-white">For Interviewers</nuxt-link>
              <nuxt-link to="/about" class="text-white">About</nuxt-link>
            </div>
            <div class="mr-auto mr-md-0 ml-auto">
              <a href="#" class="text-white mr-3">
                <b-img height="25" width="25" contain src="~/static/icons/linkedin.svg" />
              </a>
              <a href="#" class="text-white">
                <b-img height="25" width="25" contain src="~/static/icons/instagram.svg" />
              </a>
            </div>
          </div>
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
