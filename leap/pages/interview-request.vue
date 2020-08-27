<template>
  <div>
    <b-container
      v-if="!showFeedbackPage"
      class="py-5"
    >
      <b-row align-v="start" align-content="start" class="flex-grow-1">
        <b-col cols="12">
          <b-breadcrumb class="bg-light pl-0">
            <b-breadcrumb-item>
              Dashboard
            </b-breadcrumb-item>
            <b-breadcrumb-item active>
              Interview Requests
            </b-breadcrumb-item>
          </b-breadcrumb>
        </b-col>
        <b-col cols="12" md="8" class="mb-5">
          <h3 class="font-weight-bold">
            New Interview Requests ({{ interview_requests.length }})
          </h3>
          <p class="text-secondary">
            Your upcoming interview requests
          </p>
        </b-col>
        <b-col cols="12" md="4" class="text-right">
          <b-button to="/create-interview" variant="primary">
            Past Interviews
          </b-button>
        </b-col>
        <b-col v-if="interview_requests.length > 0" cols="12" class="mt-2">
          <b-card v-for="(request, idx) in interview_requests" :key="idx" no-body class="text-center border-0 mt-5">
            <b-container class="bg-white">
              <b-row>
                <b-col cols="12" md="" class="pt-5 pb-5 pl-4 border-bottom border-light">
                  <p class="text-left text-secondary">
                    Date &amp; time
                  </p>
                  <h4 class="text-left text-dark">
                    {{ date_Interview_request(idx) }}
                  </h4>
                </b-col>
                <b-col cols="12" md="6" class="mt-3">
                  <b-button
                    v-for="(badge, idy) in request.time_slots"
                    :key="idy"
                    pill
                    size="sm"
                    variant="outline-secondary"
                    :class="{
                      'bg-primary': badge === selected_slot[0],
                      'text-white': badge === selected_slot[0] ? true : false,
                      'text-dark': badge === selected_slot[0] ? false: true
                    }"
                    class="p-3 mt-5 ml-1 cursor-pointer"
                    @click="select_slot(idx, idy)"
                  >
                    {{ badge }}
                  </b-button>
                </b-col>
                <b-col cols="2" class="border-bottom border-light">
                  <b-button squared class="alert-danger text-danger-dark mt-5 mb-5" @click="decline_interview_slot(idx)">
                    Decline
                  </b-button>
                </b-col>
                <b-col cols="2" class="border-bottom border-light">
                  <b-button squared class="alert-primary text-primary mt-5 mb-5" @click="accpet_interview_slot(idx)">
                    Accept
                  </b-button>
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
        <b-col v-if="feedback.length > 0" cols="12" class="mt-2">
          <b-card v-for="(request, idx) in feedback" :key="idx" no-body class="text-center border-0">
            <b-container class="bg-white">
              <b-row>
                <b-col cols="12" md="4" class="pt-5 pb-5 pl-4 border-bottom border-light">
                  <p class="text-left text-secondary">
                    Date &amp; time
                  </p>
                  <h4 class="text-left text-dark">
                    {{ date_feedback(idx) }}
                  </h4>
                </b-col>
                <b-col cols="3" md="3" offset-md="5" class="border-bottom border-light">
                  <b-button class="alert-primary text-primary mt-5 mb-5" @click="feedbacks(idx)">
                    Feedback
                  </b-button>
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
        <b-col v-if="upcoming_interviews.length > 0" cols="12" class="mt-2">
          <b-card v-for="(request, idx) in upcoming_interviews" :key="idx" no-body class="text-center border-0">
            <b-container class="bg-white">
              <b-row>
                <b-col cols="12" md="" class="pt-5 pb-5 pl-4 border-bottom border-light">
                  <p class="text-left text-secondary">
                    Date &amp; time
                  </p>
                  <h4 class="text-left text-dark">
                    {{ date_upcomming(idx) }}
                  </h4>
                </b-col>
                <b-col :disabled="!interview_duration(idx)" cols="3" offset-md="5" class="">
                  <b-button squared class="alert-primary text-primary mt-5 mb-5">
                    Join
                  </b-button>
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
        <b-col cols="12" class="mt-5">
          <h3>Past Completed Interviews ({{ sum_of_interviews() }})</h3>
        </b-col>
        <b-col v-for="(months, idx) in Object.keys(past_interviews)" :key="idx" cols="12" class="mt-5">
          <h4>{{ months }} ({{ past_interviews[months].length }})</h4>
          <b-card v-for="(interview, idy) in past_interviews[Object.keys(past_interviews)[idx]]" :key="idy" no-body class="text-center border-0 mt-5">
            <b-container class="bg-white">
              <b-row>
                <b-col cols="12" md="4" class="pt-5 pb-5 pl-4 border-bottom border-light">
                  <p class="text-left text-secondary">
                    Date &amp; times
                  </p>
                  <h4 class="text-left text-dark">
                    {{ date_past(idx, idy) }}
                  </h4>
                </b-col>
                <b-col cols="3" offset-md="5" class="">
                  <b-button squared class="alert-primary text-primary mt-5 mb-5">
                    View Feedback
                  </b-button>
                </b-col>
                <b-col cols="5" class="pt-5 pb-5 pl-4">
                  <p class="text-left text-danger-dark font-weight-bold">
                    Role - {{ interview.role }}
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
        <b-col cols="12">
          <div class="text-center text-secondary mt-5">
            2020 Stellar Software Technologies Pvt ltd
          </div>
        </b-col>
      </b-row>
    </b-container>
    <feedback
      v-if="showFeedbackPage"
      :id="id"
      :feedbacks="feedback"
    />
  </div>
