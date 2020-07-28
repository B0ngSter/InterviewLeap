<template>
  <b-navbar fixed="top" variant="white" class="px-5 border-bottom" toggleable="md">
    <b-navbar-brand to="/">
      <Logo />
    </b-navbar-brand>
    <b-navbar-toggle target="nav-collapse" />
    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item
          v-for="(item, idx) in nav_items"
          :key="idx"
          :to="item.route"
          class="font-weight-bold"
          active-class="active"
        >
          {{ item.title }}
        </b-nav-item>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item-dropdown right>
          <template v-slot:button-content>
            <span class="font-weight-bold">{{ name }}</span>
            <b-img
              rounded
              src="https://cdn.zeplin.io/5ef9852ffe48f580cf1a311f/assets/C37953A1-4038-456B-A85A-B309B9EE174D.png"
              height="50"
              class="ml-3"
            />
          </template>
          <b-dropdown-item to="/profile" active-class="active">
            Profile
          </b-dropdown-item>
          <b-dropdown-item @click="$store.dispatch('logout')">
            Logout
          </b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
import Logo from '~/components/Logo'
export default {
  components: {
    Logo
  },
  data () {
    return {
      name: ''
    }
  },
  computed: {
    nav_items () {
      let routes
      if (this.$store.getters.is_candidate) {
      // const [a, b] = [1, 1]
      // if (a === b) {
        routes = [
          {
            title: 'Dashboard',
            route: '/dashboard'
          }, {
            title: 'Book an Interview',
            route: '/book-interview'
          }, {
            title: 'Past Interviews',
            route: 'create-interview'
          }, {
            title: 'Profile',
            route: '/profile'
          }, {
            title: 'FAQs',
            route: 'faqs'
          }
        ]
      } else if (this.$store.getters.is_interviewer) {
        routes = [
          {
            title: 'Dashboard',
            route: '/dashboard'
          }, {
            title: 'Create Interview',
            route: '/interviewer/create-interview'
          }, {
            title: 'Profile',
            route: '/profile'
          }, {
            title: 'Interview Requests',
            route: 'requests'
          }, {
            title: 'FAQs',
            route: 'faqs'
          }
        ]
      }
      return routes
    }
  },
  mounted () {
    this.name = this.$store.getters.user_name
  }
}
</script>
