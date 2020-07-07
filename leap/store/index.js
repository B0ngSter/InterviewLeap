const cookieparser = require('cookieparser')
const Cookie = process.client ? require('js-cookie') : undefined

export const state = () => {
  return {
    auth: null,
    is_authenticated: false,
    role: 'candidate',
    full_name: null,
    is_profile_completed: null,
    google_login: false,
    is_candidate: null,
    is_interviewer: null
  }
}
export const mutations = {
  setAuth (state, auth) {
    state.auth = auth
  },
  start_google_authenticating (state) {
    state.google_login = true
  },
  end_google_authenticating (state) {
    state.google_login = false
  },
  login_candidate (state) {
    state.is_candidate = true
  },
  login_interviewer (state) {
    state.is_interviewer = true
  },
  profile_status (state) {
    state.is_profile_completed = true
  },
  role_for_google_signup (state, googleSignupRole) {
    googleSignupRole ? state.role = 'candidate' : state.role = 'interviewer'
  }
}
export const actions = {
  signup (context, signupArgs) {
    this.$axios.post('/auth/signup', signupArgs.payload)
      .then((response) => {
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
    this.$axios.post('/auth/login', payload)
      .then((response) => {
        console.log(response)
        if (response.status === 200) {
          const auth = {
            accessToken: response.data.access
          }
          debugger
          if (response.data.meta_data.role === 'candidate') {
            context.commit('login_candidate')
          } else if (response.data.meta_data.role === 'interviewer') {
            context.commit('login_interviewer')
          }
          if (response.data.meta_data.is_profile_completed) {
            context.commit('profile_status')
          }
          debugger
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
      nextRoute = '/Dashboard/'
    } else if (context.getters.is_interviewer) {
      nextRoute = '/kuch or'
    }
    this.$router.push(nextRoute)
  },
  nuxtServerInit ({ commit }, { req }) {
    let auth = null
    debugger
    if (req.headers.cookie) {
      const parsed = cookieparser.parse(req.headers.cookie)
      try {
        auth = JSON.parse(parsed.auth)
      } catch (err) {
        // No valid cookie found
      }
    }
    commit('setAuth', auth)
  },
  google_auth (context, IDToken) {
    context.commit('start_google_authenticating')
    this.$axios.post('/auth/google-signin', { id_token: IDToken })
      .then((response) => {
        if (response.status === 200) {
          if (response.data.access_token) {
            context.dispatch('set_auth_cookie', response.data.access_token)
            context.dispatch('set_meta_data_cookie', response.data.meta_data)
            context.dispatch('post_login_routing')
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
