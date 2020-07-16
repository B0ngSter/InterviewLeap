<template>
  <div>
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
    <b-modal
      v-if="isLogin === 'signup'"
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
      selected_role: false,
      check: null,
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
      if (this.isLogin === 'login') {
        this.$store.dispatch('google_auth', {
          id_token: this.auth_token
        })
      }
    },
    role_select (value) {
      this.selected_role = value
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
