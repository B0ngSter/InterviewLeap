<template>
  <b-container v-if="payment" class="py-5">
    <b-row align-v="start" align-content="start" class="flex-grow-1">
      <b-col cols="12">
        <b-breadcrumb class="bg-light pl-0">
          <b-breadcrumb-item>
            Dashboard
          </b-breadcrumb-item>
          <b-breadcrumb-item>
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
      <b-col cols="12" class="mt-5">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row>
              <b-col cols="4" class="pt-5 pb-5 pl-4">
                <p class="text-left text-secondary">
                  Date
                </p>
                <p class="text-left text-dark font-weight-bold">
                  {{ date() }}
                </p>
              </b-col>
              <b-col cols="3" offset-md="2">
                <div class="mt-5 mb-5">
                  <b-button squared class="alert-danger text-danger-dark">
                    Cancel
                  </b-button>
                </div>
              </b-col>
              <b-col cols="3">
                <div class="mt-5 mb-5">
                  <b-button squared class="alert-primary text-primary" @click="reschedule">
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
            <b-row>
              <b-col cols="12" class="pt-5 pl-4">
                <p class="text-left text-secondary">
                  Time Slots you have selected
                </p>
              </b-col>
              <b-col
                v-for="(timeslot, idy) in timeSlots"
                :key="idy"
                cols="3"
                class="mb-3 cursor-pointer"
              >
                <b-card
                  no-body
                  class="p-3 pl-5 mt-3 border-0 alert-primary"
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
            <b-row>
              <b-col cols="6" class="pt-5 pl-4">
                <p class="text-left text-secondary">
                  Interview Charges
                </p>
              </b-col>
              <b-col cols="6" class="pt-5 pr-4">
                <h4 class="text-right text-secondary">
                  ₹500
                </h4>
              </b-col>
              <b-col cols="6" class="pt-2 pl-4">
                <p class="text-left text-secondary">
                  Taxes
                </p>
              </b-col>
              <b-col cols="6" class="pt-2 pr-4">
                <h4 class="text-right text-secondary">
                  ₹145
                </h4>
              </b-col>
              <hr>
              <b-col cols="6" class="pt-5 pl-4">
                <p class="text-left font-weight-bold">
                  Total Payable Amount
                </p>
              </b-col>
              <b-col cols="6" class="pt-5 pr-4">
                <h4 class="text-right font-weight-bold">
                  ₹645
                </h4>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col cols="12">
        <div class="text-center mt-5">
          <b-button variant="primary" @click="submit">
            proceed to pay
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
</template>

<script>
export default {
  props: {
    fetchedate: {
      type: String,
      required: true
    },
    timeSlots: {
      type: Array,
      required: true
    },
    payment: {
      type: Boolean,
      required: true
    },
    candidateInfo: {
      type: Object,
      required: true
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
    }
  },
  // mounted () {
  //   this.$axios.get('/book-interview/').then((response) => {
  //     debugger
  //     this.FetchedResponse = response.data
  //   })
  // },
  methods: {
    date () {
      let month = ''
      this.fetchedate.slice(5, 7).includes('0') ? month = this.fetchedate.slice(6, 7) : month = this.fetchedate.slice(5, 7)
      const monthList = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
      month = monthList[parseInt(month) - 1]
      const date = this.fetchedate.slice(8, 10)
      const year = this.fetchedate.slice(0, 4)
      const amplifiedDate = month + ' ' + date + ',' + year
      const day = String(new Date(amplifiedDate))
      return day.slice(0, 3) + ',' + day.slice(3, 10) + ', ' + day.slice(11, 16)
    },
    reschedule () {
      this.payment = false
      this.$emit('reschedule', this.payment)
    },
    submit () {
      const payload = { ...this.candidateInfo }
      payload.skills = payload.skills.toString() // to make skills in "python,java,vue.js" in this form
      const formData = new FormData()
      Object.keys(payload).map((key) => {
        formData.append(key, payload[key])
      })
      this.$axios.post('/book-interview/', formData)
        .then((response) => {
          if (response.data.long_url) {
            this.$router.push('response.data.long_url')
          }
          this.$toast.success('booked successfully', {
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
            errorResponse.response.data.message || 'Could not save your profile. Please try again later'
          )
        })
    }
  }
}
</script>

<style>
</style>
