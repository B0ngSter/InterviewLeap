<template>
  <div class="full-height">
    <b-container v-if="!hide_Report_details">
      <b-row class="mt-5">
        <b-col cols="12">
          <b-breadcrumb class="bg-light pl-0">
            <b-breadcrumb-item to="/dashboard">
              Dashboard
            </b-breadcrumb-item>
            <b-breadcrumb-item active>
              Past Interviews
            </b-breadcrumb-item>
          </b-breadcrumb>
        </b-col>
        <b-col cols="12" md="5" class="mt-2 pt-2">
          <h3 class="font-weight-bold">
            Past Interviews
          </h3>
        </b-col>
        <b-col offset-md="4" cols="12" md="3" class="mt-2 pt-2">
          <div class="text-right">
            <b-button class="text-white" variant="primary" to="/book-interview">
              Book interview
            </b-button>
          </div>
        </b-col>
        <b-col v-if="past_interviews.length === 0" cols="12" md="12" class="pb-5 mb-5">
          <div class="text-center">
            <b-img
              class="cursor-pointer mt-5"
              src="@/static/kio.svg"
              alt="Mock"
              height="308"
            />
            <p class="font-weight-bold mt-5">
              No past interviews found
            </p>
          </div>
        </b-col>
        <b-col v-for="(interviews, idx) in past_interviews" :key="idx" cols="12" class="mt-5">
          <b-card no-body class="text-center border-0">
            <b-container class="bg-white">
              <b-row class="p-4 mt-3">
                <b-col class="">
                  <p class="text-left text-secondary">
                    Date. &amp; Time
                  </p>
                  <p class="text-left text-dark font-weight-bold">
                    {{ date(idx) }}, {{ interviews.time_slot }}
                  </p>
                </b-col>
                <b-col v-if="interviews.interview_type === 'Open Mock Interview'" class="">
                  <p class="text-left text-secondary">
                    Interview from
                  </p>
                  <p class="text-left text-danger-dark font-weight-bold">
                    {{ interviews.company }}
                  </p>
                </b-col>
                <b-col md="3" cols="12" offset-md="2">
                  <div class="">
                    <b-button squared class="alert-success text-primary" @click="viewReport(interviews)">
                      View Report
                    </b-button>
                  </div>
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
    <Report
      v-if="hide_Report_details"
      :report="report"
      @Back="hide_Report_details = $event"
    />
  </div>
</template>

<script>
import Report from '~/components/Report'
export default {
  components: {
    Report
  },
  layout: 'app-page',
  data () {
    return {
      report: null,
      hide_Report_details: false,
      past_interviews: [
        // {
        //   time_slots: ['12PM - 3PM'],
        //   company: 'dedes',
        //   date: '2020-08-28',
        //   feedback: {
        //     technical_skill: ['Exceptional', 'good knowledge'],
        //     communicational_skill: ['Meets Requirenment', 'good knowledge'],
        //     presentation_skill: ['Need Training', 'good knowledge'],
        //     understanding_of_role: ['Doesn\'t meet requirenment', 'good knowledge'],
        //     strength: 'coding skills',
        //     limitations: 'understanding the problem',
        //     consider_for_job: 'no'
        //   }
        // },
        // {
        //   time_slots: ['9PM - 12AM'],
        //   date: '2020-08-28',
        //   feedback: {
        //     technical_skill: ['Exceptional', 'good knowledge'],
        //     communicational_skill: ['Exceptional', 'good knowledge'],
        //     presentation_skill: ['Exceptional', 'good knowledge'],
        //     understanding_of_role: ['Exceptional', 'good knowledge'],
        //     strength: 'coding skills',
        //     limitations: 'understanding the problem',
        //     consider_for_job: 'yes'
        //   }
        // }
      ]
    }
  },
  mounted () {
    this.fetch_interview()
  },
  methods: {
    date (idx) {
      let month = ''
      this.past_interviews[idx].date.slice(5, 7).includes('0') ? month = this.past_interviews[idx].date.slice(6, 7) : month = this.past_interviews[idx].date.slice(5, 7)
      const monthList = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
      month = monthList[parseInt(month) - 1]
      const date = this.past_interviews[idx].date.slice(8, 10)
      const year = this.past_interviews[idx].date.slice(0, 4)
      const amplifiedDate = month + ' ' + date + ',' + year
      const day = String(new Date(amplifiedDate))
      return day.slice(0, 3) + ',' + day.slice(3, 10) + ', ' + day.slice(11, 16)
    },
    fetch_interview () {
      this.$axios.get('/past-interview').then((response) => {
        this.past_interviews = response.data.past_interviews
      })
        .catch((errorResponse) => {
          this.$toast.error(
            errorResponse.response.data.message || 'Something went wrong'
          )
        })
    },
    viewReport (interviews) {
      this.hide_Report_details = true
      this.report = interviews
    }
  }
}
</script>

<style>
.full-height {
  min-height: 100vh
}
</style>
