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
              <ValidationProvider
                v-slot="{ valid, errors }"
                rules="required"
              >
                <b-form-group>
                  <b-input
                    v-if="action === 'signup'"
                    v-model="userInfo.first_name"
                    class="inputs bg-light"
                    type="text"
                    required
                    placeholder="First Name"
                    :state="errors[0] ? false : (valid ? true : null)"
                  />
                  <b-form-invalid-feedback id="inputLiveFeedback">
                    {{ errors[0] }}
                  </b-form-invalid-feedback>
                </b-form-group>
              </ValidationProvider>
            </b-col>
            <b-col cols="12" md="4" class="mt-4">
              <ValidationProvider
                v-slot="{ valid, errors }"
                rules="required"
              >
                <b-form-group>
                  <b-input
                    v-if="action === 'signup'"
                    v-model="userInfo.last_name"
                    class="inputs bg-light"
                    type="text"
                    required
                    placeholder="Last Name"
                    :state="errors[0] ? false : (valid ? true : null)"
                  />
                  <b-form-invalid-feedback id="inputLiveFeedback">
                    {{ errors[0] }}
                  </b-form-invalid-feedback>
                </b-form-group>
              </ValidationProvider>
            </b-col>
          </b-row>
          <b-row align-h="center">
            <b-col cols="12" :md="action === 'login' ? 6 : 8" class="mt-4">
              <ValidationProvider v-slot="{ valid, errors }" rules="required|email" name="Email">
                <b-form-input
                  v-model="userInfo.email"
                  class="inputs bg-light"
                  type="email"
                  required
                  placeholder="Email ID"
                  :state="errors[0] ? false : (valid ? true : null)"
                />
                <b-form-invalid-feedback id="inputLiveFeedback">
                  {{ errors[0] }}
                </b-form-invalid-feedback>
              </ValidationProvider>
            </b-col>
          </b-row>
          <b-row align-h="center">
            <b-col cols="12" :md="action === 'login' ? 6 : 4" class="mt-4">
              <ValidationProvider
                v-slot="{ valid, errors }"
                rules="required"
                name="Password"
                vid="password"
              >
                <b-form-input
                  v-model="userInfo.password"
                  type="password"
                  class="inputs bg-light"
                  required
                  placeholder="Password"
                  :state="errors[0] ? false : (valid ? true : null)"
                />
                <b-form-invalid-feedback id="inputLiveFeedback">
                  {{ errors[0] }}
                </b-form-invalid-feedback>
              </ValidationProvider>
            </b-col>
            <b-col v-if="action === 'signup'" cols="12" md="4">
              <ValidationProvider
                v-slot="{ valid, errors }"
                rules="required|confirmed:password"
                name="Password confirmation"
              >
                <b-form-input
                  v-model="userInfo.confirm_password"
                  type="password"
                  class="inputs bg-light mt-4"
                  required
                  placeholder="Confirm Password"
                  :state="errors[0] ? false : (valid ? true : null)"
                />
                <b-form-invalid-feedback id="inputLiveFeedback">
                  {{ errors[0] }}
                </b-form-invalid-feedback>
              </ValidationProvider>
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
              <b-button v-if="action === 'signup'" :disabled="!userInfo.first_name || !userInfo.role || !userInfo.confirm_password || !userInfo.password || !userInfo.email || !userInfo.last_name" class="submit_btn" variant="primary" @click="submitForm">
                <span>SignUp</span>
              </b-button>
              <b-button v-if="action === 'login'" :disabled="!userInfo.password || !userInfo.email" class="submit_btn" variant="primary" @click="submitForm">
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
import { ValidationProvider } from 'vee-validate'
import googleAuth from '~/components/GoogleAuth'

export default {
  components: {
    ValidationProvider,
    googleAuth
  },
  props: {
    action: {
      type: String,
      required: true
    }
  },
  data () {
    return {
      userInfo: {
        email: 'nit35h.7@gmail.com',
        password: '12162221N'
      }
    }
  },
  methods: {
    submitForm () {
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
