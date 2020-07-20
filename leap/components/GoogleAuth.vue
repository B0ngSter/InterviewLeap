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
      this.$axios.post('/auth/google-signin', { id_token: this.auth_token, role: this.selected_role })
        .then((response) => {
          if (response.status === 204) {
            this.show = true
          }
        })
    },
    role_select (value) {
      this.show = false
      this.selected_role = value
      this.$axios.post('/auth/google-signin', { id_token: this.auth_token, role: this.selected_role })
        .then((response) => {
          if (response.status === 204) {
            this.show = true
            if (response.data.access_token) {
              this.$store.dispatch('set_auth_cookie', response.data.access_token)
              this.$store.dispatch('set_meta_data_cookie', response.data.meta_data)
              if (response.data.meta_data.role === 'Interviewer') {
                this.$store.commit('role_is_interviewer')
              } else if (response.data.meta_data.role === 'Candidate') {
                this.$store.commit('role_is_candidate')
              }
              this.$store.commit('authentication_status')
              this.$store.dispatch('post_login_routing')
            }
          }
          if (response.status === 200) {
            debugger
            // if (response.data.access_token) {
            //   this.show = true
            //   this.$store.dispatch('set_auth_cookie', response.data.access_token)
            //   this.$store.dispatch('set_meta_data_cookie', response.data.meta_data)
            //   if (response.data.meta_data.role === 'Interviewer') {
            //     this.$store.commit('role_is_interviewer')
            //   } else if (response.data.meta_data.role === 'Candidate') {
            //     this.$store.commit('role_is_candidate')
            //   }
            //   this.$store.commit('authentication_status')
            //   this.$store.dispatch('post_login_routing')
            // }
          }
        })
        .catch((response) => {
          this.$toast.error(response.response.data.message || 'Oops.. Unable to log you in at the moment', {
            action: {
              text: 'Close',
              onClick: (e, toastObject) => {
                toastObject.goAway(0)
              }
            }
          })
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
.google_btn {
  padding: 1rem 5rem 1rem 5rem;
}
</style>
