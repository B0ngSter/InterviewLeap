<template>
  <b-container>
    <b-row class="mt-5">
      <b-col v-if="$store.getters.is_interviewer" cols="12" md="8" class="mb-5">
        <h3 class="font-weight-bold">
          Hello, {{ this.$store.state.auth.user.first_name }}
        </h3>
        <p v-if="$store.getters.is_interviewer" class="text-secondary">
          Below are your insights
        </p>
      </b-col>
      <b-col v-if="$store.getters.is_interviewer" cols="12" md="4" class="text-right">
        <b-button to="/create-interview" variant="primary">
          Create an Interview
        </b-button>
      </b-col>
      <b-col v-if="$store.getters.is_interviewer" cols="12" md="6" class="mt-4">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row>
              <b-col cols="4" class="pt-4 pb-2 pl-4">
                <b-img
                  src="@/static/interview_requests.svg"
                  alt="InterviewLeap logo"
                />
              </b-col>
              <b-col cols="8" class="pt-5 pb-2 pl-4">
                <h4 class="text-left font-weight-bold">
                  {{ interviewer_insights.new_interview_requests }}
                </h4>
                <p class="text-left text-secondary">
                  New Interview Requests
                </p>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col v-if="$store.getters.is_interviewer" cols="12" md="6" class="mt-4">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row>
              <b-col cols="4" class="pt-4 pb-2 pl-4">
                <b-img
                  src="@/static/interview_taken.svg"
                  alt="InterviewLeap logo"
                />
              </b-col>
              <b-col cols="8" class="pt-5 pb-2 pl-4">
                <h4 class="text-left font-weight-bold">
                  {{ interviewer_insights.interview_taken }}
                </h4>
                <p class="text-left text-secondary">
                  Total Interviews Taken
                </p>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col v-if="$store.getters.is_interviewer" cols="12" md="6" class="mt-4">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row>
              <b-col cols="4" class="pt-4 pb-2 pl-4">
                <b-img
                  src="@/static/interview_created.svg"
                  alt="InterviewLeap logo"
                />
              </b-col>
              <b-col cols="8" class="pt-5 pb-2 pl-4">
                <h4 class="text-left font-weight-bold">
                  {{ interviewer_insights.interview_created }}
                </h4>
                <p class="text-left text-secondary">
                  Interviews Created by You
                </p>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col v-if="$store.getters.is_interviewer" cols="12" md="6" class="mt-4">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row>
              <b-col cols="4" class="pt-4 pb-2 pl-4">
                <b-img
                  src="@/static/earning.svg"
                  alt="InterviewLeap logo"
                />
              </b-col>
              <b-col cols="8" class="pt-5 pb-2 pl-4">
                <h4 class="text-left font-weight-bold">
                  {{ interviewer_insights.total_earnings }}
                </h4>
                <p class="text-left text-secondary">
                  Total Earnings
                </p>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col v-if="$store.getters.is_interviewer" cols="12" class="mt-5">
        <h4 class="text-left font-weight-bold">
          New Interview Requests
        </h4>
        <div v-if="interviewer_insights.interview_requests.length === 0" class="text-center pt-4">
          <b-img
            src="@/static/blank_state_interviewer.svg"
            alt="InterviewLeap logo"
          />
          <p class="font-weight-bold mt-5">
            No interview requests now.
          </p>
          <p class="text-secondary">
            No worries you can Create an Interview
          </p>
          <b-button to="/create-interview" variant="primary" class="mt-4 mb-4">
            Create an Interview
          </b-button>
        </div>
      </b-col>
      <b-col cols="12" class="mt-5 mb-5">
        <b-card v-for="(request, idx) in interviewer_insights.interview_requests" :key="idx" no-body class="text-center border-0 mt-5">
          <b-container class="bg-white">
            <b-row>
              <b-col cols="12" md="4" class="pt-5 pb-5 pl-4 border-bottom border-light">
                <p class="text-left text-secondary">
                  Date &amp; time
                </p>
                <h4 class="text-left text-dark font-weight-bold">
                  <!-- {{ date() }} -->
                </h4>
              </b-col>
              <b-col cols="3" offset-md="2" class="border-bottom border-light">
                <div class="mt-5 mb-5">
                  <b-button squared class="alert-danger text-danger-dark" @click="decline_interview_request">
                    Decline
                  </b-button>
                </div>
              </b-col>
              <b-col cols="3" class="border-bottom border-light">
                <div class="mt-5 mb-5">
                  <b-button squared class="alert-primary text-primary" @click="accept_interview_request">
                    Accept
                  </b-button>
                </div>
              </b-col>
              <b-col cols="5" class="pt-5 pb-5 pl-4">
                <p class="text-left text-danger-dark font-weight-bold">
                  Role - Front-end developer
                </p>
              </b-col>
              <b-col cols="4">
                <div class="pt-5 mb-5">
                  <p class="text-right font-weight-bold">
                    View Candidate Profile >
                  </p>
                </div>
              </b-col>
              <b-col cols="3">
                <div class="pt-5 mb-5">
                  <p class="text-right font-weight-bold">
                    Downloud Resume
                  </p>
                </div>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col v-if="$store.getters.is_candidate" cols="12">
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
      interviewer_insights: {
        // new_interview_requests: 1,
        // interview_created: 1,
        // interview_taken: 1,
        // total_earnings: 1,
        // interview_requests: [
        //   {
        //     applied_designation: null,
        //     time_slots: [],
        //     date: 'datetime',
        //     candidate: 'FK'
        //   },
        //   {
        //     applied_designation: null,
        //     time_slots: [],
        //     date: 'datetime',
        //     candidate: 'FK'
        //   }
        // ]
      }
    }
  },
  mounted () {
    this.$axios.get('/dashboard/')
      .then((response) => {
        this.interviewer_insights = response.data
      })
  },
  methods: {
    decline_interview_request () {},
    accept_interview_request () {}
  }
}
</script>

<style>

</style>
