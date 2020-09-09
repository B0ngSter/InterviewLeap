<template>
  <div>
    <b-container v-if="!hide_payment_details" class="py-5">
      <b-row align-v="start" align-content="start" class="flex-grow-1">
        <b-col cols="12">
          <b-breadcrumb class="bg-light pl-0">
            <b-breadcrumb-item to="/dashboard">
              Dashboard
            </b-breadcrumb-item>
            <b-breadcrumb-item active>
              Book Interview
            </b-breadcrumb-item>
          </b-breadcrumb>
        </b-col>
        <b-col cols="6">
          <h2 class="mt-3 font-weight-bold">
            Book Open Mock Interview
          </h2>
        </b-col>
        <b-col cols="5" offset-md="1">
          <div v-if="!is_profile_completed" class="text-left text-danger-dark mt-3 mb-2">
            *Update your ‘Profile’ before booking
            Interview for right match and  complete evaluation !
          </div>
        </b-col>
        <b-col cols="12" class="mt-5">
          <b-card no-body class="text-center border-0">
            <b-container class="bg-white">
              <b-row class="p-4">
                <b-col cols="12" md="6" class="mt-3">
                  <b-form-group>
                    <b-form-input
                      v-model="$v.candidate_info.time_zone.$model"
                      class="bg-white"
                      required
                      :state="validateState('time_zone')"
                      aria-describedby="input-1-live-feedback"
                      list="timeZones-options"
                      placeholder="time zones"
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
                <b-col cols="12" md="6" class="mt-3">
                  <b-form-datepicker
                    v-model="candidate_info.date"
                    :date-disabled-fn="allowedDates"
                    placeholder="Select Date"
                    menu-class="w-100"
                    calendar-width="100%"
                  />
                </b-col>
              </b-row>
            </b-container>
          </b-card>
        </b-col>
        <b-col cols="12" md="12" class="mt-5">
          <h4 class="font-weight-bold">
            Select time Slot :
          </h4>
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
            <b-button
              variant="primary"
              class="text-white"
              :disabled="candidate_info.time_slots.length === 0 || candidate_info.time_zone == null || candidate_info.date == null"
              @click="submit"
            >
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
      :is-mock="isMock"
      :time-slots-mock="time_slots_mock"
      @reschedule="hide_payment_details = $event"
    />
  </div>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required } from 'vuelidate/lib/validators'
import Payment from '~/components/payment'
export default {
  components: {
    Payment
  },
  layout: 'app-page',
  mixins: [validationMixin],
  data () {
    return {
      hide_payment_details: false,
      isMock: false,
      time_slots: ['9AM - 12PM', '12PM - 3PM', '3PM - 6PM', '6PM - 9PM', '9PM - 12AM'],
      time_slots_to_be_sent: ['09:00 - 12:00', '12:00 - 15:00', '15:00 - 18:00', '18:00 - 21:00', '21:00 - 00:00'], // time slotes requested for backend are in this form
      timeZone: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15].map(num => `static ${num}`),
      time_slot: [],
      is_profile_completed: null,
      time_slots_mock: [],
      candidate_info: {
        time_zone: null,
        time_slots: []
      }
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
          this.is_profile_completed = response.data.is_profile_completed
          if (!response.data.is_profile_completed) {
            this.$router.push('/profile')
          }
        })
    },
    addSlot (idy) {
      this.time_slot.includes(idy) ? this.time_slot.splice(this.time_slot.indexOf(idy), 1) : this.time_slot.push(idy)
      this.candidate_info.time_slots.includes(this.time_slots_to_be_sent[idy]) ? this.candidate_info.time_slots.splice(this.time_slot.indexOf(this.time_slots_to_be_sent[idy]), 1) : this.candidate_info.time_slots.push(this.time_slots_to_be_sent[idy])
      this.time_slots_mock.includes(this.time_slots[idy]) ? this.time_slots_mock.splice(this.time_slot.indexOf(this.time_slots[idy]), 1) : this.time_slots_mock.push(this.time_slots[idy])
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
    submit () {
      this.hide_payment_details = true
      this.isMock = true
    }
  }
}
</script>

<style>
.btn {
  color: rgb(0, 0, 0);
}
</style>
