export default function ({ app, store }) {
  app.router.onReady(() => {
    app.store.dispatch('update_meta_data_from_cookie')
  })
}
