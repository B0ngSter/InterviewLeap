export const state = () => {
  return {
  }
}

export const actions = {
  signup (context, signupArgs) {
    this.$axios.post('/auth/signup', { ...signupArgs.Authpayload })
      .then((response) => {
        // this.$router.push('/email-sent')
        signupArgs.callback()
      })
      .catch((errorResponse) => {
        this.$toast.error(
          errorResponse.response.data.message || 'Unable to signup at the moment, please try again later',
          {
            action: {
              text: 'Close',
              onClick: (e, toastObject) => {
                toastObject.goAway(0)
              }
            }
          }
        )
      })
  },
  login (context, payload) {
    this.$auth.loginWith('local', { data: payload.Authpayload })
      .then((response) => {
        this.$axios.get('/book-interview/')
          .then((response) => {
            if (response.data.is_profile_completed) {
              this.$router.push('/dashboard')
            }
          })
      })
      .catch((errorResponse) => {
        this.$toast.error(
          errorResponse.response.data.message || 'Unable to login at the moment, please try again later',
          {
            action: {
              text: 'Close',
              onClick: (e, toastObject) => {
                toastObject.goAway(0)
              }
            }
          }
        )
      })
  },
  verify_verification_token (context, args) {
    this.$axios.post(`auth/verify-user/${args.verification_token}`)
      .then((response) => {
        if (response.data.is_token_valid) {
          args.successCallback()
        } else {
          args.errorCallback(response)
        }
      })
      .catch((errorResponse) => {
        args.errorCallback(errorResponse)
      })
  }
}

export const getters = {
  is_profile_completed (state) {
    return state.auth.user.is_profile_completed
  },
  full_name (state) {
    return state.auth.user.first_name + ' ' + state.auth.user.last_name
  },
  profile_pic (state) {
    return state.auth.user.profile_picture
  },
  role (state) {
    return state.auth.user.role
  },
  is_interviewer (state) {
    return state.auth.user.role === 'Interviewer'
  },
  is_candidate (state) {
    return state.auth.user.role === 'Candidate'
  }
}