</template>

<script>
import feedback from '~/components/feedback'
export default {
  layout: 'app-page',
  components: {
    feedback
  },
  data () {
    return {
      selected_slot: [],
      id: null,
      showFeedbackPage: false,
      past_interviews: {
        August: [{
          interview_start_time: '2020-08-10T13:00:00Z',
          interview_end_time: '2020-08-10T14:00:00Z',
          candidate_email: 'madhu@candidate.com',
          role: 'Django Developer'
        }],
        July: [{
          interview_start_time: '2020-07-27T09:06:02Z',
          interview_end_time: '2020-07-27T09:06:09Z',
          candidate_email: 'madhu@candidate.com',
          role: 'Past Interveiw Developer'
        }],
        June: [{
          interview_start_time: '2020-06-27T09:09:01Z',
          interview_end_time: '2020-06-27T09:09:06Z',
          candidate_email: 'madhu@candidate.com',
          role: 'Past Interveiw Developer'
        }, {
          interview_start_time: '2020-06-26T09:09:37Z',
          interview_end_time: '2020-06-26T09:09:52Z',
          candidate_email: 'madhu@candidate.com',
          role: 'Past Interveiw Developer'
        }],
        May: [{
          interview_start_time: '2020-05-24T09:10:10Z',
          interview_end_time: '2020-05-24T09:10:14Z',
          candidate_email: 'madhu@candidate.com',
          role: 'Past Interveiw Developer'
        }]
      },
      interview_requests: [{
        slug: 'tqt0b4lt',
        applied_designation: 'python developer',
        date: '2020-08-28',
        time_slots: ['9AM - 12PM', '12PM - 3PM', '3PM - 6PM'],
        candidate_email: 'madhu@candidate.com',
        is_feedback: false
      }],
      feedback: [{
        slug: 'mock-python-developer-13',
        applied_designation: 'Mock Python Developer',
        date: '2020-08-26',
        interview_start_time: '10:00:00',
        interview_end_time: '11:00:00',
        candidate_email: 'madhu@candidate.com',
        custom_interview: true
      }],
      upcoming_interviews: [{
        slug: 'tqt0b4lt',
        applied_designation: 'python developer',
        date: '2020-08-28',
        interview_start_time: '2020-08-28T00:00:00Z',
        interview_end_time: '2020-08-28T02:00:00Z',
        candidate_email: 'madhu@candidate.com',
        mock_interview: true
      }]
    }
  },
  mounted () {
    this.$axios.get('/auth/interview-requests/')
      .then((response) => {
        // this.interview_requests = response.data.interview_requests
        // this.feedback = response.data.feedback
        // this.past_interviews = response.data.past_interviews
        // this.upcoming_interviews = response.data.upcoming_interviews
      })
  },
  methods: {
    date_Interview_request (idx) {
      let month = ''
      this.interview_requests[idx].date.slice(5, 7).includes('0') ? month = this.interview_requests[idx].date.slice(6, 7) : month = this.interview_requests[idx].date.slice(5, 7)
      const monthList = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
      month = monthList[parseInt(month) - 1]
      const date = this.interview_requests[idx].date.slice(8, 10)
      const year = this.interview_requests[idx].date.slice(0, 4)
      const amplifiedDate = month + ' ' + date + ',' + year
      const day = String(new Date(amplifiedDate))
      return day.slice(0, 3) + ',' + day.slice(3, 10)
    },
    date_feedback (idx) {
      let month = ''
      this.feedback[idx].date.slice(5, 7).includes('0') ? month = this.feedback[idx].date.slice(6, 7) : month = this.feedback[idx].date.slice(5, 7)
      const monthList = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
      month = monthList[parseInt(month) - 1]
      const date = this.feedback[idx].date.slice(8, 10)
      const year = this.feedback[idx].date.slice(0, 4)
      const amplifiedDate = month + ' ' + date + ',' + year
      const day = String(new Date(amplifiedDate))
      return day.slice(0, 3) + ',' + day.slice(3, 10)
    },
    date_upcomming (idx) {
      let month = ''
      this.upcoming_interviews[idx].date.slice(5, 7).includes('0') ? month = this.upcoming_interviews[idx].date.slice(6, 7) : month = this.upcoming_interviews[idx].date.slice(5, 7)
      const monthList = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
      month = monthList[parseInt(month) - 1]
      const date = this.upcoming_interviews[idx].date.slice(8, 10)
      const year = this.upcoming_interviews[idx].date.slice(0, 4)
      const amplifiedDate = month + ' ' + date + ',' + year
      const day = String(new Date(amplifiedDate))
      return day.slice(0, 3) + ',' + day.slice(3, 10)
    },
    date_past (idx, idy) {
      let month = ''
      this.past_interviews[Object.keys(this.past_interviews)[idx]][idy].interview_end_time.slice(5, 7).includes('0') ? month = this.past_interviews[Object.keys(this.past_interviews)[idx]][idy].interview_end_time.slice(6, 7) : month = this.past_interviews[Object.keys(this.past_interviews)[idx]][idy].interview_end_time.slice(5, 7)
      const monthList = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
      month = monthList[parseInt(month) - 1]
      const date = this.past_interviews[Object.keys(this.past_interviews)[idx]][idy].interview_end_time.slice(8, 10)
      const year = this.past_interviews[Object.keys(this.past_interviews)[idx]][idy].interview_end_time.slice(0, 4)
      const amplifiedDate = month + ' ' + date + ',' + year
      const day = String(new Date(amplifiedDate))
      return day.slice(0, 3) + ',' + day.slice(3, 10) + ', ' + day.slice(11, 16)
    },
    interview_duration (idx) {
      // const oneSpan = 3 * 60 * 60 * 1000 // in milliseconds
      const dateString = this.upcoming_interviews[idx].date
      const year = dateString.substring(0, 4)
      const month = dateString.substring(5, 7)
      const day = dateString.substring(8, 10)
      const interviewDay = new Date(year, month - 1, day).getTime()
      const starTime = interviewDay + this.upcoming_interviews[idx].interview_start_time.substring(11, 13) * 60 * 60 * 1000
      const EndTime = interviewDay + this.upcoming_interviews[idx].interview_end_time.substring(11, 13) * 60 * 60 * 1000
      // const timeSlots = ['9AM - 12PM', '12PM - 3PM', '3PM - 6PM', '6PM - 9PM', '9PM - 12AM']
      // const interviewArray = [starTime, starTime + oneSpan, starTime + 2 * oneSpan, starTime + 3 * oneSpan, starTime + 4 * oneSpan]
      // const interviewSlot = interviewArray[timeSlots.indexOf(this.upcoming_interviews[idx].time_slots[0])]
      const timesNow = new Date().getTime()
      if (timesNow > starTime && timesNow < EndTime) {
        return true
      } else {
        return false
      }
    },
    select_slot (idx, idy) {
      this.selected_slot.includes(this.interview_requests[idx].time_slots[idy]) ? this.selected_slot.splice(this.selected_slot.indexOf(this.interview_requests[idx].time_slots[idy]), 1) : this.selected_slot.push(this.interview_requests[idx].time_slots[idy])
      if (this.selected_slot.length === 2) {
        this.selected_slot.splice(0, 1)
      }
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
      this.$axios.post('/auth/interview-requests/', payload).then((response) => {})
    },
    decline_interview_slot (idx) {
      this.interview_requests.splice(idx, 1)
    },
    feedbacks (idx) {
      this.id = idx
      this.showFeedbackPage = true
    },
    sum_of_interviews () {
      let sum = 0
      Object.keys(this.past_interviews).map((key) => {
        sum += this.past_interviews[key].length
      })
      return sum
    }
  }
}
</script>

<style>
</style>
