<template>
  <section class="d-flex flex-fill">
    <b-container>
      <b-row align-h="center" align-v="center">
        <b-col cols="11" md="8" lg="6" class="text-center text-joyful-dark">
          <h3 class="mb-5 text-dark">
            Reset your password
          </h3>
          <div v-if="$route.query.token">
            <b-form-input
              v-model="password"
              class="bg-light border-0"
              type="password"
              required
              placeholder="Enter your new password"
            />
            <b-form-input
              v-model="re_password"
              class="bg-light border-0"
              type="password"
              required
              placeholder="Re-Enter your new password"
            />
            <div class="text-center mt-5">
              <b-button variant="primary" @click="set_password">
                <b-icon-reply-fill />
                Update my password
              </b-button>
            </div>
          </div>
          <div v-else>
            <p>
              Forgot your password? Don’t worry, we all do ;)
            </p>
            <p>
              We’ll send you instructions to reset your password to
              your registered email address
            </p>
            <b-form-input
              v-model="email"
              class="bg-light border-0"
              type="email"
              required
              placeholder="Enter your email ID"
            />
            <div class="text-center mt-5">
              <b-button variant="primary" @click="send_instructions">
                <b-icon-reply-fill />
                Send me instructions
              </b-button>
            </div>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </section>
</template>

<script>
export default {
  layout: 'auth',
  auth: 'guest',
  asyncData ({ $axios, query, redirect }) {
    if (query.token) {
      return $axios.post('/auth/password-reset/validate_token/', {
        token: query.token
      })
        .catch((errorResponse) => {
          alert(errorResponse.response.data.message || 'Invalid/Expired token')
          redirect('/')
        })
    }
  },
  data () {
    return {
      email: null,
      password: null,
      re_password: null
    }
  },
  methods: {
    send_instructions () {
      this.$axios.post('/auth/password-reset/', { email: this.email })
        .then((response) => {
          this.$router.push(`/email-sent?email=${this.email}&context=Password-reset`)
        })
        .catch((errorResponse) => {
          this.$toast.error(
            errorResponse.response.data.message || 'Something went wrong, please try again later'
          )
        })
    },
    set_password () {
      this.$axios.post('/auth/password-reset/', { email: this.email })
        .then((response) => {
          this.$router.push('/auth/email-sent')
        })
        .catch((errorResponse) => {
          this.$toast.error(
            errorResponse.response.data.message || 'Something went wrong, please try again later'
          )
        })
    }
  }
}
</script>
