<template>
  <div>
    <b-container v-if="!showProfile">
      <b-row class="mt-5">
        <b-col cols="12" md="3" class="mb-5">
          <h3 class="font-weight-bold">
            Hello, {{ this.$store.state.auth.user.first_name }}
          </h3>
          <p v-if="$store.getters.is_interviewer" class="text-secondary">
            Below are your insights
          </p>
          <p v-if="$store.getters.is_candidate" class="text-secondary">
            Your upcoming interviews
          </p>
        </b-col>
        <b-col v-if="$store.getters.is_candidate && upcoming_interviews.length === 0" cols="12" md="6" class="pb-5 mb-5">
          <div class="text-center">
            <b-img
              class="cursor-pointer"
              src="@/static/kio.svg"
              alt="Mock"
              height="308"
            />
            <p class="font-weight-bold">
              No upcoming interviews
            </p>
          </div>
        </b-col>
        <b-col v-if="$store.getters.is_candidate" :offset-md="upcoming_interviews.length === 0 ? 0 : 6" cols="12" md="3" class="pb-5 mb-5 text-center">
          <b-button class="text-white" variant="primary" to="/book-interview">
            Book interview
          </b-button>
        </b-col>
        <b-col v-if="$store.getters.is_interviewer" cols="12" md="4" offset-md="5" class="text-center">
          <b-button class="text-white" to="/create-interview" variant="primary">
            Create an Interview
          </b-button>
        </b-col>
        <div v-if="$store.getters.is_candidate" style="width: 100%;">
          <b-col v-for="(interviews, idx) in upcoming_interviews" :key="idx" cols="12" class="mt-4">
            <b-card no-body class="text-center border-0">
              <b-container class="bg-white">
                <b-row class="p-4 mt-3">
                  <b-col cols="12" :md="$store.state.is_mock ? 3 : 4">
                    <p class="text-left text-secondary">
                      Date
                    </p>
                    <p class="text-left text-dark font-weight-bold">
                      {{ date(idx, upcoming_interviews) }}
                    </p>
                  </b-col>
                  <b-col v-if="$store.state.is_mock" cols="12" md="3">
                    <p class="text-left text-secondary">
                      Interview from
                    </p>
                    <p class="text-left text-danger-dark font-weight-bold">
                      {{ interviews.job_title }}
                    </p>
                  </b-col>
                  <b-col cols="6" md="3" offset-md="2">
                    <div class="text-right">
                      <b-button squared class="alert-danger  text-danger-dark" @click="model=true">
                        Cancel
                      </b-button>
                    </div>
                  </b-col>
                  <b-col cols="6" md="3">
                    <div class="text-right">
                      <b-button squared class="alert-primary cancle-btn-padding text-primary" :to="`/book-interview/${upcoming_interviews[idx].slug}`">
                        Reschedule
                      </b-button>
                    </div>
                  </b-col>
                </b-row>
              </b-container>
            </b-card>
            <b-modal
              id="modal-center"
              v-model="model"
              centered
              hide-footer
              hide-header
            >
              <h4 class="pa-5 mt-5 text-secondary text-center">
                Cancellation of scheduled interview is non refundable
              </h4>
              <div class="text-center mt-5 mb-5">
                <b-button
                  squared
                  variant="outline-primary"
                  class="btn-padding text-primary ml-3"
                  @click="model=false"
                >
                  Close
                </b-button>
                <b-button squared variant="danger" class="text-white" @click="cancel (idx)">
                  Cancel Anyway
                </b-button>
              </div>
            </b-modal>
          </b-col>
        </div>
        <b-col v-if="$store.getters.is_interviewer" cols="12" md="6" class="mt-4 cursor-pointer">
          <nuxt-link to="/interview-request" style="text-decoration: none;">
            <b-card no-body class="text-center border-0">
              <b-container class="bg-white">
                <b-row>
                  <b-col cols="6" md="4" class="pt-4 pb-2 pl-4">
                    <b-img
                      src="@/static/interview_requests.svg"
                      alt="InterviewLeap logo"
                    />
                  </b-col>
                  <b-col cols="6" md="8" class="pt-5 pb-2 pl-4">
                    <h4 class="text-left text-dark font-weight-bold">
                      {{ interviewer_insights.new_interview_requests }}
                    </h4>
                    <p class="text-left text-secondary">
                      New Interview Requests
                    </p>
                  </b-col>
                </b-row>
              </b-container>
            </b-card>
          </nuxt-link>
        </b-col>
        <b-col v-if="$store.getters.is_interviewer" cols="12" md="6" class="mt-4">
          <nuxt-link to="/interview-request" style="text-decoration: none;">
            <b-card no-body class="text-center border-0">
              <b-container class="bg-white">
                <b-row>
                  <b-col cols="6" md="4" class="pt-4 pb-2 pl-4">
                    <b-img
                      src="@/static/interview_taken.svg"
                      alt="InterviewLeap logo"
                    />
                  </b-col>
                  <b-col cols="6" md="8" class="pt-5 pb-2 pl-4">
                    <h4 class="text-left text-dark font-weight-bold">
                      {{ interviewer_insights.interview_taken }}
                    </h4>
                    <p class="text-left text-secondary">
                      Total Interviews Conducted
                    </p>
                  </b-col>
                </b-row>
              </b-container>
            </b-card>
          </nuxt-link>
        </b-col>
        <b-col v-if="$store.getters.is_interviewer" cols="12" md="6" class="mt-4">
          <nuxt-link to="/created-interview" style="text-decoration: none;">
            <b-card no-body class="text-center border-0">
              <b-container class="bg-white">
                <b-row>
                  <b-col cols="6" md="4" class="pt-4 pb-2 pl-4">
                    <b-img
                      src="@/static/interview_created.svg"
                      alt="InterviewLeap logo"
                    />
                  </b-col>
                  <b-col cols="6" md="8" class="pt-5 pb-2 pl-4">
                    <h4 class="text-left text-dark font-weight-bold">
                      {{ interviewer_insights.interview_created }}
                    </h4>
                    <p class="text-left text-secondary">
                      Interviews Created by You
                    </p>
                  </b-col>
                </b-row>
              </b-container>
            </b-card>
          </nuxt-link>
        </b-col>
        <b-col v-if="$store.getters.is_interviewer" cols="12" md="6" class="mt-4">
          <nuxt-link to="/transaction" style="text-decoration: none;">
            <b-card no-body class="text-center border-0">
              <b-container class="bg-white">
                <b-row>
                  <b-col cols="6" md="4" class="pt-4 pb-2 pl-4">
                    <b-img
                      src="@/static/earning.svg"
                      alt="InterviewLeap logo"
                    />
                  </b-col>
                  <b-col cols="6" md="8" class="pt-5 pb-2 pl-4">
                    <h4 class="text-left text-dark font-weight-bold">
                      {{ interviewer_insights.total_earnings }}
                    </h4>
                    <p class="text-left text-secondary">
                      Total Earnings
                    </p>
                  </b-col>
                </b-row>
              </b-container>
            </b-card>
          </nuxt-link>
        </b-col>
        <b-col v-if="$store.getters.is_interviewer" cols="12" class="mt-5">
          <h4 class="text-left font-weight-bold">
            New Interview Requests
          </h4>
          <div v-if="interview_requests.length === 0" class="text-center pt-4">
            <b-img
              src="@/static/blank_state_interviewer.svg"
              alt="InterviewLeap logo"
            />
            <p class="font-weight-bold mt-5">
              No pending interview requests.
            </p>
            <p class="text-secondary">
              No worries you can Create an Interview
            </p>
            <b-button to="/create-interview" variant="primary" class="text-white mt-4 mb-4">
              Create an Interview
            </b-button>
          </div>
        </b-col>
        <b-col v-if="$store.getters.is_interviewer" cols="12" class="mt-5 mb-5">
          <b-card v-for="(request, idx) in interview_requests" :key="idx" no-body class="text-center border-0 mt-5">
            <b-container class="bg-white">
              <b-row class="p-4 mt-3">
                <b-col cols="12" md="2" class="pb-4">
                  <p class="text-left text-secondary">
                    Date &amp; time
                  </p>
                  <h4 class="text-left text-dark">
                    {{ date(idx, interview_requests) }}
                  </h4>
                </b-col>
                <b-col cols="12" md="5" class="pb-4 text-left">
                  <b-button
                    v-for="(badge, idy) in request.time_slots"
                    :key="idy"
                    pill
                    size="sm"
                    variant="outline-secondary"
                    :class="{
                      'bg-primary': badge === selected_slot[0] && idx === selected_slot[1],
                      'text-white': selected_slot[1] === idx && badge === selected_slot[0],
                      'text-dark': badge !== selected_slot[0] || selected_slot[1] !== idx,
                      'border-0': badge === selected_slot[0] && idx === selected_slot[1]
                    }"
                    class="p-3 cursor-pointer ml-2 mt-2"
                    @click="select_slot(idx, idy)"
                  >
                    {{ badge }}
                  </b-button>
                </b-col>
                <b-col cols="12" md="5" class="pb-4 text-right">
                  <b-button squared class="alert-danger text-danger-dark" @click="decline_interview_slot(idx)">
                    Decline
                  </b-button>
                  <b-button squared :disabled="selected_slot[1] !== idx" class="alert-primary text-primary ml-3" @click="accpet_interview_slot(idx)">
                    Accept
                  </b-button>
                </b-col>
                <b-col md="5" cols="12" class="border-top border-light pt-4">
                  <p class="text-left text-danger-dark font-weight-bold">
                    Role - Front-end developer
                  </p>
                </b-col>
                <b-col md="4" cols="12" class="border-top border-light pt-4">
                  <div class="">
                    <p class="text-right font-weight-bold cursor-pointer" @click="candidate_profile(request)">
                      View Candidate Profile >
                    </p>
                  </div>
                </b-col>
                <b-col md="3" cols="12" class="border-top border-light pt-4">
                  <div class="">
                    <p class="text-right font-weight-bold" @click="resume(request)">
                      Download Resume
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
        <b-col cols="12">
          <div class="text-center text-secondary mt-5 mb-5">
            2020 Stellar Software Technologies Pvt ltd
          </div>
        </b-col>
      </b-row>
    </b-container>
    <profile v-if="showProfile" :profile-response="profileResponse" />
  </div>
