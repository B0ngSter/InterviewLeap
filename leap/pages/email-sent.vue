<template>
  <b-container>
    <b-row class="ml-5 pl-5">
      <b-col cols="12">
        <div class="text-center">
          <b-img
            src="@/static/email.svg"
            alt="Candidate logo"
            height="308"
          />
        </div>
      </b-col>
      <b-col cols="12">
        <h3 class="text-center text-weight-bold mt-5">
          Email Verification
          <br>
        </h3>
        <p class="text-center text-secondary mt-3 mb-5">
          Verify your email address to get started in Interview Leap
        </p>
        <div class="text-center mt-5">
          <p>Didn’t receive verification mail ?</p>
          <p class="text-danger-dark text-weight-bold cursor-pointer" @click="resend">
            Resend
          </p>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  layout: 'auth',
  auth: 'guest',
  methods: {
    resend () {
      let endpoint
      if (this.$route.query.context === 'signup') {
        endpoint = 'auth/resend-email/'
      } else if (this.$route.query.context === 'Password-reset') {
        endpoint = 'auth/password-reset/validate_token/'
      }
      this.$axios.post(endpoint, { email: this.$route.query.email }).then((res) => {
        this.$toast.info('Email sent successfully!', {
          action: {
            text: 'Close',
            onClick: (e, toastObject) => {
              toastObject.goAway(0)
            }
          }
        })
      })
    }
  }
}
</script>

<style>
</style>
