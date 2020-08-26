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
        <b-col cols="12" class="mt-5 mb-5">
          <b-card v-for="(request, idx) in interview_requests" :key="idx" no-body class="text-center border-0 mt-5">
            <b-container class="bg-white">
              <b-row>
                <b-col cols="12" md="" class="pt-5 pb-5 pl-4 border-bottom border-light">
                  <p class="text-left text-secondary">
                    Date &amp; time
                  </p>
                  <h4 class="text-left text-dark">
                    {{ date(idx) }}
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
                    }"
                    class="p-3 mt-5 ml-1 text-dark cursor-pointer"
                    @click="select_slot(idx, idy)"
                  >
                    {{ badge }}
                  </b-button>
                </b-col>
                <b-col v-if="!request.is_feedback && !interview_duration(idx)" cols="2" class="border-bottom border-light">
                  <b-button squared class="alert-danger text-danger-dark mt-5 mb-5" @click="decline_interview_slot(idx)">
                    Decline
                  </b-button>
                </b-col>
                <b-col v-if="!request.is_feedback && !interview_duration(idx)" cols="2" class="border-bottom border-light">
                  <b-button squared class="alert-primary text-primary mt-5 mb-5" @click="accpet_interview_slot(idx)">
                    Accept
                  </b-button>
                </b-col>
                <b-col v-if="request.is_feedback" cols="3" class="border-bottom border-light">
                  <b-button class="alert-primary text-primary mt-5 mb-5" @click="feedback(idx)">
                    Feedback
                  </b-button>
                </b-col>
                <b-col v-if="interview_duration(idx)" cols="3" offset-md="5" class="">
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
      :interview-requests="interview_requests"
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
      interview_requests: [
        {
          applied_designation: 'nm',
          candidate_email: 'nit35h.7@gmail.com',
          date: '2020-08-28',
          slug: null,
          time_slots: ['9PM - 12AM'],
          is_feedback: false,
          candidate: 'FK'
        },
        {
          applied_designation: 'nm',
          candidate_email: 'nit35h.7@gmail.com',
          date: '2020-08-28',
          slug: null,
          time_slots: ['9AM - 12PM'],
          is_feedback: true,
          candidate: 'FK'
        }
      ]
    }
  },
  mounted () {
    this.$axios.get('/auth/interview-requests/')
      .then((response) => {
        // this.interview_requests = response.data
      })
  },
  methods: {
    date (idx) {
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
    interview_duration (idx) {
      const oneSpan = 3 * 60 * 60 * 1000 // in milliseconds
      const dateString = this.interview_requests[idx].date
      const year = dateString.substring(0, 4)
      const month = dateString.substring(5, 7)
      const day = dateString.substring(8, 10)
      const interviewDay = new Date(year, month - 1, day).getTime()
      const starTime = interviewDay + 9 * 60 * 60 * 1000
      const timeSlots = ['9AM - 12PM', '12PM - 3PM', '3PM - 6PM', '6PM - 9PM', '9PM - 12AM']
      const interviewArray = [starTime, starTime + oneSpan, starTime + 2 * oneSpan, starTime + 3 * oneSpan, starTime + 4 * oneSpan]
      const interviewSlot = interviewArray[timeSlots.indexOf(this.interview_requests[idx].time_slots[0])]
      const timesNow = new Date().getTime()
      if (timesNow > interviewSlot && timesNow < interviewSlot + oneSpan) {
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
    feedback (idx) {
      this.id = idx
      this.showFeedbackPage = true
    }
  }
}
</script>

<style>
</style>
