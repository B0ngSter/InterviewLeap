<template>
  <div>
  <b-navbar toggleable="lg">
    <b-navbar-brand href="#">
      <Logo />
    </b-navbar-brand>
    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav class="ml-auto">
       <b-nav-item @click="select_role('candidate')"><p v-bind:class="isActive == true ? 'text-primary' : 'text-secondary'" class="font-weight-bold">Candidate</p></b-nav-item>
       <b-nav-item @click="select_role('interviewer')"><p v-bind:class="isActive == false ? 'text-primary' : 'text-secondary'" class="font-weight-bold">Interviewer</p></b-nav-item>
       <!-- <b-nav-item v-if="signUp"><p>New User</p><a>Sign Up</a></b-nav-item> -->
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
    <auth
      :submitForm="signUpUser"
      :spinner="spinner"
      :disable_the_submit_btn="disable_the_submit_btn"
      signUp="true"
      :isCandidate="isActive"
      :isInterviewer="!isActive"
    />
    <p class="text-center text-secondary">Already have an account <strong>
      <NuxtLink to="/auth/login">
        Log In
      </NuxtLink>
    </strong></p>
    <p class="text-right mr-4 text-secondary bottom_text"><small>&copy; 2020 Stellar Software Technologies Pvt ltd</small></p>
  </div>
</template>

<script>
import auth from '~/components/auth'
import Logo from '~/components/Logo'
export default {
  data () {
    return {
      isActive: true,
      role: null,
      disable_the_submit_btn: false,
      spinner: false
    }
  },
  components: {
    auth,
    Logo
  },
  methods: {
    signUpUser (UserInfo) {
      const authData = { ...UserInfo }
      this.isActive ? authData.role = 'candidate' : authData.role = 'interviewer'
      this.$store.dispatch('signup', {
        payload: authData,
        callback: () => { this.$router.push(`/auth/email-sent?email=${authData.email}`) }
      })
      // this.spinner = true
      // this.disable_the_submit_btn = true
    },
    select_role (role) {
      this.role = role
      role === 'candidate' ? this.isActive = true : this.isActive = false
      this.$store.dispatch('role_for_signup', this.isActive)
    }
  }
}
</script>

<style >
/* .text--light {
  color: #82919c;
  font-size: 16px;
  line-height: 21px;
}
.bottom_text {
  color: #82919c;
  font-size: 14px;
  line-height: 17px;
} */
</style>
