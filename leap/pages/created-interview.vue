<template>
  <div class="full-height">
    <b-container>
      <b-row class="mt-5">
        <b-col cols="12" md="5" class="mt-2 pt-2">
          <h2 class="font-weight-bold">
            Hello, {{ this.$store.state.auth.user.first_name }}
          </h2>
          <p class="text-secondary pt-2">
            Below are the interviews you have created
          </p>
        </b-col>
        <b-col offset-md="2" cols="12" md="5" class="mt-2 pt-2">
          <div class="text-right">
            <b-button class="text-white" to="/create-interview" variant="primary">
              Create an Interview >
            </b-button>
          </div>
        </b-col>
        <b-col v-if="created_interviews.length === 0" cols="12" md="12" class="pb-5 mb-5">
          <div class="text-center">
            <b-img
              class="cursor-pointer mt-5"
              src="@/static/kio.svg"
              alt="Mock"
              height="308"
            />
            <p class="font-weight-bold mt-5">
              No interviews found2222
            </p>
          </div>
        </b-col>
        <b-col v-for="(interviews, idx) in created_interviews" :key="idx" cols="12" class="mt-3">
          <b-card no-body class="text-center border-0">
            <b-container class="bg-white">
              <b-row class="p-4 mt-3">
                <b-col cols="6" md="4">
                  <p class="text-left text-secondary">
                    {{ interviews.job_title }}
                  </p>
                  <p class="text-left text-dark font-weight-bold">
                    {{ interviews.exp_years }} years
                  </p>
                </b-col>
                <b-col cols="3" md="2" offset-md="4">
                  <b-button squared class="alert-danger text-danger-dark" @click="deleteInterview(interviews.slug, idx)">
                    Delete
                  </b-button>
                </b-col>
                <b-col cols="3" md="2">
                  <b-button squared class="alert-success text-primary" :to="`/create-interview/${created_interviews[idx].slug}`">
                    Edit
                  </b-button>
                </b-col>
              </b-row>
            </b-container>
          </b-card>
        </b-col>
        <b-col cols="12">
          <div class="text-center text-secondary mt-5">
            2020 Stellar Software Technologies Pvt ltd
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  layout: 'app-page',
  data () {
    return {
      report: null,
      created_interviews: []
    }
  },
  mounted () {
    this.fetch_interview()
  },
  methods: {
    fetch_interview () {
      this.$axios.get('/interview/create-interview/').then((response) => {
        this.created_interviews = response.data
      })
        .catch((errorResponse) => {
          this.$toast.error(
            errorResponse.response.data.message || 'Something went wrong'
          )
        })
    },
    deleteInterview (slug, idx) {
      this.$axios.delete(`/interview/create-interview?slug=${slug}`).then((response) => {
        this.created_interviews.splice(idx, 1)
        this.$toast.success(response.data.message, {
          action: {
            text: 'Close',
            onClick: (e, toastObject) => {
              toastObject.goAway(0)
            }
          }
        })
      })
        .catch((errorResponse) => {
          this.$toast.error(
            errorResponse.response.data.message || 'Something went wrong'
          )
        })
    }
  }
}
</script>

<style>
.full-height {
  min-height: 100vh
}
</style>
