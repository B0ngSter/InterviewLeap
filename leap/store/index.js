export const state = () => {
  return {
    access_token: null,
    is_authenticated: false,
    role: null,
    full_name: null,
    is_profile_completed: false,
    is_candidate: null,
    is_interviewer: null,
    profile_picture: null
  }
}
export const mutations = {
  profile_status (state) {
    state.is_profile_completed = true
  },
  authentication_status (state) {
    state.is_authenticated = true
  },
  role_is_interviewer (state) {
    state.is_interviewer = true
  },
  role_is_candidate (state) {
    state.is_candidate = true
  },
  user_data (state, user) {
    state.profile_picture = user.profile_picture
    state.full_name = user.full_name
  },
  logged_out (state) {
    state.is_interviewer = null
    state.is_authenticated = false
    state.is_candidate = null
  },
  update_meta_data_from_cookie (context) {
    let getMetaData = this.$cookies.get('meta_data')
    try {
      if (!getMetaData) {
        throw new Error('Token not found')
      }
      if (typeof getMetaData === 'string') {
        getMetaData = JSON.parse(getMetaData)
      }
      state.full_name = getMetaData.full_name
      state.role = getMetaData.role
      state.is_profile_completed = getMetaData.is_profile_completed
    } catch (err) {
      state.full_name = null
      state.role = null
      state.is_profile_completed = null
    }
    const token = this.$cookies.get('auth_token')
    state.is_authenticated = !!token
    if (state.is_authenticated) {
      this.$axios.setToken(token, 'Bearer')
    } else {
      this.$axios.setToken(null)
    }
  }
}
export const actions = {
  signup (context, signupArgs) {
    this.$axios.post('/auth/signup', signupArgs)
      .then((response) => {
        this.$router.push('/auth/email-sent')
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
    this.$axios.post('/auth/login', payload)
      .then((response) => {
        if (response.status === 200) {
          context.dispatch('set_auth_cookie', response.data.access)
          context.dispatch('set_meta_data_cookie', response.data.meta_data)
          context.commit('authentication_status')
          context.commit('user_data', response.data.meta_data)
          if (response.data.meta_data.role === 'Interviewer') {
            context.commit('role_is_interviewer')
          } else if (response.data.meta_data.role === 'Candidate') {
            context.commit('role_is_candidate')
          }
          context.dispatch('post_login_routing')
        }
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
  post_login_routing (context) {
    let nextRoute = ''
    if (!context.getters.is_profile_completed) {
      nextRoute = '/profile'
    }
    this.$router.push(nextRoute)
  },
  set_auth_cookie (context, token) {
    this.$cookies.set('auth_token', token, {
      path: '/',
      maxAge: 60 * 60 * 24 * 7
    })
  },
  set_meta_data_cookie (context, metaData) {
    this.$cookies.set('meta_data', JSON.stringify(metaData), {
      path: '/',
      maxAge: 60 * 60 * 24 * 7
    })
    context.commit('update_meta_data_from_cookie')
  },
  logout (context) {
    this.$cookies.remove('auth_token')
    this.$cookies.remove('meta_data')
    context.commit('update_meta_data_from_cookie')
    context.commit('logged_out')
    this.$router.push('/')
    this.$toast.info('You have logged out successfully!', {
      action: {
        text: 'Close',
        onClick: (e, toastObject) => {
          toastObject.goAway(0)
        }
      }
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
  is_authenticated (state) {
    return state.is_authenticated
  },
  is_profile_completed (state) {
    return state.is_profile_completed
  },
  user_name (state) {
    return state.full_name
  },
  profile_pic (state) {
    return state.profile_picture
  },
  role (state) {
    return state.role
  },
  is_interviewer (state) {
    return state.is_interviewer
  },
  is_candidate (state) {
    return state.is_candidate
  }
}
