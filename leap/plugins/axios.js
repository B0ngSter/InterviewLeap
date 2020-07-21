export default function ({ store, $axios, redirect }) {
  $axios.onError((error) => {
    if (error.response.status === 401) {
      console.log('Login to continue')
      // Logout here and redirect to login page
      redirect('/auth/login')
    }
  })
}
