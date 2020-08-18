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
                  <!-- {{ date() }} -->
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
        blah blah blah
      </b-col>
      <b-col cols="12" class="mt-5">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row>
              <b-col cols="12" md="6" class="pt-5 pb-2 pl-4 border-bottom border-light">
                <p class="text-left text-secondary">
                  Technical Skill
                </p>
              </b-col>
              <b-col cols="12" md="6" class="pt-5 pb-2 pl-4 border-bottom border-light">
                <b-progress :value="value" :max="max" show-progress animated />
              </b-col>
              <b-col cols="2" class="pt-3 pb-5">
                <b-form-radio v-model="feedback.technical_skill" class="font-weight-bold" value="Exceptional" size="md">
                  Exceptional
                </b-form-radio>
              </b-col>
              <b-col cols="3 pt-3 pb-5">
                <b-form-radio v-model="feedback.technical_skill" class="font-weight-bold" value="Meets Requirenment" size="md">
                  Meets Requirenment
                </b-form-radio>
              </b-col>
              <b-col cols="3 pt-3 pb-5">
                <b-form-radio v-model="feedback.technical_skill" class="font-weight-bold" value="Need Training" size="md">
                  Need Training
                </b-form-radio>
              </b-col>
              <b-col cols="3 pt-3 pb-5">
                <b-form-radio v-model="feedback.technical_skill" class="font-weight-bold" value="Doesn't meet requirenment" size="md">
                  Doesn't meet requirenment
                </b-form-radio>
              </b-col>
              <b-col v-if="feedback.technical_skill !== ''" cols="12">
                <p class="text-left text-secondary">
                  Detail Feedback
                </p>
                <b-form-textarea
                  id="textarea"
                  v-model="feedback.text"
                />
                <b-button variant="primary" class="mt-5">
                  Save
                </b-button>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>

export default {
  layout: 'app-page',
  data () {
    return {
      feedback: {
        technical_skill: '',
        communicational_skill: '',
        presentation_skill: '',
        understanding_of_role: '',
        text: '',
        strength: '',
        limitations: '',
        consider_for_job: ''
      },
      max: 100,
      value: 0
    }
  },
  methods: {
    // if (this.feedback.technical_skill === 'Exceptional') {
    //   return this.value = 100
    // } else if (this.feedback.technical_skill === 'Meets Requirenment') {
    //   return this.value = 75
    // } else if (this.feedback.technical_skill === 'Need Training') {
    //   return this.value = 50
    // } else if (this.feedback.technical_skill === 'Doesn\'t meet requirenment') {
    //   return this.value = 25
    // }
  }
}
</script>
<style>
</style>
