<template>
  <div>
    <b-container v-if="!hide_payment_details" class="py-5">
      <b-row align-v="start" align-content="start" class="flex-grow-1">
        <b-col cols="12">
          <b-breadcrumb class="bg-light pl-0">
            <b-breadcrumb-item>
              Dashboard
            </b-breadcrumb-item>
            <b-breadcrumb-item active>
              Book Interview
            </b-breadcrumb-item>
          </b-breadcrumb>
        </b-col>
        <b-col cols="6">
          <h2 class="mt-3 font-weight-bold">
            Book Interview
          </h2>
        </b-col>
        <b-col cols="5" offset-md="1">
          <div class="text-left text-danger-dark mt-3 mb-2">
            *Update your ‘Profile’ before booking
            Interview for right match and  complete evaluation !
          </div>
        </b-col>
        <b-col cols="12" class="mt-5">
          <b-card no-body class="text-center border-0">
            <b-container class="bg-white">
              <b-row align-v="center" align-content="start">
                <b-col cols="4" md="5" class="pt-5 pb-5 ml-4">
                  <p class="text-left text-secondary">
                    Select Company Type you want to be interviewed for
                  </p>
                </b-col>
                <b-col cols="2">
                  <b-form-radio v-model="candidate_info.company_type" class="font-weight-bold" value="product" size="md">
                    Product
                  </b-form-radio>
                </b-col>
                <b-col cols="2">
                  <b-form-radio v-model="candidate_info.company_type" class="font-weight-bold" value="service" size="md">
                    Service
                  </b-form-radio>
                </b-col>
                <b-col cols="2">
                  <b-form-radio v-model="candidate_info.company_type" class="font-weight-bold" value="captive" size="md">
                    Captive
                  </b-form-radio>
                </b-col>
              </b-row>
            </b-container>
          </b-card>
        </b-col>
        <b-col cols="12" class="mt-2">
          <b-card no-body class="text-center border-0">
            <b-container class="bg-white">
              <b-row align-v="center" align-content="start">
                <b-col cols="12" md="12" class="pl-3 pr-3 pt-4">
                  <b-input-group>
                    <b-form-input
                      v-model="skill_search_query"
                      list="skill-options"
                      placeholder="Core Skills"
                      :disabled="skills_filled"
                      @change="fetchSkills"
                    />
                    <datalist id="skill-options">
                      <option v-for="(Skill, idp) in fetchedSkill" :key="idp">
                        {{ Skill }}
                      </option>
                    </datalist>
                    <b-button variant="primary" :disabled="skills_filled" @click="addSkill">
                      Add
                    </b-button>
                  </b-input-group>
                  <p class="mt-2 text-muted font-weight-normal">
                    {{ candidate_info.skills.length }}/5 skills selected
                  </p>
                  <h4>
                    <b-badge
                      v-for="(skill, id_s) in candidate_info.skills"
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
                <b-col cols="12" md="4" class="pt-5 pb-5">
                  <b-form-group>
                    <b-form-input
                      v-model="$v.candidate_info.time_zone.$model"
                      class="bg-white"
                      required
                      :state="validateState('time_zone')"
                      aria-describedby="input-1-live-feedback"
                      list="timeZones-options"
                      placeholder="timeZones"
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
                <b-col cols="12" md="4" class="pt-5 pb-5">
                  <b-form-datepicker
                    v-model="candidate_info.date"
                    :date-disabled-fn="allowedDates"
                    placeholder="Select Date"
                    menu-class="w-100"
                    calendar-width="100%"
                  />
                </b-col>
                <b-col cols="12" md="4" class="pt-5 pb-5">
                  <b-form-group>
                    <b-form-input
                      v-model="$v.candidate_info.applied_designation.$model"
                      class="bg-white"
                      required
                      placeholder="Role you’re interviewed for Eg: Senior Android Developer"
                      :state="validateState('applied_designation')"
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
        <b-col cols="12" md="8" class="mt-5">
          <h4 class="font-weight-bold">
            Select time Slot :
          </h4>
        </b-col>
        <b-col cols="12" md="4" class="mt-5">
          <span>
            <b-img
              src="@/static/question.svg"
              alt="Question"
            />
          </span>
          <span>Select 3 suitable time slots for interview.</span>
        </b-col>
        <b-col
          v-for="(timeslot, idy) in time_slots"
          :key="idy"
          class="mt-5 cursor-pointer"
        >
          <b-card
            no-body
            class="p-3 pl-5 mt-3 border-0"
            :class="{ 'alert-primary': time_slot.includes(idy) }"
            @click="addSlot(idy)"
          >
            {{ timeslot }}
          </b-card>
        </b-col>
        <b-col cols="12">
          <div class="text-center mt-5">
            <b-button variant="primary" :disabled="candidate_info.company_type === '' || candidate_info.skills.length === 0 || candidate_info.time_slots.length === 0 || candidate_info.applied_designation == null || candidate_info.time_zone == null || candidate_info.date == null" @click="submit">
              Book  Interview
            </b-button>
          </div>
        </b-col>
        <b-col cols="12">
          <div class="text-center text-secondary mt-5">
            2020 Stellar Software Technologies Pvt ltd
          </div>
        </b-col>
      </b-row>
    </b-container>
    <Payment
      v-if="hide_payment_details"
      :candidate-info="candidate_info"
      @reschedule="hide_payment_details = $event"
    />
  </div>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required } from 'vuelidate/lib/validators'
