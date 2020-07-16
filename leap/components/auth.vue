<template>
  <b-container>
    <b-row>
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
              <div class="text-center">
                <googleAuth class="google_btn" :is-login="action" />
                <p class="text-center mt-4">
                  Or
                </p>
              </div>
            </b-col>
          </b-row>
          <b-row v-if="action === 'signup'" align-h="center">
            <b-col cols="4 mt-4">
              <b-form-input
                v-if="action === 'signup'"
                v-model="userInfo.first_name"
                class="inputs bg-light form-control-lg"
                type="text"
                required
                placeholder="First Name"
              />
            </b-col>
            <b-col cols="4 mt-4">
              <b-form-input
                v-if="action === 'signup'"
                v-model="userInfo.last_name"
                class="inputs bg-light form-control-lg"
                type="text"
                required
                placeholder="Last Name"
              />
            </b-col>
          </b-row>
          <b-row align-h="center">
            <b-col :cols="action === 'login' ? 6 : 8" class="mt-4">
              <b-form-input
                v-model="userInfo.email"
                class="inputs bg-light form-control-lg"
                type="email"
                required
                placeholder="Email ID"
              />
            </b-col>
          </b-row>
          <b-row align-h="center">
            <b-col :cols="action === 'login' ? 6 : 4" class="mt-4">
              <b-form-input
                v-model="userInfo.password"
                type="password"
                class="inputs bg-light form-control-lg"
                required
                placeholder="Password"
              />
            </b-col>
            <b-col v-if="action === 'signup'" cols="4">
              <b-form-input
                v-model="userInfo.re_password"
                type="password"
                class="inputs bg-light form-control-lg mt-4"
                required
                placeholder="Confirm Password"
              />
            </b-col>
          </b-row>
          <b-row>
            <b-col offset-md="7">
              <p v-if="action === 'login'" class="text-danger-dark mt-3">
                Forgot Password
              </p>
            </b-col>
          </b-row>
          <b-row v-if="action === 'signup'" class="mt-4">
            <b-col offset-md="2" cols="2">
              <b-form-radio v-model="userInfo.role" name="role_btn" value="Candidate" size="md">
                Candidate
              </b-form-radio>
            </b-col>
            <b-col cols="2">
              <b-form-radio v-model="userInfo.role" name="role_btn" value="Interviewer" size="md">
                Interviewer
              </b-form-radio>
            </b-col>
          </b-row>
          <b-row :class="action === 'login' ? 'mt-2' : 'mt-5'">
            <b-col offset-md="5">
              <b-button class="submit_btn" variant="primary" @click="submitForm">
                Submit
              </b-button>
            </b-col>
          </b-row>
          <b-row v-if="action === 'signup'">
            <b-col>
              <p class="text-center text-secondary mt-4">
                Already have an account
                <NuxtLink to="/auth/login" class="font-weight-bold">
                  Login
                </NuxtLink>
              </p>
            </b-col>
          </b-row>
          <b-row v-if="action === 'login'">
            <b-col>
              <p class="text-center text-secondary mt-4">
                Don't have an account
                <NuxtLink to="/auth/signup" class="font-weight-bold">
                  SignUp
                </NuxtLink>
              </p>
            </b-col>
          </b-row>
          <b-row>
            <b-col align-self="end">
              <p class="text-right mr-4 text-secondary bottom_text">
                <small>&copy; 2020 Stellar Software Technologies Pvt ltd</small>
              </p>
            </b-col>
          </b-row>
        </b-form>
      </b-container>
    </b-row>
  </b-container>
</template>

<script>
import googleAuth from '~/components/GoogleAuth'

export default {
  components: {
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
      }
    }
  },
  methods: {
    submitForm () {
      this.$store.dispatch(this.action, this.userInfo)
    }
  }
}
</script>

<style scoped>
.google_btn {
  margin-left: 32%;
}
.inputs {
  font-size: 1rem;
  border: 1px #F4F4F4;
}
</style>
