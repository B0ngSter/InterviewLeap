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
      <b-modal v-if="isLogin === 'signup'" v-model="show" id="modal-sm" size="sm" title="How you wants to login">
        <b-container>
          <b-row>
            <b-col>
              <b-form-radio v-model="selected_role"  name="role_btn" value="Candidate" size="md">Candidate</b-form-radio>
            </b-col>
            <b-col>
              <b-form-radio v-model="selected_role" name="role_btn"  value="Interviewer" size="md">Interviewer</b-form-radio>
            </b-col>
          </b-row>
        </b-container>
        <template v-slot:modal-footer>
          <div class="text-center">
            <div class="w-100">
              <b-button
                variant="primary"
                size="sm"
                @click="continue_with_role"
              >
                Continue
              </b-button>
            </div>
          </div>
      </template>
      </b-modal>
    </p>
  </div>
</template>

<script>
import Vue from 'vue'
import GSignInButton from 'vue-google-signin-button'

Vue.use(GSignInButton)

export default {
  props: ['isLogin'],
  data: () => {
    return {
      selected_role: false,
      googleSignInParams: {
        client_id: '792788771362-cundr764n1vlps2nqd63mtdmcqr9fii5.apps.googleusercontent.com'
      },
      show: false,
      auth_token: null
    }
  },
  methods: {
    onSignInSuccess (googleUser) {
      this.show = true
      const authResponse = googleUser.getAuthResponse()
      this.auth_token = authResponse.id_token
    },
    continue_with_role () {
      this.show = false
      this.$store.dispatch('google_auth', {
        id_token: this.auth_token,
        role: this.selected_role
      })
    },
    onSignInError (error) {
      let errorText
      if (error.error === 'popup_closed_by_user') {
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
