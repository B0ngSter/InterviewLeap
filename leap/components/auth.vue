<template>
  <b-container>
    <b-row align-h="center" align-v="center">
      <b-container>
        <b-form id="auth_form">
          <b-row>
            <b-col cols="12">
              <h2 v-if="action === 'login'" class="text-center header_text font-weight-bold">
                Log In
              </h2>
              <h2 v-if="action === 'signup'" class="text-center header_text font-weight-bold">
                Signup
              </h2>
            </b-col>
          </b-row>
          <b-row class="justify-content-center mt-5">
            <googleAuth :is-login="action" />
          </b-row>
          <p class="text-center mt-4">
            Or
          </p>
          <b-row v-if="action === 'signup'" align-h="center">
            <b-col cols="12" md="4" class="mt-4">
              <b-form-group>
                <b-form-input
                  v-if="action === 'signup'"
                  v-model="$v.userInfo.first_name.$model"
                  class="inputs bg-light"
                  required
                  placeholder="First Name"
                  :state="validateState('first_name')"
                  aria-describedby="input-1-live-feedback"
                />
                <b-form-invalid-feedback
                  id="input-1-live-feedback"
                >
                  This is a required field.
                </b-form-invalid-feedback>
              </b-form-group>
            </b-col>
            <b-col cols="12" md="4" class="mt-4">
              <b-form-group>
                <b-form-input
                  v-if="action === 'signup'"
                  v-model="$v.userInfo.last_name.$model"
                  class="inputs bg-light"
                  required
                  type="text"
                  placeholder="Last Name"
                  :state="validateState('last_name')"
                  aria-describedby="input-1-live-feedback"
                />
                <b-form-invalid-feedback
                  id="input-1-live-feedback"
                >
                  This is a required field.
                </b-form-invalid-feedback>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row align-h="center">
            <b-col cols="12" :md="action === 'login' ? 6 : 8" class="mt-4">
              <b-form-group>
                <b-form-input
                  v-model="$v.userInfo.email.$model"
                  class="inputs bg-light"
                  required
                  type="email"
                  placeholder="Email ID"
                  :state="validateState('email')"
                  aria-describedby="input-1-live-feedback"
                />
                <b-form-invalid-feedback
                  id="input-1-live-feedback"
                >
                  This is a required field.
                </b-form-invalid-feedback>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row align-h="center">
            <b-col cols="12" :md="action === 'login' ? 6 : 4" class="mt-4">
              <b-form-group>
                <b-form-input
                  v-model="$v.userInfo.password.$model"
                  class="inputs bg-light"
                  required
                  type="password"
                  placeholder="Password"
                  :state="validateState('password')"
                  aria-describedby="input-1-live-feedback"
                />
                <b-form-invalid-feedback
                  id="input-1-live-feedback"
                >
                  This is a required field.
                </b-form-invalid-feedback>
              </b-form-group>
            </b-col>
            <b-col v-if="action === 'signup'" cols="12" md="4">
              <b-form-group>
                <b-form-input
                  v-if="action === 'signup'"
                  v-model="$v.userInfo.confirm_password.$model"
                  class="inputs bg-light mt-4"
                  type="password"
                  required
                  placeholder="Confirm Password"
                  :state="validateState('confirm_password') && userInfo.confirm_password === userInfo.password"
                  aria-describedby="input-1-live-feedback"
                />
                <b-form-invalid-feedback
                  id="input-1-live-feedback"
                >
                  This is a required field.
                </b-form-invalid-feedback>
              </b-form-group>
            </b-col>
          </b-row>
          <b-row align-h="center">
            <b-col cols="12" :md="action === 'login' ? 6 : 4">
              <p v-if="action === 'login'" class="mt-2">
                <NuxtLink to="/password-reset" class="text-danger-dark">
                  Forgot Password? Click to reset
                </NuxtLink>
              </p>
            </b-col>
          </b-row>
          <b-row v-if="action === 'signup'" class="mt-4">
            <b-col offset-md="2" cols="4" md="2">
              <b-form-radio v-model="userInfo.role" name="role_btn" value="Candidate" size="md">
                Candidate
              </b-form-radio>
            </b-col>
            <b-col cols="4" md="2">
              <b-form-radio v-model="userInfo.role" name="role_btn" value="Interviewer" size="md">
                Interviewer
              </b-form-radio>
            </b-col>
          </b-row>
          <b-row :class="action === 'login' ? 'mt-2' : 'mt-5'">
            <b-col offset-md="5" offset="3">
              <b-button
                v-if="action === 'signup'"
                :disabled="!userInfo.first_name || !userInfo.role || !userInfo.confirm_password || !userInfo.password || !userInfo.email || !userInfo.last_name"
                class="submit_btn text-white"
                variant="primary"
                @click="submitForm"
              >
                <span>SignUp</span>
              </b-button>
              <b-button
                v-if="action === 'login'"
                :disabled="!userInfo.password || !userInfo.email"
                class="submit_btn text-white"
                variant="primary"
                @click="submitForm"
              >
                <span>Login</span>
              </b-button>
            </b-col>
          </b-row>
          <b-row v-if="action === 'signup'">
            <b-col>
              <p class="text-center text-secondary mt-4">
                Already have an account?
                <NuxtLink to="/login" class="font-weight-bold">
                  Login here
                </NuxtLink>
              </p>
            </b-col>
          </b-row>
          <b-row v-if="action === 'login'">
            <b-col>
              <p class="text-center text-secondary mt-4">
                Don't have an account?
                <NuxtLink to="/signup" class="font-weight-bold">
                  SignUp here
                </NuxtLink>
              </p>
            </b-col>
          </b-row>
        </b-form>
      </b-container>
    </b-row>
  </b-container>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, email } from 'vuelidate/lib/validators'
import googleAuth from '~/components/GoogleAuth'
export default {
  components: {
    googleAuth
  },
  mixins: [validationMixin],
  props: {
    action: {
      type: String,
      required: true
    }
  },
  data () {
    return {
      userInfo: {
        first_name: null,
        last_name: null,
        email: 'nit35h.7@gmail.com',
        password: '12162221N',
        confirm_password: null
      }
    }
  },
  validations: {
    userInfo: {
      first_name: { required },
      last_name: { required },
      password: { required },
      confirm_password: { required },
      email: { required, email }
    }
  },
  methods: {
    validateState (name) {
      const { $dirty, $error } = this.$v.userInfo[name]
      return $dirty ? !$error : null
    },
    submitForm () {
      if (this.action === 'login') {
        delete this.userInfo.first_name
        delete this.userInfo.last_name
        delete this.userInfo.confirm_password
      }
      this.$store.dispatch(this.action, {
        Authpayload: this.userInfo,
        callback: () => { this.$router.push(`/email-sent?email=${this.userInfo.email}&context=signup`) }
      })
    }
  }
}
</script>

<style scoped>
.inputs {
  font-size: 1rem;
  border: 1px #F4F4F4;
}
</style>
