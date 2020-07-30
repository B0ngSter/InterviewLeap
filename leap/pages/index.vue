<template>
  <div class="container">
    <div>
      <Logo />
      <h1 class="title">
        InterviewLeap
      </h1>
      <div class="links">
        <b-button variant="primary" to="/test">
          Test App page
        </b-button>
        <NuxtLink to="/login">
          login
        </NuxtLink>
        <NuxtLink to="/signup">
          Sign Up
        </NuxtLink>
        <p>
          loggedIn? <b>{{ this.$auth.loggedIn }}</b>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  auth: false
}
</script>

<style scoped>
.container {
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.title {
  display: block;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}
</style>
