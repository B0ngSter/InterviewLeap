<template>
  <div>
    <b-container class="py-5">
      <b-row align-v="start" align-content="start" class="flex-grow-1">
        <b-col cols="12">
          <b-breadcrumb class="bg-light pl-0">
            <b-breadcrumb-item to="/dashboard">
              Dashboard
            </b-breadcrumb-item>
            <b-breadcrumb-item active>
              Create Interview
            </b-breadcrumb-item>
          </b-breadcrumb>
        </b-col>
        <b-col cols="12">
          <h2 class="mt-5">
            Hello, {{ this.$store.state.auth.user.first_name }}
          </h2>
          <p class="text-secondary">
            Your upcoming interview requests
          </p>
        </b-col>
        <b-col cols="12" class="mt-5">
          <b-card no-body class="text-center border-0">
            <b-container class="bg-white">
              <b-row>
                <b-col cols="12" md="6" class="pt-5 pb-5">
                  <b-form-group>
                    <b-form-input
                      v-model="$v.interviewInfo.job_title.$model"
                      class="mb-2 mb-sm-0 mr-md-4 ml-md-3"
                      name="example-input-1"
                      placeholder="Job Title"
                      :state="validateState('job_title')"
                      aria-describedby="input-1-live-feedback"
                    />
                    <b-form-invalid-feedback
                      id="input-1-live-feedback"
                    >
                      This is a required field.
                    </b-form-invalid-feedback>
                  </b-form-group>
                </b-col>
                <b-col cols="12" md="6" class="pt-5 pb-5 pr-5">
                  <b-form-group>
                    <b-form-input
                      v-model="$v.interviewInfo.exp_years.$model"
                      min="0"
                      class="mb-2 mb-sm-0 mr-md-4 ml-md-3"
                      placeholder="Experience Required (Optional)"
                      :state="validateState('exp_years')"
                      aria-describedby="input-1-live-feedback"
                    />
                    <b-form-invalid-feedback
                      id="input-1-live-feedback"
                    >
                      This is a required field.
                    </b-form-invalid-feedback>
                  </b-form-group>
                </b-col>
              </b-row>
            </b-container>
          </b-card>
        </b-col>
        <b-col cols="12" class="mt-2">
          <b-card no-body class="text-center border-0">
            <b-container class="bg-white">
              <b-row align-v="center" align-content="start">
                <b-col cols="12" md="12" class="p-4">
                  <b-input-group>
                    <b-form-input
                      v-model="skill_search_query"
                      placeholder="Core Skills"
                      list="Skill-options"
                      :disabled="skills_filled"
                      @keypress="fetchSkills"
                      @keydown.enter="addSkill"
                    />
                    <datalist id="Skill-options">
                      <option v-for="(Skill, idp) in fetchedSkill" :key="idp">
                        {{ Skill }}
                      </option>
                    </datalist>
                    <b-button variant="primary" :disabled="skills_filled" @click="addSkill">
                      Add
                    </b-button>
                  </b-input-group>
                  <p class="mt-2 text-muted font-weight-normal">
                    {{ interviewInfo.skills.length }}/5 skills selected
                  </p>
                  <h4>
                    <b-badge
                      v-for="(skill, id_s) in interviewInfo.skills"
                      :key="id_s"
                      size="lg"
                      variant="light"
                      class="mb-2 mr-2 border"
                      pill
                    >
                      <span class="d-flex align-items-center">
                        <span class="mr-2">{{ skill }}</span>
                        <b-icon-x
                          class="cursor-pointer"
                          @click="removeTag(id_s)"
                        />
                      </span>
                    </b-badge>
                  </h4>
                </b-col>
              </b-row>
            </b-container>
          </b-card>
        </b-col>
        <b-col cols="12" class="mt-2">
          <b-card no-body class="text-center border-0">
            <b-container class="bg-white">
              <b-row>
                <b-col cols="12" md="6" class="pt-5 pb-5 pl-4">
                  <b-form-group>
                    <b-form-input
                      v-model="$v.interviewInfo.description.$model"
                      class="bg-white"
                      required
                      placeholder="Brief description"
                      :state="validateState('description')"
                      aria-describedby="input-1-live-feedback"
                    />
                    <b-form-invalid-feedback
                      id="input-1-live-feedback"
                    >
                      This is a required field.
                    </b-form-invalid-feedback>
                  </b-form-group>
                </b-col>
                <b-col cols="12" md="6" class="pt-5 pb-5 pr-5">
                  <b-form-group>
                    <b-input
                      id="timeZones"
                      v-model="$v.interviewInfo.timezone.$model"
                      required
                      list="timeZones-options"
                      class="mb-2 mb-sm-0 ml-md-4 mr-md-3"
                      :state="validateState('timezone')"
                      placeholder="Time Zone"
                      autocomplete="off"
                    />
                    <datalist id="timeZones-options">
                      <option v-for="(timeZones, idx) in timeZone" :key="idx">
                        {{ timeZones }}
                      </option>
                    </datalist>
                    <b-form-invalid-feedback
                      id="input-1-live-feedback"
                    >
                      This is a required field.
                    </b-form-invalid-feedback>
                  </b-form-group>
                </b-col>
              </b-row>
            </b-container>
          </b-card>
        </b-col>
        <b-col cols="12" class="mt-5">
          <h4>Set Availability</h4>
        </b-col>
        <b-col cols="3" offset-md="5">
          <h4 class="pl-3">
            <b-badge pill class="pt-3 pb-3 pl-5 pr-5 alert-primary">
              {{ month() }}
            </b-badge>
          </h4>
        </b-col>
        <b-col cols="12" />
        <b-col
          v-for="(timeslots, date, idx) in date_row"
          :key="idx"
          :class="{'selected': date === selected_date}"
          class="mt-5 ml-5"
        >
          <b-badge
            pill
            :class="{
              'bg-primary': date === selected_date,
              'text-dark': date !== selected_date,
              'bg-white': date !== selected_date
            }"
            class="p-4 cursor-pointer"
            @click="select_date(date)"
          >
            {{ dayZ(idx) }}
          </b-badge>
          <h4
            class="p-4"
            :class="{
              'text-dark': date !== selected_date,
              'text-primary': date == selected_date
            }"
          >
            {{ currentDate(idx) }}
          </h4>
        </b-col>
      </b-row>
    </b-container>
    <b-container>
      <b-row cols="5">
        <b-col
          v-for="(timeslot, idy) in time_slots"
          :key="idy"
        >
          <b-card
            v-if="selected_date"
            no-body
            class="p-3 pl-5 mt-3 border-0 cursor-pointer"
            :class="{
              'alert-primary': date_row[selected_date].includes(time_slots_to_be_sent[idy])
            }"
            @click="toggle_timeslot(idy)"
          >
            {{ timeslot }}
          </b-card>
        </b-col>
        <b-col cols="12">
          <div class="text-center mt-5 mb-5">
            <b-button
              variant="primary"
              :disabled="interviewInfo.job_title === null || interviewInfo.skills.length === 0 || interviewInfo.exp_years == null || interviewInfo.timezone == null || interviewInfo.description == null"
              @click="submit"
            >
              Create Interview
            </b-button>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import Vue from 'vue'
