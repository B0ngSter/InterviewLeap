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
          active-class="text-primary"
        >
          {{ item.title }}
        </b-nav-item>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item-dropdown right>
          <template v-slot:button-content>
            <span class="font-weight-bold">{{ $store.state.auth.user.first_name }}</span>
            <b-img
              rounded
              :src="$store.getters.profile_pic"
              height="50"
              class="ml-3"
            />
          </template>
          <b-dropdown-item to="/profile" class="border-bottom border-light" active-class="text-dark">
            <p class="p-3 mt-2">
              <span>
                <b-img
                  src="@/static/login.svg"
                  alt="InterviewLeap logo"
                />
              </span>
              <span class="pl-3">Profile</span>
            </p>
          </b-dropdown-item>
          <b-dropdown-item v-if="$store.getters.is_interviewer" to="/transaction" class="border-bottom border-light" active-class="text-dark">
            <p class="p-3 mt-2">
              <span>
                <b-img
                  src="@/static/pay.svg"
                  alt="InterviewLeap logo"
                />
              </span>
              <span class="pl-3">Transactions</span>
            </p>
          </b-dropdown-item>
          <b-dropdown-item to="/profile" class="border-bottom border-light" active-class="text-dark">
            <p class="p-3 mt-2">
              <span>
                <b-img
                  src="@/static/headphones.svg"
                  alt="InterviewLeap logo"
                />
              </span>
              <span class="pl-3">Support</span>
            </p>
          </b-dropdown-item>
          <b-dropdown-item class="bg-primary" active-class="text-white" @click="logout">
            <b-button variant="primary" style="width: 100%;" class="text-white">
              Logout
            </b-button>
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
  computed: {
    nav_items () {
      let routes
      if (this.$store.getters.is_candidate) {
        routes = [
          {
            title: 'Dashboard',
            route: '/dashboard'
          }, {
            title: 'Book an Interview',
            route: '/book-interview'
          }, {
            title: 'Past Interviews',
            route: '/past-interview'
          }, {
            title: 'Profile',
            route: '/profile'
          }, {
            title: 'FAQs',
            route: '/faqs'
          }
        ]
      } else if (this.$store.getters.is_interviewer) {
        routes = [
          {
            title: 'Dashboard',
            route: '/dashboard'
          }, {
            title: 'Create Interview',
            route: '/create-interview'
          }, {
            title: 'Profile',
            route: '/profile'
          }, {
            title: 'Interview Requests',
            route: '/interview-request'
          }, {
            title: 'FAQs',
            route: '/faqs'
          }
        ]
      }
      return routes
    }
  },
  methods: {
    async logout () {
      await this.$auth.logout()
    }
  }
}
</script>
<style>
.hoover:hover {
  background-color: #5dcc99;
}
.navbar-nav .dropdown-menu {
  padding: 0;
}
</style>
