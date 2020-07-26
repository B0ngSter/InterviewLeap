export default function ({ store, $axios, redirect }) {
  $axios.onError((error) => {
    if (error.response.status === 401) {
      // Logout here and redirect to login page
      redirect('/auth/login')
    }
  })
}