import { validationMixin } from 'vuelidate'
import { required } from 'vuelidate/lib/validators'
export default {
  layout: 'app-page',
  mixins: [validationMixin],
  data () {
    return {
      time_slots: ['9AM - 12PM', '12PM - 3PM', '3PM - 6PM', '6PM - 9PM', '9PM - 12AM'],
      time_slots_to_be_sent: ['09:00 - 12:00', '12:00 - 15:00', '15:00 - 18:00', '18:00 - 21:00', '21:00 - 00:00'], // time slotes requested for backend are in this form
      selected_date: null,
      date_row: {},
      job_exp: '',
      interviewInfo: {
        skills: [],
        job_title: null,
        exp_years: null,
        description: null,
        timezone: null,
        slug: null
      },
      timeZone: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15].map(num => `static ${num}`),
      fetchedSkill: [],
      skill_search_query: ''
    }
  },
  computed: {
    skills_filled () {
      return this.interviewInfo.skills.length >= 5
    }
  },
  mounted () {
    this.fetch_timeZone()
    this.generate_dates()
    // this.updateInterview()
    // this.fetch_timeSlots()
  },
  validations: {
    interviewInfo: {
      job_title: { required },
      exp_years: { required },
      description: { required },
      timezone: { required }
    }
  },
  methods: {
    validateState (name) {
      const { $dirty, $error } = this.$v.interviewInfo[name]
      return $dirty ? !$error : null
    },
    // fetch_timeSlots () {
    //   this.$axios.get('/time-slot')
    //     .then((response) => {
    //       this.time_slots = response.data.time_slot
    //     })
    // },
    // updateInterview () {
    //   this.$axios.get('/auth/create-interview/')
    //     .then((response) => {
    //       if (response.data.includes('pk')) {
    //         this.interviewInfo = this.response.data
    //       }
    //     })
    //     .catch((errorResponse) => {
    //       this.$toast.error(
    //         errorResponse.response.data.message || 'Something went wrong'
    //       )
    //     })
    // },
    fetch_timeZone () {
      this.$axios.get('/book-interview')
        .then((response) => {
          this.timeZone = response.data.timezone_list
        })
        .catch((errorResponse) => {
          this.$toast.error(
            errorResponse.response.data.message || 'Something went wrong'
          )
        })
    },
    month () {
      const today = new Date()
      const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
      return months[today.getMonth()]
    },
    dayZ (value) {
      const today = new Date()
      const dayss = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
      return dayss[today.getDay() + value]
    },
    currentDate (val) {
      const today = new Date().getTime()
      const oneDay = 24 * 60 * 60 * 1000 // in milliseconds
      const dates = today + (oneDay * val)
      return new Date(dates).toString().slice(8, 10)
    },
    toggle_timeslot (idy) {
      const timeslotIdx = this.date_row[this.selected_date].indexOf(this.time_slots_to_be_sent[idy]) // to toggle the class of time blocks
      if (timeslotIdx > -1) {
        this.date_row[this.selected_date].splice(timeslotIdx, 1)
      } else {
        this.date_row[this.selected_date].push(this.time_slots_to_be_sent[idy])
      }
    },
    select_date (date) {
      this.selected_date = date
    },
    generate_dates () {
      const today = new Date().getTime()
      const oneDay = 24 * 60 * 60 * 1000 // in milliseconds
      const dates = [0, 1, 2, 3, 4, 5, 6].map((int) => {
        return today + (oneDay * int)
      })
      let month = new Date().getMonth() + 1
      if (month < 10) {
        month = '0' + month
      }
      for (let i = 0; i < dates.length; i++) {
        const date = dates[i]
        const thismonth = new Date(dates[i]).toString().slice(4, 7)
        const MonthOfFirstDay = new Date(dates[0]).toString().slice(4, 7)
        if (thismonth !== MonthOfFirstDay) { // in case if date is like 30 or 31 so month count will be increase by 1
          month = parseInt(month) + 1
          if (month < 10) {
            month = '0' + month
          }
        }
        const todaydate = new Date(date).toString().slice(8, 10)
        const year = new Date(date).toString().slice(11, 15)
        Vue.set(this.date_row, month + '-' + todaydate + '-' + year, []) // date is requested in MM-DD-YYYY
      }
    },
    submit () {
      let payload = {}
      payload = { ...this.interviewInfo }
      payload.skills = payload.skills.toString()
      payload.interview_time = { ...this.date_row }
      Object.keys(payload.interview_time).map((key) => {
        if (payload.interview_time[key].length === 0) {
          delete payload.interview_time[key] // remove date keys which are empty
        }
      })
      this.$axios.post('/interview/create-interview/', payload)
        .then((response) => {
          this.$toast.success('Your profile changes were saved', {
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
            errorResponse.response.data.message || 'Interview has been created. Please try again later'
          )
        })
    },
    removeTag (skillIndex) {
      this.interviewInfo.skills.splice(skillIndex, 1)
    },
    addSkill () {
      if (this.skill_search_query.length === 0) {
      } else if (!this.interviewInfo.skills.includes(this.skill_search_query)) {
        this.interviewInfo.skills.push(this.skill_search_query)
      }
      this.skill_search_query = ''
    },
    fetchSkills () {
      this.$axios.get(`/skill-search?search=${this.skill_search_query}`)
        .then((response) => {
          if (response.status === 200) {
            this.fetchedSkill = response.data.result
          }
        })
    } // do not remove below code for time being
    // important learning can be extracted from code below
    // about data not being saved inside json
    // badge_active (idy) {
    //   const today = new Date()
    //   const date = parseInt(('0' + today.getDate()).slice(-2)) + idy
    //   const month = ('0' + (today.getMonth() + 1)).slice(-2)
    //   const year = today.getFullYear()
    //   const formatedDate = year + '-' + month + '-' + date
    //   this.date_array.push(formatedDate)
    //   this.date_array.forEach((element) => {
    //     this.payload_json[element] = []
    //   })
    //   this.time_array.push([...this.active_timeStamp, -1, idy])
    //   // if (idy === this.idy_arr[this.idy_arr.length - 1]) {
    //   //   this.active_timeStamp = this.time_array[this.time_array.length - 1]
    //   // }
    //   this.time_array.forEach((element) => {
    //     if (element.length > 2) {
    //       if (idy === element[element.length - 1]) {
    //         const new2 = element.slice(0, -2)
    //         this.active_timeStamp = new2
    //       }
    //     }
    //   })
    //   this.time_array.push([...this.interviewTimes])
    //   this.active_dateStamp = idy
    //   this.active_timeStamp = []
    //   this.interviewTimes = []
    // },
    // time_stamp (idx) {
    //   this.active_timeStamp.includes(idx) ? this.active_timeStamp.splice(this.active_timeStamp.indexOf(idx), 1) : this.active_timeStamp.push(idx)
    //   this.interviewTimes.includes(this.time_list[idx]) ? this.interviewTimes.splice(this.interviewTimes.indexOf(this.time_list[idx]), 1) : this.interviewTimes.push(this.time_list[idx])
    //   // this.interviewTimes.forEach((element) => {
    //   //   this.payload_json[Object.keys(this.payload_json)[Object.keys(this.payload_json).length - 1]] = [element]
    //   // })
    //   this.payload_json[Object.keys(this.payload_json)[Object.keys(this.payload_json).length - 1]] = [...this.interviewTimes]
    // },
  }
}
</script>
