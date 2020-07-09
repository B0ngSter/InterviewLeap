<template>
<b-container>
  <b-row>
    <b-container>
      <b-form id="auth_form">
        <b-row>
          <b-col cols="12">
            <h2 class="text-center header_text font-weight-bold" v-if="action === 'login'">Log In</h2>
            <h2 class="text-center header_text font-weight-bold" v-if="action === 'signup'">Signup</h2>
            <div class="text-center">
              <p class="google_btn">
                <googleAuth :isLogin="action" />
              </p>
              <p class="text-center mt-4">Or</p>
            </div>
          </b-col>
        </b-row>
        <b-row align-h="center" v-if="action === 'signup'">
          <b-col cols="4 mt-4">
            <b-form-input
              class="inputs bg-light form-control-lg"
              v-model="userInfo.first_name"
              v-if="action === 'signup'"
              type="text"
              required
              placeholder="First Name"
            >
            </b-form-input>
          </b-col>
          <b-col cols="4 mt-4">
              <b-form-input
                class="inputs bg-light form-control-lg"
                v-model="userInfo.last_name"
                type="text"
                v-if="action === 'signup'"
                required
                placeholder="Last Name"
              >
              </b-form-input>
          </b-col>
        </b-row>
        <b-row align-h="center">
          <b-col cols="8 mt-4">
              <b-form-input
                class="inputs bg-light form-control-lg"
                v-model="userInfo.email"
                type="email"
                v-if="action === 'signup'"
                required
                placeholder="email"
              ></b-form-input>
          </b-col>
        </b-row>
        <b-row align-h="center">
          <b-col cols="6">
              <b-form-input
                class="inputs bg-light form-control-lg"
                v-model="userInfo.email"
                type="email"
                v-if="action === 'login'"
                required
                placeholder="email"
              ></b-form-input>
          </b-col>
        </b-row>
        <b-row align-h="center" >
          <b-col cols="6 mt-4">
              <b-form-input
                class="inputs bg-light form-control-lg"
                v-model="userInfo.password"
                v-if="action === 'login'"
                required
                placeholder="Passwordw"
              ></b-form-input>
          </b-col>
        </b-row>
        <b-row align-h="center" v-if="action === 'signup'">
          <b-col cols="4">
              <b-form-input
                class="inputs bg-light form-control-lg"
                v-model="userInfo.password"
                v-if="action === 'signup'"
                required
                placeholder="Password"
              ></b-form-input>
          </b-col>
          <b-col cols="4">
              <b-form-input
                class="inputs bg-light form-control-lg"
                v-model="userInfo.re_password"
                v-if="action === 'signup'"
                required
                placeholder="Confirm Password"
              ></b-form-input>
          </b-col>
        </b-row>
        <b-row>
          <b-col offset-md="7">
              <p class="text-danger mt-3" v-if="action === 'login'">Forgot Password</p>
          </b-col>
        </b-row>
        <b-row v-if="action === 'signup'" class="mt-4">
          <b-col offset-md="3">
            <b-form-radio v-model="userInfo.role"  name="role_btn" value="Candidate" size="md">Candidate</b-form-radio>
          </b-col>
          <b-col>
            <b-form-radio v-model="userInfo.role" name="role_btn"  value="Interviewer" size="md">Interviewer</b-form-radio>
          </b-col>
        </b-row>
        <b-row class="mt-2" v-if="action === 'login'">
          <b-col offset-md="5">
            <b-button class="submit_btn" @click="submitForm" variant="primary">
              Submit
            </b-button>
          </b-col>
        </b-row>
        <b-row class="mt-5" v-if="action === 'signup'">
          <b-col offset-md="5">
            <b-button class="submit_btn" @click="submitForm" variant="primary">
              Submit
            </b-button>
          </b-col>
        </b-row>
        <b-row v-if="action === 'signup'">
          <b-col>
            <p class="text-center text-secondary mt-4">Already have an account
              <NuxtLink to="/auth/login" class="font-weight-bold">
                Login
              </NuxtLink>
            </p>
          </b-col>
        </b-row>
        <b-row v-if="action === 'login'">
          <b-col>
            <p class="text-center text-secondary mt-4">Don't have an account
              <NuxtLink to="/auth/signup" class="font-weight-bold">
                SignUp
              </NuxtLink>
            </p>
          </b-col>
        </b-row>
        <b-row>
          <b-col align-self="end">
            <p class="text-right mr-4 text-secondary bottom_text"><small>&copy; 2020 Stellar Software Technologies Pvt ltd</small></p>
          </b-col>
        </b-row>
      </b-form>
    </b-container>
  </b-row>
</b-container>
</template>

<script>
import googleAuth from '~/components/google_auth'

export default {
  props: ['action'],
  data () {
    return {
      userInfo: {}
    }
  },
  components: {
    googleAuth
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
