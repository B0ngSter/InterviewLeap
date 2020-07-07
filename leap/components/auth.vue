<template>
<b-container>
    <b-form id="auth_form">
      <b-row>
        <b-col cols="12">
          <h2 v-if="isCandidate" class="text-center header_text">Sign Up <span class="text-primary">for Candidate</span></h2>
          <h2 v-if="isInterviewer" class="text-center header_text">Sign Up <span class="text-primary">for Interviewer</span></h2>
          <h2 class="text-center header_text font-weight-bold" v-if="login">Log In</h2>
          <div class="text-center">
            <p class="google_btn">
              <googleAuth />
            </p>
            <p class="text-center mt-4">Or</p>
          </div>
        </b-col>
        <b-col cols="2"></b-col>
        <b-col cols="4 mt-4">
            <b-form-input
              class="inputs bg-light form-control-lg"
              v-model="userInfo.first_name"
              v-if="signUp"
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
              v-if="signUp"
              required
              placeholder="Last Name"
            >
            </b-form-input>
        </b-col>
        <b-col cols="2"></b-col>
        <b-col cols="2"></b-col>
        <b-col cols="8 mt-4">
            <b-form-input
              class="inputs bg-light form-control-lg"
              v-model="userInfo.email"
              type="email"
              v-if="signUp"
              required
              placeholder="email"
            ></b-form-input>
        </b-col>
        <b-col cols="2"></b-col>
        <b-col cols="3"></b-col>
        <b-col cols="6">
            <b-form-input
              class="inputs bg-light form-control-lg"
              v-model="userInfo.email"
              type="email"
              v-if="!signUp"
              required
              placeholder="email"
            ></b-form-input>
        </b-col>
        <b-col cols="3"></b-col>
        <b-col cols="3"></b-col>
        <b-col cols="6 mt-4">
            <b-form-input
              class="inputs bg-light form-control-lg"
              v-model="userInfo.password"
              v-if="!signUp"
              required
              placeholder="Password"
            ></b-form-input>
        </b-col>
        <b-col cols="3"></b-col>
        <b-col cols="2"></b-col>
        <b-col cols="4">
            <b-form-input
              class="inputs bg-light form-control-lg"
              v-model="userInfo.password"
              v-if="signUp"
              required
              placeholder="Password form-control-lg"
            ></b-form-input>
        </b-col>
        <b-col cols="4">
            <b-form-input
              class="inputs bg-light form-control-lg"
              v-model="userInfo.re_password"
              v-if="signUp"
              required
              placeholder="Confirm Password"
            ></b-form-input>
        </b-col>
        <b-col cols="2"></b-col>
        <b-col cols="5"></b-col>
        <b-col cols="4">
          <div class="text-right mt-3" v-if="!signUp"><p class="text-danger" >Forgot Password</p></div>
        </b-col>
        <b-col cols="3"></b-col>
        <b-col cols="4"></b-col>
        <b-col cols="4 mt-4">
          <b-button class="submit_btn" :disabled="disable_the_submit_btn" @click="submitForm(userInfo)" variant="primary">
            <b-spinner v-if="spinner" small></b-spinner>
            <span v-if="!spinner">Submit</span></b-button>
        </b-col>
        <b-col cols="4"></b-col>
      </b-row>
    </b-form>
</b-container>
</template>

<script>
import googleAuth from '~/components/google_auth'

export default {
  props: ['submitForm', 'signUp', 'isCandidate', 'isInterviewer', 'login', 'disable_the_submit_btn', 'spinner'],
  data () {
    return {
      userInfo: {
        role: '',
        email: 'micromini57@gmail.com',
        password: '12162221N'
      }
    }
  },
  components: {
    googleAuth
  }
}
</script>

<style scoped>
.container {
  min-height: 80vh;
}
/* .forgot_pass {
  color: #FF7959;
  text-decoration: underline;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
}
.header_text {
  font-size: 2rem;
  font-weight: bold;
  line-height: 2.563rem;
}
.head_color {
    color: #5DCC99;
}
.submit_btn {
  padding: 1rem 4rem 1rem 4rem;
  border: 0px;
  margin-top: 2rem;
  height: 3.75rem;
}
.inputs {
  width: 100%;
  border: 1px #F4F4F4;
  margin-top: 15px;
  height: 3.75rem;
  font-size: 1rem;
  border-radius: 0px;
  background-color: #F7F8FC;
}
.inputs::placeholder {
  padding: 20px;
  font-size: 1rem;
}
.inputs:focus {
  border: 0px;
} */
.google_btn {
  margin-left: 32%;
}
.inputs {
  font-size: 1rem;
  border: 1px #F4F4F4;
}
</style>
