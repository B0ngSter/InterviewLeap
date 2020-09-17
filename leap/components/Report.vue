<template>
  <b-container>
    <b-row class="mt-5">
      <b-col cols="12">
        <b-breadcrumb class="bg-light pl-0">
          <b-breadcrumb-item to="/dashboard">
            Dashboard
          </b-breadcrumb-item>
          <b-breadcrumb-item v-if="!reporTypeInterviewer" to="/past-interview" @click="goBack">
            Past Interviews
          </b-breadcrumb-item>
          <b-breadcrumb-item v-if="!reporTypeInterviewer" active>
            Report
          </b-breadcrumb-item>
          <b-breadcrumb-item v-if="reporTypeInterviewer" active>
            Feedback
          </b-breadcrumb-item>
        </b-breadcrumb>
      </b-col>
      <b-col cols="12" md="3" class="mt-2 pt-2">
        <h3 v-if="!reporTypeInterviewer" class="font-weight-bold">
          Report
        </h3>
        <h3 v-if="reporTypeInterviewer" class="font-weight-bold">
          Feedback
        </h3>
      </b-col>
      <b-col v-if="!reporTypeInterviewer" offset-md="2" cols="12" md="3" class="mt-2 pt-2">
        <div class="text-left">
          <b-img
            class="cursor-pointer"
            src="@/static/down-arrow.svg"
            alt="Mock"
          />
          <span class="text-secondary pl-4 cursor-pointer" @click="downloud_report">Download report</span>
        </div>
      </b-col>
      <b-col v-if="!reporTypeInterviewer" cols="12" md="4" class="mt-2 pt-2">
        <div class="text-left">
          <b-img
            class="cursor-pointer"
            src="@/static/play-button-small.svg"
            alt="Mock"
          />
          <span class="text-secondary pl-4 cursor-pointer">Play Interview Recording</span>
        </div>
      </b-col>
      <b-col v-if="!reporTypeInterviewer" cols="12" class="mt-2">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row>
              <b-col class="pt-5 ml-5 pb-5 pl-2">
                <p class="text-left text-secondary">
                  Date. &amp; Time ({{ report.interview_type }})
                </p>
                <p class="text-left text-dark font-weight-bold">
                  {{ date() }}, {{ report.time_slot }}
                </p>
              </b-col>
              <b-col v-if="report.interview_type === 'Open Mock Interview'" class="pt-5 pb-5 pl-4">
                <p class="text-left text-secondary">
                  Interview from
                </p>
                <p class="text-left text-danger-dark font-weight-bold">
                  {{ report.company }}
                </p>
              </b-col>
              <b-col cols="3" offset-md="2" class="pr-5 mr-5 pt-5">
                <div class="text-right">
                  <b-img
                    class="cursor-pointer"
                    src="@/static/play-button.svg"
                    alt="Mock"
                  />
                </div>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <h4 v-if="!reporTypeInterviewer" class="ml-3 mt-4">
        Interviewer's evaluation on your performance
      </h4>
      <b-col cols="12" class="mt-3">
        <b-card no-body class="text-center border-0 font-weight-bold">
          <b-container class="bg-white">
            <b-row>
              <b-col cols="12" class="pt-5 pb-2 pl-4 border-bottom border-light">
                <p class="text-left text-secondary ml-2">
                  Technical Skill: {{ report.feedback.technical_skill[0] }}
                </p>
              </b-col>
              <b-col cols="6" class="pb-2 pl-4 border-bottom border-light">
                <b-progress :value="technical_skill_progress_value" :max="max" show-progress animated />
              </b-col>
              <b-col v-if="report.feedback.technical_skill.length > 1" cols="6" class="pb-2 pl-4 border-bottom border-light">
                <p class="font-weight-bold text-right">
                  View details >
                </p>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col cols="12" class="mt-3">
        <b-card no-body class="text-center border-0 font-weight-bold">
          <b-container class="bg-white">
            <b-row>
              <b-col cols="12" class="pt-5 pb-2 pl-4 border-bottom border-light">
                <p class="text-left text-secondary ml-2">
                  Communication skills: {{ report.feedback.communicational_skill[0] }}
                </p>
              </b-col>
              <b-col cols="6" class="pb-2 pl-4 border-bottom border-light">
                <b-progress :value="understanding_of_role_progress_value" :max="max" show-progress animated />
              </b-col>
              <b-col v-if="report.feedback.communicational_skill.length > 1" cols="6" class="pb-2 pl-4 border-bottom border-light">
                <p class="font-weight-bold text-right">
                  View details >
                </p>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col cols="12" class="mt-3">
        <b-card no-body class="text-center border-0 font-weight-bold">
          <b-container class="bg-white">
            <b-row>
              <b-col cols="12" class="pt-5 pb-2 pl-4 border-bottom border-light">
                <p class="text-left text-secondary ml-2">
                  Presentation skills: {{ report.feedback.presentation_skill[0] }}
                </p>
              </b-col>
              <b-col cols="6" class="pb-2 pl-4 border-bottom border-light">
                <b-progress :value="presentation_skill_progress_value" :max="max" show-progress animated />
              </b-col>
              <b-col v-if="report.feedback.presentation_skill.length > 1" cols="6" class="pb-2 pl-4 border-bottom border-light">
                <p class="font-weight-bold text-right">
                  View details >
                </p>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col cols="12" class="mt-3">
        <b-card no-body class="text-center border-0 font-weight-bold">
          <b-container class="bg-white">
            <b-row>
              <b-col cols="12" class="pt-5 pb-2 pl-4 border-bottom border-light">
                <p class="text-left text-secondary ml-2">
                  Understanding of Role: {{ report.feedback.understanding_of_role[0] }}
                </p>
              </b-col>
              <b-col cols="6" class="pb-2 pl-4 border-bottom border-light">
                <b-progress :value="understanding_of_role_progress_value" :max="max" show-progress animated />
              </b-col>
              <b-col v-if="report.feedback.understanding_of_role.length > 1" cols="6" class="pb-2 pl-4 border-bottom border-light">
                <p class="font-weight-bold text-right">
                  View details >
                </p>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col cols="12" class="mt-3">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row>
              <b-col v-if="!reporTypeInterviewer" cols="12" class="pt-5 pb-2 pl-4">
                <h3 class="text-left ml-2">
                  Your Overall Strengths and Limitations related to this position
                </h3>
                <p class="text-left text-secondary ml-2">
                  Thanks so much for attending your interview this morning. It was great to meet you and
                  I really appreciate the effort you made to attend the interview.
                </p>
              </b-col>
              <b-col cols="12" class="pl-4 pt-3">
                <p class="text-left font-weight-bold ml-2">
                  Strengths
                </p>
                <p class="text-left text-secondary ml-2">
                  {{ report.feedback.strength }}
                </p>
              </b-col>
              <b-col cols="12" class="pl-4 pt-3">
                <p class="text-left font-weight-bold ml-2">
                  Limitations
                </p>
                <p class="text-left text-secondary ml-2">
                  {{ report.feedback.limitations }}
                </p>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col v-if="report.feedback.consider_for_job !== ''" cols="12" class="mt-3 mb-5 pb-5">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row>
              <b-col cols="12" class="pt-5 pb-5 pl-4">
                <h3 v-if="!reporTypeInterviewer" class="text-left ml-2 text-primary">
                  Interviewer {{ job_offer() }} you suitable for this job.
                </h3>
                <h3 v-if="reporTypeInterviewer" class="text-left ml-2 text-primary">
                  Candidate {{ job_result() }} suitable for this job.
                </h3>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col cols="12">
        <div class="text-center text-secondary mt-5 mb-5">
          2020 Stellar Software Technologies Pvt ltd
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  layout: 'app-page',
  props: {
    report: {
      type: Object,
      required: true
    },
    reporTypeInterviewer: {
      type: Boolean,
      default: false
    }
  },
  data () {
    return {
      max: 100,
      technical_skill_progress_value: 0,
      presentation_skill_progress_value: 0,
      communicational_skill_progress_value: 0,
      understanding_of_role_progress_value: 0,
      report_pdf: null,
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
        //     consider_for_job: 'no'
        //   }
        // }
      ]
    }
  },
  mounted () {
    if (this.report.feedback.technical_skill[0] === 'Exceptional') {
      this.technical_skill_progress_value = 100
    } else if (this.report.feedback.technical_skill[0] === 'Meets Requirenment') {
      this.technical_skill_progress_value = 75
    } else if (this.report.feedback.technical_skill[0] === 'Need Training') {
      this.technical_skill_progress_value = 50
    } else if (this.report.feedback.technical_skill[0] === 'Doesn\'t meet requirenment') {
      this.technical_skill_progress_value = 25
    }
    if (this.report.feedback.communicational_skill[0] === 'Exceptional') {
      this.communicational_skill_progress_value = 100
    } else if (this.report.feedback.communicational_skill[0] === 'Meets Requirenment') {
      this.communicational_skill_progress_value = 75
    } else if (this.report.feedback.communicational_skill[0] === 'Need Training') {
      this.communicational_skill_progress_value = 50
    } else if (this.report.feedback.communicational_skill[0] === 'Doesn\'t meet requirenment') {
      this.communicational_skill_progress_value = 25
    }
    if (this.report.feedback.presentation_skill[0] === 'Exceptional') {
      this.presentation_skill_progress_value = 100
    } else if (this.report.feedback.presentation_skill[0] === 'Meets Requirenment') {
      this.presentation_skill_progress_value = 75
    } else if (this.report.feedback.presentation_skill[0] === 'Need Training') {
      this.presentation_skill_progress_value = 50
    } else if (this.report.feedback.presentation_skill[0] === 'Doesn\'t meet requirenment') {
      this.presentation_skill_progress_value = 25
    }
    if (this.report.feedback.understanding_of_role[0] === 'Exceptional') {
      this.understanding_of_role_progress_value = 100
    } else if (this.report.feedback.understanding_of_role[0] === 'Meets Requirenment') {
      this.understanding_of_role_progress_value = 75
    } else if (this.report.feedback.understanding_of_role[0] === 'Need Training') {
      this.understanding_of_role_progress_value = 50
    } else if (this.report.feedback.understanding_of_role[0] === 'Doesn\'t meet requirenment') {
      this.understanding_of_role_progress_value = 25
    }
  },
  methods: {
    date () {
      let month = ''
      this.report.date.slice(5, 7).includes('0') ? month = this.report.date.slice(6, 7) : month = this.report.date.slice(5, 7)
      const monthList = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
      month = monthList[parseInt(month) - 1]
      const date = this.report.date.slice(8, 10)
      const year = this.report.date.slice(0, 4)
      const amplifiedDate = month + ' ' + date + ',' + year
      const day = String(new Date(amplifiedDate))
      return day.slice(0, 3) + ',' + day.slice(3, 10) + ', ' + day.slice(11, 16)
    },
    job_offer () {
      if (this.report.feedback.consider_for_job === 'yes') {
        return 'considers'
      } else if (this.report.feedback.consider_for_job === 'no') {
        return 'does not consider'
      }
    },
    job_result () {
      if (this.report.feedback.consider_for_job === 'yes') {
        return 'was'
      } else if (this.report.feedback.consider_for_job === 'no') {
        return 'was not'
      }
    },
    downloud_report () {
      const payload = {}
      payload.slug = this.report.slug
      payload.pk = this.report.pk
      this.$axios.get(`/report-details/${this.report.pk}/${this.report.slug}/`).then((response) => {
        // this.report_pdf = response.data
      }).catch((errorResponse) => {
        this.$toast.error(
          errorResponse.response.data.message || 'Please try again later'
        )
      })
    },
    goBack () {
      this.$emit('Back', false)
    }
    // fetch_interview () {
    //   this.$axios.get('/past-interview').then((response) => {
    //     this.past_interviews = response.data.past_interviews
    //   })
    //     .catch((errorResponse) => {
    //       this.$toast.error(
    //         errorResponse.response.data.message || 'Something went wrong'
    //       )
    //     })
    // }
  }
}
</script>

<style>
</style>
