<template>
  <b-container>
    <b-row class="mt-5">
      <b-col cols="12" md="3" class="pb-5 mb-5">
        <h3 class="font-weight-bold">
          Hello, {{ this.$store.state.auth.user.first_name }}
        </h3>
        <p v-if="$store.getters.is_interviewer" class="text-secondary">
          Below are your insights
        </p>
      </b-col>
      <b-col cols="12" md="9">
        <b-button @click="router.push('/create-interview')">
          Create an Interview
        </b-button>
      </b-col>
      <b-col v-if="$store.getters.is_interviewer" cols="12" md="6" class="pa-5">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row>
              <b-col :cols="this.$store.state.is_mock ? 3 : 4" class="pt-5 pb-5 pl-4">
                <b-img
                  src="@/static/interview_requests.svg"
                  alt="InterviewLeap logo"
                />
              </b-col>
              <b-col v-if="this.$store.state.is_mock" cols="3" class="pt-5 pb-5 pl-4">
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
      <b-col v-if="$store.getters.is_interviewer" cols="12" md="6" class="pa-5">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row>
              <b-col :cols="this.$store.state.is_mock ? 3 : 4" class="pt-5 pb-5 pl-4">
                <b-img
                  src="@/static/interview_taken.svg"
                  alt="InterviewLeap logo"
                />
              </b-col>
              <b-col v-if="this.$store.state.is_mock" cols="3" class="pt-5 pb-5 pl-4">
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
      <b-col v-if="$store.getters.is_interviewer" cols="12" md="6" class="pa-5">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row>
              <b-col :cols="this.$store.state.is_mock ? 3 : 4" class="pt-5 pb-5 pl-4">
                <b-img
                  src="@/static/interview_created.svg"
                  alt="InterviewLeap logo"
                />
              </b-col>
              <b-col v-if="this.$store.state.is_mock" cols="3" class="pt-5 pb-5 pl-4">
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
      <b-col v-if="$store.getters.is_interviewer" cols="12" md="6" class="pa-5">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row>
              <b-col :cols="this.$store.state.is_mock ? 3 : 4" class="pt-5 pb-5 pl-4">
                <b-img
                  src="@/static/earning.svg"
                  alt="InterviewLeap logo"
                />
              </b-col>
              <b-col v-if="this.$store.state.is_mock" cols="3" class="pt-5 pb-5 pl-4">
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
      <b-col v-if="$store.getters.is_interviewer" cols="12">
        <h4 class="text-left font-weight-bold">
          New Interview Requests
        </h4>
        <b-img
          v-if="interviewer_insights.interview_requests == null"
          src="@/static/blank_state_interviewer.svg"
          alt="InterviewLeap logo"
        />
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
        new_interview_requests: 1,
        interview_created: 1,
        interview_taken: 1,
        total_earnings: 1,
        interview_requests: {
          applied_designation: null,
          time_slots: [],
          date: 'datetime',
          candidate: 'FK'
        }
      }
    }
  }
}
</script>

<style>

</style>
