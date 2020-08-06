
export default {
  /*
  ** Nuxt rendering mode
  ** See https://nuxtjs.org/api/configuration-mode
  */
  mode: 'universal',
  /*
  ** Nuxt target
  ** See https://nuxtjs.org/api/configuration-target
  */
  target: 'server',
  /*
  ** Headers of the page
  ** See https://nuxtjs.org/api/configuration-head
  */
  head: {
    title: process.env.npm_package_name || '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: process.env.npm_package_description || '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ],
    script: [{ src: 'https://apis.google.com/js/api:client.js' }]
  },
  /*
  ** Global CSS
  */
  css: [
    '~/assets/theme.scss'
  ],
  /*
  ** Plugins to load before mounting the App
  ** https://nuxtjs.org/guide/plugins
  */
  plugins: [
    { src: '~/plugins/axios.js' },
    { src: '~/plugins/vee-validate.js' }
  ],
  /*
  ** Auto import components
  ** See https://nuxtjs.org/api/configuration-components
  */
  components: true,
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
    // Doc: https://github.com/nuxt-community/eslint-module
    '@nuxtjs/eslint-module'
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
    // Doc: https://bootstrap-vue.js.org
    [
      'bootstrap-vue/nuxt', {
        icons: true
      }
    ],
    // Doc: https://axios.nuxtjs.org/usage
    '@nuxtjs/axios',
    '@nuxtjs/auth',
    '@nuxtjs/toast',
    'cookie-universal-nuxt',
    'js-cookie',
    'cookieparser'
  ],
  /*
  ** Axios module configuration
  ** See https://axios.nuxtjs.org/options
  */
  router: {
    middleware: ['auth']
  },
  axios: {
    baseURL: process.env.NODE_ENV === 'dev' ? 'http://localhost:8000' : 'https://api.interviewleap.com'
  },
  auth: {
    redirect: {
      home: '/profile'
    },
    strategies: {
      customGoogleAuth: {
        _scheme: '~/schemes/customGoogleAuth',
        endpoints: {
          login: { url: '/auth/google-signin', method: 'post', propertyName: 'access_token' },
          user: { url: '/auth/profile', method: 'get', propertyName: 'profile' },
          logout: false
        }
      },
      local: {
        endpoints: {
          login: { url: '/auth/login', method: 'post', propertyName: 'access' },
          user: { url: '/auth/profile', method: 'get', propertyName: 'profile' },
          logout: false
        }
        // tokenRequired: false,
        // tokenType: false
      }
    }
  },
  toast: {
    position: 'bottom-center',
    duration: 5000 // default timeout of 5 seconds
  },

  /*
  ** Build configuration
  ** See https://nuxtjs.org/api/configuration-build/
  */
  build: {
    transpile: ['@nuxtjs/auth', 'vee-validate/dist/rules']
  }
}
