export default function ({ store, redirect }) {
  if (!store.getters.is_authenticated) {
    return redirect('/')
  }
}
