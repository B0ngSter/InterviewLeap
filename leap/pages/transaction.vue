<template>
  <div class="full-height">
    <b-container v-if="!hide_Report_details">
      <b-row class="mt-5">
        <b-col cols="12">
          <b-breadcrumb class="bg-light pl-0">
            <b-breadcrumb-item to="/dashboard">
              Dashboard
            </b-breadcrumb-item>
            <b-breadcrumb-item active>
              Transactions
            </b-breadcrumb-item>
          </b-breadcrumb>
        </b-col>
        <b-col cols="12" md="3" class="mt-2 pt-2">
          <h3 class="font-weight-bold">
            Transactions
          </h3>
        </b-col>
        <b-col offset-md="6" cols="12" md="3" class="mt-2 pt-2 text-right">
          <h4 class="cursor-pointer">
            <span>
              <b-img
                src="@/static/sort.png"
                alt="InterviewLeap logo"
              />
            </span>
            <span class="pl-3">Sort</span>
          </h4>
        </b-col>
        <b-col v-if="transactions.length === 0" cols="12" md="12" class="pb-5 mb-5">
          <div class="text-center">
            <b-img
              class="cursor-pointer mt-5"
              src="@/static/kio.svg"
              alt="Mock"
              height="308"
            />
            <p class="font-weight-bold mt-5">
              No Transactions found
            </p>
          </div>
        </b-col>
        <b-col v-for="(interviews, idx) in transactions" :key="idx" cols="12" class="mt-5">
          <b-card no-body class="text-center border-0">
            <b-container class="bg-white">
              <b-row class="p-4 mt-3">
                <b-col cols="12" md="3" class="pb-2">
                  <p class="text-left text-secondary">
                    Month {{ !ext.includes(idx) }}
                  </p>
                  <p class="text-left text-dark font-weight-bold">
                    {{ interviews.month }}
                  </p>
                </b-col>
                <b-col cols="12" md="3" class="pb-2">
                  <p class="text-left text-secondary">
                    Amount
                  </p>
                  <p class="text-left text-danger-dark font-weight-bold">
                    {{ interviews.amount }}
                  </p>
                </b-col>
                <b-col cols="12" md="3" class="pb-2">
                  <p class="text-left text-secondary">
                    Transaction Date
                  </p>
                  <p class="text-left text-danger-dark font-weight-bold">
                    <!-- {{ date(idx) }} -->
                  </p>
                </b-col>
                <b-col md="3" cols="12">
                  <div cols="12" md="3" class="pb-2 text-right">
                    <b-button squared :class="{ 'alert-success': interviews.status === 'completed', 'text-primary': interviews.status === 'completed', 'text-warning': interviews.status === 'pending', 'alert-warning': interviews.status === 'pending' }" @click="viewReport(interviews)">
                      {{ interviews.status }}
                    </b-button>
                  </div>
                </b-col>
                <b-col cols="12" md="6" class="border-top border-light pt-4">
                  <p class="text-left font-weight-bold">
                    <span>Interview Leap</span>
                    <span v-if="interviews.status === 'pending'" class="pl-2 pr-2">
                      <b-img
                        src="@/static/right_gray.svg"
                        alt="Mock"
                      />
                    </span>
                    <span v-if="interviews.status === 'completed'" class="pl-2 pr-2">
                      <b-img
                        src="@/static/right_green.svg"
                        alt="Mock"
                      />
                    </span>
                    <span>You</span>
                  </p>
                </b-col>
                <b-col cols="12" md="6" class="border-top text-right border-light pt-4">
                  <p class="cursor-pointer" @click="openDetails(idx)">
                    <span :class="{'text-primary': !ext.includes(idx)}">
                      View Details
                    </span>
                    <span v-if="ext.includes(idx)">
                      <b-img
                        src="@/static/next_up.svg"
                        alt="Mock"
                      />
                    </span>
                    <span v-if="!ext.includes(idx)">
                      <b-img
                        src="@/static/next_down.svg"
                        alt="Mock"
                      />
                    </span>
                  </p>
                </b-col>
                <transition name="slide-fade">
                  <b-col v-if="!ext.includes(idx)" cols="6" class="pt-4" md="6">
                    <p class="text-left text-secondary">
                      Interviews taken from us
                    </p>
                  </b-col>
                </transition>
                <transition name="slide-fade">
                  <b-col v-if="!ext.includes(idx)" cols="6" class="pt-4" md="6">
                    <p class="text-right font-weight-bold">
                      7 X 450 = ₹3150
                    </p>
                  </b-col>
                </transition>
                <transition name="slide-fade">
                  <b-col v-if="!ext.includes(idx)" cols="6" class="pt-3 pb-2" md="6">
                    <p class="text-left text-secondary">
                      Interviews taken from open mock interviews
                    </p>
                  </b-col>
                </transition>
                <transition name="slide-fade">
                  <b-col v-if="!ext.includes(idx)" cols="6" class="pt-3 pb-2" md="6">
                    <p class="text-right font-weight-bold">
                      11 X 450 = ₹4950
                    </p>
                  </b-col>
                </transition>
                <transition name="slide-fade">
                  <b-col v-if="!ext.includes(idx)" cols="6" class="pt-4 mt-1 border-top border-light" md="6">
                    <h4 class="text-left pt-1">
                      Total
                    </h4>
                  </b-col>
                </transition>
                <transition name="slide-fade">
                  <b-col v-if="!ext.includes(idx)" cols="6" class="pt-4 mt-1 border-top border-light" md="6">
                    <h4 class="text-right pt-1">
                      18 X 450 = ₹8100
                    </h4>
                  </b-col>
                </transition>
                <transition name="slide-fade">
                  <b-col v-if="!ext.includes(idx)" cols="6" class="pt-4 pb-4" md="6">
                    <h4 class="text-left text-danger-dark">
                      Deductions
                    </h4>
                  </b-col>
                </transition>
                <transition name="slide-fade">
                  <b-col v-if="!ext.includes(idx)" cols="6" class="pt-4 pb-4" md="6">
                    <h4 class="text-right text-danger-dark">
                      -730
                    </h4>
                  </b-col>
                </transition>
                <transition name="slide-fade">
                  <b-col v-if="!ext.includes(idx)" cols="6" class="pt-5 pb-3 border-top border-light" md="6">
                    <h4 class="text-left text-primary">
                      Amount to be received
                    </h4>
                  </b-col>
                </transition>
                <transition name="slide-fade">
                  <b-col v-if="!ext.includes(idx)" cols="6" class="pt-5 pb-3 border-top border-light" md="6">
                    <h4 class="text-right text-primary">
                      ₹7370
                    </h4>
                  </b-col>
                </transition>
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
    <Report
      v-if="hide_Report_details"
      :report="report"
      @Back="hide_Report_details = $event"
    />
  </div>
