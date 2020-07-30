<template>
  <div>
    <g-signin-button
      :params="googleSignInParams"
      @success="onSignInSuccess"
      @error="onSignInError"
    >
      <b-button
        class="google_btn bg-white"
        :loading="$store.state.google_login"
        block
        outlined
        large
      >
        <span class="text-secondary">Continue with</span><img class="ml-3" src="@/static/logos/google.svg" alt="">
      </b-button>
    </g-signin-button>
    <b-modal
      id="modal-center"
      v-model="show"
      title-class="font-weight-bold text-center w-100 mt-2"
      header-class="p-2 border-bottom-0 font-weight-bold"
      centered
      title-tag="h3"
      hide-footer
      size="xl"
      title="You are a"
    >
      <b-container>
        <b-row>
          <b-col>
            <b-img
              class="cursor-pointer"
              src="@/static/candidate.svg"
              alt="Candidate logo"
              height="308"
              @click="role_select('Candidate')"
            />
            <p class="text-center mt-4 font-weight-bold">
              Candidate
            </p>
          </b-col>
          <b-col>
            <b-img
              class="cursor-pointer"
              src="@/static/interviewer.svg"
              alt="Candidate logo"
              height="308"
              @click="role_select('Interviewer')"
            />
            <p class="text-center mt-4 font-weight-bold">
              Interviewer
            </p>
          </b-col>
        </b-row>
      </b-container>
    </b-modal>
  </div>
</template>

<script>
import Vue from 'vue'
import GSignInButton from 'vue-google-signin-button'

Vue.use(GSignInButton)

export default {
  props: {
    isLogin: {
      type: String,
      required: true
    }
  },
  data: () => {
    return {
      selected_role: null,
      googleSignInParams: {
        client_id: '792788771362-cundr764n1vlps2nqd63mtdmcqr9fii5.apps.googleusercontent.com'
      },
      show: false,
      auth_token: null
    }
  },
  methods: {
    onSignInSuccess (googleUser) {
      const authResponse = googleUser.getAuthResponse()
      this.auth_token = authResponse.id_token
      this.google_auth()
    },
    role_select (value) {
      this.show = false
      this.selected_role = value
      this.google_auth()
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
    },
    google_auth () {
      this.$auth.loginWith('customGoogleAuth', { data: { id_token: this.auth_token, role: this.selected_role } })
        .catch((response) => {
          if (response.response.status === 307) {
            this.show = true
          } else {
            this.$toast.error(response.response.data.message || 'Oops.. Unable to log you in at the moment', {
              action: {
                text: 'Close',
                onClick: (e, toastObject) => {
                  toastObject.goAway(0)
                }
              }
            })
          }
        })
    }
  }
}
</script>

<style>
.google_btn {
  padding: 1rem 5rem;
}
</style>
