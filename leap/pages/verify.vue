<template>
  <b-container>
    <b-row>
      <b-col cols="12" class="mt-5 pt-5">
        <div class="text-center">
          <b-spinner variant="primary" style="width: 6rem; height: 6rem;" label="Large Spinner Text Centered" />
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  auth: false,
  mounted () {
    const errorCallback = (response) => {
      this.$toast.error((response.data && response.data.message) ? response.data.message : "We could'nt verify your account.", {
        action: {
          text: 'Close',
          onClick: (e, toastObject) => {
            toastObject.goAway(0)
          }
        }
      })
      this.$router.push('/')
    }
    const successCallback = (response) => {
      this.$toast.success('You email has been verified, please login now', {
        action: {
          text: 'Close',
          onClick: (e, toastObject) => {
            toastObject.goAway(0)
          }
        }
      })
      this.$router.push('/login')
    }
    if (this.$route.query.token) {
      this.$store.dispatch('verify_verification_token', {
        verification_token: this.$route.query.token,
        successCallback,
        errorCallback
      })
    } else {
      errorCallback()
    }
  }
}
</script>

<style>

</style>