</template>

<script>
import Report from '~/components/Report'
export default {
  components: {
    Report
  },
  layout: 'app-page',
  data () {
    return {
      report: null,
      hide_Report_details: false,
      ext: [],
      transactions: [
        {
          month: 'july',
          amount: 5000,
          transaction_date: '2020-04-12',
          status: 'pending',
          custom_interviews_taken: 5,
          mock_interviews_taken: 6
        },
        {
          month: 'june',
          amount: 5000,
          transaction_date: '2020-04-20',
          status: 'completed',
          custom_interviews_taken: 5,
          mock_interviews_taken: 6
        }
      ]
    }
  },
  mounted () {
    // this.fetch_interview()
    this.ext = Array.from(Array(50).keys())
  },
  methods: {
    openDetails (idx) {
      this.ext.includes(idx) ? this.ext.splice(this.ext.indexOf(idx), 1) : this.ext.push(idx)
    }
    // date (idx) {
    //   let month = ''
    //   this.transactions[idx].date.slice(5, 7).includes('0') ? month = this.transactions[idx].date.slice(6, 7) : month = this.transactions[idx].date.slice(5, 7)
    //   const monthList = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    //   month = monthList[parseInt(month) - 1]
    //   const date = this.transactions[idx].date.slice(8, 10)
    //   const year = this.transactions[idx].date.slice(0, 4)
    //   const amplifiedDate = month + ' ' + date + ',' + year
    //   const day = String(new Date(amplifiedDate))
    //   return day.slice(0, 3) + ',' + day.slice(3, 10) + ', ' + day.slice(11, 16)
    // }
    // fetch_interview () {
    //   this.$axios.get('/past-interview').then((response) => {
    //     this.transactions = response.data.transactions
    //   })
    //     .catch((errorResponse) => {
    //       this.$toast.error(
    //         errorResponse.response.data.message || 'Something went wrong'
    //       )
    //     })
    // },
    // viewReport (interviews) {
    //   this.hide_Report_details = true
    //   this.report = interviews
    // }
  }
}
</script>

<style>
.full-height {
  min-height: 100vh
}
.slide-fade-enter-active {
  transition: all 1s ease;
}
.slide-fade-enter {
  transform: translateX(20px);
  opacity: 0;
}
</style>
