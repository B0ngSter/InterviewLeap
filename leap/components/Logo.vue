<template>
  <b-img
    class="InterviewLeapLogo"
    :src="dark_long ? require('@/static/logos/dark.svg') : require('@/static/logos/icon.svg')"
    alt="InterviewLeap logo"
    height="58"
  />
</template>

<style>
.InterviewLeapLogo {
  animation: 1s appear;
  margin: auto;
}

@keyframes appear {
  0% {
    opacity: 0;
  }
}
</style>

<script>
export default {
  props: {
    dark_long: {
      type: Boolean,
      default: false
    }
  }
}
</script>
