<template>
  <div>
    <p>
      <g-signin-button
        :params="googleSignInParams"
        @success="onSignInSuccess"
        @error="onSignInError"
      >
        <b-button
          class="btn_top"
          :loading="$store.state.google_login"
          block
          outlined
          large
        >
        <span class="text-secondary">Continue with</span><img class="ml-3" src="@/static/logos/google.svg" alt="">
        </b-button>
      </g-signin-button>
    </p>
  </div>
</template>

<script>
import Vue from 'vue'
import GSignInButton from 'vue-google-signin-button'

Vue.use(GSignInButton)

export default {
  data: () => {
    return {
      googleSignInParams: {
        client_id: '792788771362-cundr764n1vlps2nqd63mtdmcqr9fii5.apps.googleusercontent.com'
      }
    }
  },
  methods: {
    onSignInSuccess (googleUser) {
      const authResponse = googleUser.getAuthResponse()
      authResponse.role = this.$store.getters.role
      debugger
      this.$store.dispatch('google_auth', authResponse.id_token)
    },
    onSignInError (error) {
      let errorText
      if (error.error === 'popup_closed_by_user') {
        errorText = 'The authentication was not completed'
        errorText = 'The authentication was not completed'
      }
      this.notification = {
        visibility: true,
        text: errorText,
        color: 'error'
      }
    }
  }
}
</script>

<style>
.btn_top {
  padding: 1rem 5rem 1rem 5rem;
  background-color: white;
  color: #0e293c;
  cursor: pointer;
  height: 3.75rem;
  width: 25rem;
  margin-top: 5%;
}
.btn_top:hover {
  background-color: white;
  color: #0e293c;
}
.btn_top:focus {
  background-color: white;
  color: #0e293c;
}
</style>
