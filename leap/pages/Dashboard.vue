<template>
  <b-container>
    <b-row class="mt-5">
      <b-col cols="12" md="3" class="pb-5 mb-5">
        <h3 class="font-weight-bold">
          Hello, {{ this.$store.state.auth.user.first_name }}
        </h3>
        <p class="text-secondary">
          Your upcoming interviews
        </p>
      </b-col>
      <b-col v-if="upcoming_interviews == null" cols="12" md="6" class="pb-5 mb-5">
        <div class="text-center">
          <b-img
            class="cursor-pointer"
            src="@/static/kio.svg"
            alt="Mock"
            height="308"
          />
          <p class="font-weight-bold">
            No interview scheduled for now
          </p>
        </div>
      </b-col>
      <b-col cols="12">
        <b-card v-for="(interviews, idx) in upcoming_interviews" :key="idx" no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row>
              <b-col :cols="this.$store.state.is_mock ? 3 : 4" class="pt-5 pb-5 pl-4">
                <p class="text-left text-secondary">
                  Date
                </p>
                <p class="text-left text-dark font-weight-bold">
                  {{ date() }}
                </p>
              </b-col>
              <b-col v-if="this.$store.state.is_mock" cols="3" class="pt-5 pb-5 pl-4">
                <p class="text-left text-secondary">
                  Interview from
                </p>
                <p class="text-left text-danger-dark font-weight-bold">
                  {{ interviews.job_title }}
                </p>
              </b-col>
              <b-col cols="3" offset-md="2">
                <div class="mt-5 mb-5">
                  <b-button squared class="alert-danger text-danger-dark" @click="cancel">
                    Cancel
                  </b-button>
                </div>
              </b-col>
              <b-col cols="3">
                <div class="mt-5 mb-5">
                  <b-button squared class="alert-primary text-primary" @click="reschedule">
                    Reschedule
                  </b-button>
                </div>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col cols="12">
        <mockInterviewListing />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>import mockInterviewListing from '~/components/mockInterviewListing'
export default {
  layout: 'app-page',
  components: {
    mockInterviewListing
  },
  data () {
    return {
      upcoming_interviews: [
        {
          date: '2020-08-21',
          job_title: 'Byjus',
          slug: 'rvfw5lvb'
        },
        {
          date: '2020-08-21',
          job_title: 'Byjus',
          slug: 'ip3fjjmo'
        }
      ]
    }
  },
  mounted () {
    this.$axios.get('/dashboard/')
      .then((response) => {
      })
  },
  methods: {
    date () {
      let month = ''
      this.upcoming_interviews.date.slice(5, 7).includes('0') ? month = this.upcoming_interviews.date.slice(6, 7) : month = this.upcoming_interviews.date.slice(5, 7)
      const monthList = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
      month = monthList[parseInt(month) - 1]
      const date = this.upcoming_interviews.date.slice(8, 10)
      const year = this.upcoming_interviews.date.slice(0, 4)
      const amplifiedDate = month + ' ' + date + ',' + year
      const day = String(new Date(amplifiedDate))
      return day.slice(0, 3) + ',' + day.slice(3, 10) + ', ' + day.slice(11, 16)
    },
    reschedule (idx) {
      this.$router.push('/book-mock?id=${' + this.upcoming_interviews[idx].slug + '}')
    },
    cancel (idx) {},
    fetch_interview () {
      this.$axios.get('/Interview-list/').then((response) => {
        this.upcoming_interviews = response.data.upcoming_interviews
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
</style>