</template>
<script>
import mockInterviewListing from '~/components/mockInterviewListing'
import profile from '~/components/candidateProfile'
export default {
  layout: 'app-page',
  components: {
    profile,
    mockInterviewListing
  },
  data () {
    return {
      selected_slot: [],
      model: false,
      showProfile: false,
      profileResponse: {},
      interviewer_insights: {
        new_interview_requests: '',
        interview_created: '',
        interview_taken: '',
        total_earnings: ''
        // interview_requests: [
        //   {
        //     applied_designation: null,
        //     time_slots: [],
        //     date: '2020-08-21',
        //     candidate: 'FK'
        //   },
        //   {
        //     applied_designation: null,
        //     time_slots: [],
        //     date: '2020-08-21',
        //     candidate: 'FK'
        //   }
        // ]
      },
      interview_requests: [
        // {
        //   applied_designation: null,
        //   time_slots: ['9PM - 12AM', '12AM - 3AM'],
        //   date: '2020-08-21',
        //   candidate: 'FK'
        // },
        // {
        //   applied_designation: null,
        //   time_slots: [],
        //   date: '2020-08-21',
        //   candidate: 'FK'
        // }
      ],
      upcoming_interviews: [
        // {
        //   date: '2020-08-21',
        //   job_title: 'Byjus',
        //   slug: 'rvfw5lvb'
        // },
        // {
        //   date: '2020-08-21',
        //   job_title: 'Byjus',
        //   slug: 'ip3fjjmo'
        // }
      ]
    }
  },
  mounted () {
    this.$axios.get('/dashboard/')
      .then((response) => {
        this.interviewer_insights = response.data
      })
    if (this.$store.getters.is_interviewer) {
      this.$axios.get('/interview/interview-requests/')
        .then((response) => {
          this.interview_requests = response.data.interview_requests
        })
    }
    this.fetch_interview()
  },
  methods: {
    candidate_profile (obj, idx) {
      this.showProfile = true
      this.email = obj.candidate_email
      this.$axios.get(`/auth/candidate-profile?email=${this.email}`)
        .then((response) => {
          this.profileResponse = response.data
        })
    },
    date (idx, object) {
      let month = ''
      object[idx].date.slice(5, 7).includes('0') ? month = object[idx].date.slice(6, 7) : month = object[idx].date.slice(5, 7)
      const monthList = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
      month = monthList[parseInt(month) - 1]
      const date = object[idx].date.slice(8, 10)
      const year = object[idx].date.slice(0, 4)
      const amplifiedDate = month + ' ' + date + ',' + year
      const day = String(new Date(amplifiedDate))
      return day.slice(0, 3) + ',' + day.slice(3, 10)
    },
    select_slot (idx, idy) {
      const dummyarray = []
      dummyarray.includes(this.interview_requests[idx].time_slots[idy]) ? dummyarray.splice(dummyarray.indexOf(this.interview_requests[idx].time_slots[idy]), 1) : dummyarray.push(this.interview_requests[idx].time_slots[idy])
      if (dummyarray.length === 2) {
        dummyarray.splice(0, 1)
      }
      this.selected_slot = dummyarray
      this.selected_slot.push(idx)
    },
    decline_interview_slot (idx) {
      const payload = {}
      payload.action = 'decline'
      payload.candidate_email = this.interview_requests[idx].candidate_email
      payload.slug = this.interview_requests[idx].slug
      this.$axios.post('/interview/interview-requests/', payload).then((response) => {
        this.interview_requests.splice(idx, 1)
        this.$toast.success('Interview declined', {
          action: {
            text: 'Close',
            onClick: (e, toastObject) => {
              toastObject.goAway(0)
            }
          }
        })
      })
    },
    accpet_interview_slot (idx) {
      const ClassicalTimeSlots = ['09:00 - 12:00', '12:00 - 15:00', '15:00 - 18:00', '18:00 - 21:00', '21:00 - 00:00']
      const nomSlots = ['9AM - 12PM', '12PM - 3PM', '3PM - 6PM', '6PM - 9PM', '9PM - 12AM']
      const payload = {}
      payload.action = 'accept'
      payload.start_time = ClassicalTimeSlots[nomSlots.indexOf(this.selected_slot[0])].slice(0, 5)
      payload.end_time = ClassicalTimeSlots[nomSlots.indexOf(this.selected_slot[0])].slice(8, 13)
      payload.date = this.interview_requests[idx].date
      payload.candidate_email = this.interview_requests[idx].candidate_email
      payload.slug = this.interview_requests[idx].slug
      this.$axios.post('/interview/interview-requests/', payload).then((response) => {
        this.interview_requests.splice(idx, 1)
        this.$toast.success('Interview scheduled', {
          action: {
            text: 'Close',
            onClick: (e, toastObject) => {
              toastObject.goAway(0)
            }
          }
        })
      })
    },
    resume (interview) {
      window.open(interview.resume, '_blank')
    },
    interview_join_link (idx) {
      window.open(this.upcoming_interviews[idx].meet_link, '_blank')
    },
    cancel (idx) {
      const payload = {}
      payload.state = 'Cancelled'
      payload.slug = this.upcoming_interviews[idx].slug
      this.$axios.post('/interview-list/', payload).then((response) => {
        this.upcoming_interviews.splice(idx, 1)
        this.model = false
        this.$toast.success('Interview cancelled', {
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
    },
    fetch_interview () {
      if (this.$store.getters.is_candidate) {
        this.$axios.get('/interview-list/').then((response) => {
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
}
</script>
<style scoped>
.btn-padding {
  padding: 1.34rem 5rem 1.34rem 5rem;
}
.cancle-btn-padding {
  padding: 1.34rem 1.8rem 1.34rem 1.8rem;
}
</style>
