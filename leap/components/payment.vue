<template>
  <b-container class="py-5">
    <b-row align-v="start" align-content="start" class="flex-grow-1">
      <b-col cols="12">
        <b-breadcrumb class="bg-light pl-0">
          <b-breadcrumb-item to="/dashboard">
            Dashboard
          </b-breadcrumb-item>
          <b-breadcrumb-item v-if="!isMock" @click="reschedule">
            Book Interview
          </b-breadcrumb-item>
          <b-breadcrumb-item active>
            Payment
          </b-breadcrumb-item>
        </b-breadcrumb>
      </b-col>
      <b-col cols="6">
        <h2 class="mt-5">
          Interview Summary
        </h2>
      </b-col>
      <b-col cols="6">
        <div class="text-right text-danger-dark mt-5">
          *Cancelation of scheduled interview
          is non refundable
        </div>
      </b-col>
      <b-col cols="12" class="mt-5" style="width: 100%;">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row class="p-4 mt-3">
              <b-col cols="12" md="3">
                <p class="text-left text-secondary">
                  Date
                </p>
                <p class="text-left text-dark font-weight-bold">
                  {{ date() }}
                </p>
              </b-col>
              <b-col v-if="isMock" cols="12" md="3">
                <p class="text-left text-secondary">
                  Interview from
                </p>
                <p class="text-left text-danger-dark font-weight-bold">
                  {{ company_name }}
                </p>
              </b-col>
              <b-col cols="6" md="2" :offset-md="isMock ? 2 : 4">
                <div class="text-right">
                  <b-button squared class="alert-danger" @click="cancel">
                    <span class="text-danger-dark">
                      Cancel
                    </span>
                  </b-button>
                </div>
              </b-col>
              <b-col cols="6" md="2">
                <div class="text-right">
                  <b-button squared class="alert-primary custom_btn text-primary" @click="reschedule">
                    Reschedule
                  </b-button>
                </div>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col cols="12">
        <b-card no-body class="text-center border-0 mt-2">
          <b-container class="bg-white">
            <b-row v-if="!isMock" class="p-4">
              <b-col cols="12" class="">
                <p class="text-left text-secondary">
                  Time Slots you have selected
                </p>
              </b-col>
              <b-col
                v-for="(timeslot, idy) in candidateInfo.time_slots"
                :key="idy"
                cols="3"
                class="cursor-pointer"
              >
                <b-card
                  no-body
                  class="p-3 mt-3 border-0 alert-primary"
                >
                  {{ timeslot }}
                </b-card>
              </b-col>
            </b-row>
            <b-row v-if="isMock" class="p-4">
              <b-col cols="12" class="">
                <p class="text-left text-secondary">
                  Time Slots you have selected
                </p>
              </b-col>
              <b-col
                v-for="(timeslot, idy) in timeSlotsMock"
                :key="idy"
                cols="3"
                class="cursor-pointer"
              >
                <b-card
                  no-body
                  class="p-3 mt-3 border-0 alert-primary"
                >
                  {{ timeslot }}
                </b-card>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col cols="12">
        <b-card no-body class="text-center border-0 mt-2">
          <b-container class="bg-white">
            <b-row class="p-4">
              <b-col cols="6" class="pt-4">
                <p class="text-left text-secondary">
                  Interview Charges
                </p>
              </b-col>
              <b-col cols="6" class="pt-4">
                <h4 class="text-right text-secondary">
                  ₹{{ amount }}
                </h4>
              </b-col>
              <b-col cols="6" class="pt-4">
                <p class="text-left text-secondary">
                  Taxes
                </p>
              </b-col>
              <b-col cols="6" class="pt-4">
                <h4 class="text-right text-secondary">
                  ₹{{ tax }}
                </h4>
              </b-col>
              <b-col cols="6" class="pt-4 border-top border-light">
                <h4 class="text-left text-secondary">
                  Total Payable Amount
                </h4>
              </b-col>
              <b-col cols="6" class="pt-4 border-top border-light">
                <h4 class="text-right font-weight-bold">
                  ₹{{ total_amount }}
                </h4>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col cols="12">
        <div class="text-center mt-5">
          <b-button class="text-white" variant="primary" @click="submit">
            Proceed to pay
          </b-button>
        </div>
      </b-col>
      <b-col cols="12">
        <div class="text-center text-secondary mt-5 pt-5 pb-5 mb-5">
          2020 Stellar Software Technologies Pvt ltd
        </div>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  props: {
    timeSlotsMock: {
      type: Array,
      required: false
    },
    candidateInfo: {
      type: Object,
      required: true
    },
    isMock: {
      type: Boolean
    }
  },
  data () {
    return {
      // FetchedResponse: {
      //   // applied_designation: 'ew',
      //   // company_type: 'product',
      //   // date: '2020-07-29',
      //   // skills: 'frrrrrrsw,wsw',
      //   // time_slots: ['12PM - 3PM', '3PM - 6PM'],
      //   // time_zone: 'static 12'
      // }
      amount: null,
      tax: null,
      total_amount: null,
      company_name: null
    }
  },
  mounted () {
    this.$axios.get('/book-interview')
      .then((response) => {
        this.total_amount = response.data.total_amount
        this.tax = response.data.tax
        this.amount = response.data.amount
      })
      .catch((errorResponse) => {
        this.$toast.error(
          errorResponse.response.data.message || 'Something went wrong'
        )
      })
    this.fetch_company_name()
  },
  methods: {
    fetch_company_name () {
      this.$axios.get('/interview-list/').then((response) => {
        response.data.mocks.map((key) => {
          if (key.slug === this.$route.params.slug) {
            this.company_name = key.company
          }
        })
      })
    },
    date () {
      let month = ''
      this.candidateInfo.date.slice(5, 7).includes('0') ? month = this.candidateInfo.date.slice(6, 7) : month = this.candidateInfo.date.slice(5, 7)
      const monthList = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
      month = monthList[parseInt(month) - 1]
      const date = this.candidateInfo.date.slice(8, 10)
      const year = this.candidateInfo.date.slice(0, 4)
      const amplifiedDate = month + ' ' + date + ',' + year
      const day = String(new Date(amplifiedDate))
      return day.slice(0, 3) + ',' + day.slice(3, 10) + ', ' + day.slice(11, 16)
    },
    reschedule () {
      this.$emit('reschedule', false)
    },
    submit () {
      let payload = {}
      let endpoint
      if (this.isMock) {
        endpoint = `/book-mock/${this.$route.params.slug}/`
        payload.start_time = this.candidateInfo.time_slots[0].slice(0, 5)
        payload.end_time = this.candidateInfo.time_slots[0].slice(8, 13)
        payload.amount = this.amount
        payload.date = this.candidateInfo.date
        payload.tax = this.tax
        payload.total_amount = this.total_amount
      } else {
        payload = { ...this.candidateInfo }
        payload.skills = payload.skills.toString() // to make skills in "python,java,vue.js" in this form
        endpoint = '/book-interview/'
      }
      this.$axios.post(endpoint, payload)
        .then((response) => {
          if (response.data.long_url) {
            window.open(response.data.long_url, '_self')
          } else if (response.data.message) {
            this.$toast.error(response.data.message, {
              action: {
                text: 'Close',
                onClick: (e, toastObject) => {
                  toastObject.goAway(0)
                }
              }
            })
          }
        })
        .catch((errorResponse) => {
          this.$toast.error(
            errorResponse.response.data.message || 'Could not book your interview. Please try again later'
          )
        })
    },
    cancel () {
      this.$router.push('/dashboard')
    }
  }
}
</script>

<style>
.custom_btn {
  padding: 1.34rem 1.8rem 1.34rem 1.8rem;
}
</style>