import Payment from '~/components/payment'
export default {
  layout: 'app-page',
  components: {
    Payment
  },
  mixins: [validationMixin],
  data () {
    return {
      hide_payment_details: false,
      time_slots: ['9AM - 12PM', '12PM - 3PM', '3PM - 6PM', '6PM - 9PM', '9PM - 12AM'],
      timeZone: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15].map(num => `static ${num}`),
      time_slot: [],
      candidate_info: {
        skills: [],
        company_type: '',
        time_slots: [],
        time_zone: null,
        applied_designation: null
      },
      skill_search_query: '',
      fetchedSkill: []
    }
  },
  computed: {
    skills_filled () {
      return this.candidate_info.skills.length >= 5
    }
  },
  mounted () {
    this.fetch_timeZone()
  },
  validations: {
    candidate_info: {
      applied_designation: { required },
      time_zone: { required }
    }
  },
  methods: {
    validateState (name) {
      const { $dirty, $error } = this.$v.candidate_info[name]
      return $dirty ? !$error : null
    },
    // fetch_timeSlots () {
    //   this.$axios.get('/time-slot')
    //     .then((response) => {
    //       this.time_slots = response.data.time_slot
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
    addSlot (idy) {
      this.time_slot.includes(idy) ? this.time_slot.splice(this.time_slot.indexOf(idy), 1) : this.time_slot.push(idy)
      this.candidate_info.time_slots.includes(this.time_slots[idy]) ? this.candidate_info.time_slots.splice(this.time_slot.indexOf(this.time_slots[idy]), 1) : this.candidate_info.time_slots.push(this.time_slots[idy])
    },
    allowedDates (val) {
      const today = new Date()
      const year = today.getFullYear()
      const month = today.getMonth() + 1
      const date = today.getDate()
      if (year <= parseInt(val.split('-')[0])) {
        if (year === parseInt(val.split('-')[0]) && month < parseInt(val.split('-')[1])) {
          return
        }
        if (year === parseInt(val.split('-')[0]) && month === parseInt(val.split('-')[1]) && date < parseInt(val.split('-')[2])) {
          return
        }
        return val
      }
    },
    removeTag (skillIndex) {
      this.candidate_info.skills.splice(skillIndex, 1)
    },
    addSkill () {
      if (!this.candidate_info.skills.includes(this.skill_search_query)) {
        this.candidate_info.skills.push(this.skill_search_query)
      } else if (this.skill_search_query === '') {
        return
      }
      this.skill_search_query = ''
    },
    submit () {
      this.hide_payment_details = true
    },
    fetchSkills () {
      this.$axios.get(`/skill-search?search=${this.skill_search_query}`)
        .then((response) => {
          if (response.status === 200) {
            this.fetchedSkill = response.data.result
          }
        })
    }
  }
}
</script>

<style>
</style>
