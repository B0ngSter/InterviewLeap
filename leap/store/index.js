const Cookie = process.client ? require('js-cookie') : undefined

export const state = () => {
  return {
    access_token: null,
    is_authenticated: false,
    role: null,
    full_name: null,
    is_profile_completed: null
  }
}
export const mutations = {
  setAuth (state, payload) {
    state.access_token = payload.access_token
    state.is_authenticated = payload.is_authenticated
    state.role = payload.role
    state.is_profile_completed = payload.is_profile_completed
    state.full_name = payload.full_name
  },
  end_google_authenticating (state) {
    state.google_login = false
  },
  profile_status (state) {
    state.is_profile_completed = true
  }
}
export const actions = {
  signup (context, signupArgs) {
    this.$axios.post('/auth/signup', signupArgs)
      .then((response) => {
        context.dispatch('set_auth_cookie', response.data.access_token)
        context.dispatch('set_meta_data_cookie', response.data.meta_data)
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
        console.log(response)
        if (response.status === 200) {
          const auth = {
            access_token: response.data.access_token,
            is_authenticated: true,
            role: response.data.meta_data.role,
            is_profile_completed: response.data.meta_data.is_profile_completed,
            full_name: response.data.meta_data.full_name
          }
          debugger
          context.commit('set_role', response.data.meta_data.role)
          if (response.data.meta_data.is_profile_completed) {
            context.commit('profile_status')
          }
          this.$router.push('/')
          context.dispatch('post_login_routing')
          this.$store.commit('setAuth', auth)
          Cookie.set('auth', auth)
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
    if (context.getters.is_candidate) {
      nextRoute = '/dashboard/'
    } else if (context.getters.is_interviewer) {
      nextRoute = '/kuch or'
    }
    this.$router.push(nextRoute)
  },
  google_auth (context, payload) {
    debugger
    this.$axios.post('/auth/google-signin', payload)
      .then((response) => {
        console.log(response)
        debugger
        if (response.status === 200) {
          if (response.data.access_token) {
            context.dispatch('set_auth_cookie', response.data.access_token)
            context.dispatch('set_meta_data_cookie', response.data.meta_data)
            // context.dispatch('post_login_routing')
            this.$router.push('/auth/email-sent')
          }
        } else {
          this.$toast.error((response.data && response.data.message) ? response.data.message : 'Login failed.. please try again', {
            action: {
              text: 'Close',
              onClick: (e, toastObject) => {
                toastObject.goAway(0)
              }
            }
          })
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
      .finally(() => {
        context.commit('end_google_authenticating')
      })
  },
  role_for_signup (context, role) {
    context.commit('role_for_google_signup', role)
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
  update_meta_data_from_cookie (state) {
    let metaData = this.$cookies.get('meta_data')
    try {
      if (!metaData) {
        throw new Error('Token not found')
      }
      if (typeof metaData === 'string') {
        metaData = JSON.parse(metaData)
      }
      state.role = metaData.role
      state.is_profile_completed = metaData.is_profile_completed
    } catch (err) {
      state.role = null
      state.is_profile_complete = null
    }
    const token = this.$cookies.get('auth_token')
    state.is_authenticated = !!token
    if (state.is_authenticated) {
      this.$axios.setToken(token, 'Bearerw')
    } else {
      this.$axios.setToken(null)
    }
  },
  set_industry_choices (state, industriesData) {
    state.industry_choices = industriesData
  }
}
export const getters = {
  is_authenticated (state) {
    return state.is_authenticated
  },
  is_profile_completed (state) {
    return state.is_profile_completed
  },
  full_name (state) {
    return state.full_name
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
