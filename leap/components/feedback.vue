<template>
  <b-container>
    <b-row align-v="start" align-content="start" class="flex-grow-1">
      <b-col cols="12" class="mt-5">
        <b-breadcrumb class="bg-light pl-0">
          <b-breadcrumb-item>
            Dashboard
          </b-breadcrumb-item>
          <b-breadcrumb-item>
            Interview Request
          </b-breadcrumb-item>
          <b-breadcrumb-item active>
            Feedback
          </b-breadcrumb-item>
        </b-breadcrumb>
      </b-col>
      <b-col cols="12">
        <h4 class="font-weight-bold">
          Feedback
        </h4>
      </b-col>
      <b-col cols="12" class="mt-5">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row>
              <b-col cols="12" class="pt-5 pb-5 pl-4">
                <p class="text-left text-secondary">
                  Date &amp; time
                </p>
                <h4 class="text-left text-dark font-weight-bold border-bottom border-light">
                  {{ date() }}
                </h4>
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
        <p class="text-secondary mt-5 pt-3">
          Please evaluate the candidate in the following categories on the relevance and requirement of the position.
        </p>
        <p class="text-danger-dark">
          it should be completed immediately following the interview
        </p>
      </b-col>
      <b-col cols="12" class="mt-2">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row>
              <b-col cols="12" md="6" class="pt-5 pb-2 pl-4 border-bottom border-light">
                <p class="text-left text-secondary ml-2">
                  Technical Skill
                </p>
              </b-col>
              <b-col cols="12" md="6" class="pt-5 pb-2 pl-4 border-bottom border-light">
                <b-progress :value="technical_skill_progress_value" :max="max" show-progress animated />
              </b-col>
              <b-col cols="2" class="pt-3 pb-5">
                <b-form-radio v-model="technical_skill" class="font-weight-bold" value="Exceptional" size="md" @change="progressBar('Exceptional')">
                  Exceptional
                </b-form-radio>
              </b-col>
              <b-col cols="3 pt-3 pb-5">
                <b-form-radio v-model="technical_skill" class="font-weight-bold" value="Meets Requirenment" size="md" @change="progressBar('Meets Requirenment')">
                  Meets Requirenment
                </b-form-radio>
              </b-col>
              <b-col cols="3 pt-3 pb-5">
                <b-form-radio v-model="technical_skill" class="font-weight-bold" value="Need Training" size="md" @change="progressBar('Need Training')">
                  Need Training
                </b-form-radio>
              </b-col>
              <b-col cols="3 pt-3 pb-5">
                <b-form-radio v-model="technical_skill" class="font-weight-bold" value="Doesn't meet requirenment" size="md" @change="progressBar('Doesn\'t meet requirenment')">
                  Doesn't meet requirenment
                </b-form-radio>
              </b-col>
              <b-col v-if="technical_skill !== ''" cols="12" class="pl-4 ml-1 mb-4">
                <p class="text-left text-secondary">
                  Detail Feedback
                </p>
                <b-form-textarea
                  id="textarea"
                  v-model="technical_skill_text"
                />
                <b-button variant="primary" class="mt-5">
                  Save
                </b-button>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col cols="12" class="mt-2">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row>
              <b-col cols="12" md="6" class="pt-5 pb-2 pl-4 border-bottom border-light">
                <p class="text-left text-secondary ml-2">
                  Communication skills
                </p>
              </b-col>
              <b-col cols="12" md="6" class="pt-5 pb-2 pl-4 border-bottom border-light">
                <b-progress :value="communicational_skill_progress_value" :max="max" show-progress animated />
              </b-col>
              <b-col cols="2" class="pt-3 pb-5">
                <b-form-radio v-model="communicational_skill" class="font-weight-bold" value="Exceptional" size="md" @change="progressBar_two('Exceptional')">
                  Exceptional
                </b-form-radio>
              </b-col>
              <b-col cols="3 pt-3 pb-5">
                <b-form-radio v-model="communicational_skill" class="font-weight-bold" value="Meets Requirenment" size="md" @change="progressBar_two('Meets Requirenment')">
                  Meets Requirenment
                </b-form-radio>
              </b-col>
              <b-col cols="3 pt-3 pb-5">
                <b-form-radio v-model="communicational_skill" class="font-weight-bold" value="Need Training" size="md" @change="progressBar_two('Need Training')">
                  Need Training
                </b-form-radio>
              </b-col>
              <b-col cols="3 pt-3 pb-5">
                <b-form-radio v-model="communicational_skill" class="font-weight-bold" value="Doesn't meet requirenment" size="md" @change="progressBar_two('Doesn\'t meet requirenment')">
                  Doesn't meet requirenment
                </b-form-radio>
              </b-col>
              <b-col v-if="communicational_skill !== ''" cols="12" class="pl-4 ml-1 mb-4">
                <p class="text-left text-secondary">
                  Detail Feedback
                </p>
                <b-form-textarea
                  id="textarea"
                  v-model="communicational_skill_text"
                />
                <b-button variant="primary" class="mt-5">
                  Save
                </b-button>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col cols="12" class="mt-2">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row>
              <b-col cols="12" md="6" class="pt-5 pb-2 pl-4 border-bottom border-light">
                <p class="text-left text-secondary ml-2">
                  Presentation skills
                </p>
              </b-col>
              <b-col cols="12" md="6" class="pt-5 pb-2 pl-4 border-bottom border-light">
                <b-progress :value="presentation_skill_progress_value" :max="max" show-progress animated />
              </b-col>
              <b-col cols="2" class="pt-3 pb-5">
                <b-form-radio v-model="presentation_skill" class="font-weight-bold" value="Exceptional" size="md" @change="progressBar_three('Exceptional')">
                  Exceptional
                </b-form-radio>
              </b-col>
              <b-col cols="3 pt-3 pb-5">
                <b-form-radio v-model="presentation_skill" class="font-weight-bold" value="Meets Requirenment" size="md" @change="progressBar_three('Meets Requirenment')">
                  Meets Requirenment
                </b-form-radio>
              </b-col>
              <b-col cols="3 pt-3 pb-5">
                <b-form-radio v-model="presentation_skill" class="font-weight-bold" value="Need Training" size="md" @change="progressBar_three('Need Training')">
                  Need Training
                </b-form-radio>
              </b-col>
              <b-col cols="3 pt-3 pb-5">
                <b-form-radio v-model="presentation_skill" class="font-weight-bold" value="Doesn't meet requirenment" size="md" @change="progressBar_three('Doesn\'t meet requirenment')">
                  Doesn't meet requirenment
                </b-form-radio>
              </b-col>
              <b-col v-if="presentation_skill !== ''" cols="12" class="pl-4 ml-1 mb-4">
                <p class="text-left text-secondary">
                  Detail Feedback
                </p>
                <b-form-textarea
                  id="textarea"
                  v-model="presentation_skill_text"
                />
                <b-button variant="primary" class="mt-5">
                  Save
                </b-button>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col cols="12" class="mt-2">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row>
              <b-col cols="12" md="6" class="pt-5 pb-2 pl-4 border-bottom border-light">
                <p class="text-left text-secondary ml-2">
                  Understanding of Role
                </p>
              </b-col>
              <b-col cols="12" md="6" class="pt-5 pb-2 pl-4 border-bottom border-light">
                <b-progress :value="understanding_of_role_progress_value" :max="max" show-progress animated />
              </b-col>
              <b-col cols="2" class="pt-3 pb-5">
                <b-form-radio v-model="understanding_of_role" class="font-weight-bold" value="Exceptional" size="md" @change="progressBar_four('Exceptional')">
                  Exceptional
                </b-form-radio>
              </b-col>
              <b-col cols="3 pt-3 pb-5">
                <b-form-radio v-model="understanding_of_role" class="font-weight-bold" value="Meets Requirenment" size="md" @change="progressBar_four('Meets Requirenment')">
                  Meets Requirenment
                </b-form-radio>
              </b-col>
              <b-col cols="3 pt-3 pb-5">
                <b-form-radio v-model="understanding_of_role" class="font-weight-bold" value="Need Training" size="md" @change="progressBar_four('Need Training')">
                  Need Training
                </b-form-radio>
              </b-col>
              <b-col cols="3 pt-3 pb-5">
                <b-form-radio v-model="understanding_of_role" class="font-weight-bold" value="Doesn't meet requirenment" size="md" @change="progressBar_four('Doesn\'t meet requirenment')">
                  Doesn't meet requirenment
                </b-form-radio>
              </b-col>
              <b-col v-if="understanding_of_role !== ''" cols="12" class="pl-4 ml-1 mb-4">
                <p class="text-left text-secondary">
                  Detail Feedback
                </p>
                <b-form-textarea
                  id="textarea"
                  v-model="understanding_of_role_text"
                />
                <b-button variant="primary" class="mt-5">
                  Save
                </b-button>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col cols="12" class="mt-4 mb-5">
        <b-card no-body class="border-0">
          <b-container>
            <b-row>
              <b-col cols="7" class="mt-5 ml-5">
                <p class="text-left text-dark">
                  Overall Strengths and limitations as they related to this position
                </p>
                <p class="text-left text-secondary">
                  Thanks so much for attending your interview this morning. It
                  was great to meet you and I really appreciate the effort you made to attend the interview.
                </p>
              </b-col>
              <b-col cols="11" class="mt-2 ml-5">
                <b-form-textarea
                  id="textarea"
                  v-model="feedback.strength"
                  placeholder="Strength:"
                />
              </b-col>
              <b-col cols="11" class="mt-5 mb-5 ml-5">
                <b-form-textarea
                  id="textarea"
                  v-model="feedback.limitations"
                  placeholder="Limitations:"
                />
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col cols="12" class="mt-4 mb-5">
        <b-card no-body class="border-0">
          <b-container>
            <b-row>
              <b-col cols="11" class="mt-5 ml-5">
                <h4 class="text-left">
                  Should you consider this candidate for employment in this position ?
                </h4>
              </b-col>
              <b-col cols="1" class="mt-2 pb-5 ml-5">
                <b-form-radio v-model="feedback.consider_for_job" class="font-weight-bold" value="Yes" size="md">
                  Yes
                </b-form-radio>
              </b-col>
              <b-col cols="2" class="mt-2 pb-5 ml-5">
                <b-form-radio v-model="feedback.consider_for_job" class="font-weight-bold" value="No" size="md">
                  No
                </b-form-radio>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col cols="12">
        <div class="text-center mb-5 pb-5">
          <b-button variant="primary" class="mt-5" @click="submit">
            Save
          </b-button>
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>

export default {
  layout: 'app-page',
  props: {
    id: {
      type: Number,
      required: true
    },
    feedbacks: {
      type: Array,
      required: true
    }
  },
  data () {
    return {
      technical_skill: '',
      technical_skill_text: '',
      communicational_skill: '',
      communicational_skill_text: '',
      presentation_skill: '',
      presentation_skill_text: '',
      understanding_of_role: '',
      understanding_of_role_text: '',
      feedback: {
        strength: '',
        limitations: '',
        consider_for_job: ''
      },
      max: 100,
      technical_skill_progress_value: 0,
      presentation_skill_progress_value: 0,
      communicational_skill_progress_value: 0,
      understanding_of_role_progress_value: 0
    }
  },
  mounted () {
    this.$axios.get('endpoint')
      .then((response) => {
      })
  },
  methods: {
    date () {
      let month = ''
      this.feedbacks[this.id].date.slice(5, 7).includes('0') ? month = this.feedbacks[this.id].date.slice(6, 7) : month = this.feedbacks[this.id].date.slice(5, 7)
      const monthList = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
      month = monthList[parseInt(month) - 1]
      const date = this.feedbacks[this.id].date.slice(8, 10)
      const year = this.feedbacks[this.id].date.slice(0, 4)
      const amplifiedDate = month + ' ' + date + ',' + year
      const day = String(new Date(amplifiedDate))
      return day.slice(0, 3) + ',' + day.slice(3, 10) + ', ' + day.slice(11, 16)
    },
    progressBar (x) {
      if (x === 'Exceptional') {
        this.technical_skill_progress_value = 100
      } else if (x === 'Meets Requirenment') {
        this.technical_skill_progress_value = 75
      } else if (x === 'Need Training') {
        this.technical_skill_progress_value = 50
      } else if (x === 'Doesn\'t meet requirenment') {
        this.technical_skill_progress_value = 25
      }
    },
    progressBar_two (x) {
      if (x === 'Exceptional') {
        this.communicational_skill_progress_value = 100
      } else if (x === 'Meets Requirenment') {
        this.communicational_skill_progress_value = 75
      } else if (x === 'Need Training') {
        this.communicational_skill_progress_value = 50
      } else if (x === 'Doesn\'t meet requirenment') {
        this.communicational_skill_progress_value = 25
      }
    },
    progressBar_three (x) {
      if (x === 'Exceptional') {
        this.presentation_skill_progress_value = 100
      } else if (x === 'Meets Requirenment') {
        this.presentation_skill_progress_value = 75
      } else if (x === 'Need Training') {
        this.presentation_skill_progress_value = 50
      } else if (x === 'Doesn\'t meet requirenment') {
        this.presentation_skill_progress_value = 25
      }
    },
    progressBar_four (x) {
      if (x === 'Exceptional') {
        this.understanding_of_role_progress_value = 100
      } else if (x === 'Meets Requirenment') {
        this.understanding_of_role_progress_value = 75
      } else if (x === 'Need Training') {
        this.understanding_of_role_progress_value = 50
      } else if (x === 'Doesn\'t meet requirenment') {
        this.understanding_of_role_progress_value = 25
      }
    },
    submit () {
      const payload = { ...this.feedback }
      payload.technical_skill = [this.technical_skill, this.technical_skill_text]
      payload.communicational_skill = [this.communicational_skill, this.communicational_skill_text]
      payload.presentation_skill = [this.presentation_skill, this.presentation_skill_text]
      payload.understanding_of_role = [this.understanding_of_role, this.understanding_of_role_text]
      let endpoint
      if (this.feedback.custom_interview === true) {
        endpoint = `custom-interview/${this.feedback[this.id].slug}/feedback/`
      } else if (this.feedback.mock_interview === true) {
        endpoint = `mock-interview/${this.feedback[this.id].slug}/feedback/`
      }
      this.$axios.post(endpoint, payload)
        .then((response) => {
          this.$toast.success('Your feedback has been saved', {
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
            errorResponse.response.data.message || 'Could not save your feedback. Please try again later'
          )
        })
    }
  }
}
</script>
<style>
</style>
