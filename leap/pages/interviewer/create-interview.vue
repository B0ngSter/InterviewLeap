<template>
  <div>
    <b-container class="py-5">
      <b-row align-v="start" align-content="start" class="flex-grow-1">
        <b-col cols="12">
          <b-breadcrumb class="bg-light pl-0">
            <b-breadcrumb-item>
              Dashboard
            </b-breadcrumb-item>
            <b-breadcrumb-item active>
              Create Interview
            </b-breadcrumb-item>
          </b-breadcrumb>
        </b-col>
        <b-col cols="12">
          <h2 class="mt-5">
            Hello, Saurav
          </h2>
          <!-- <p>Hello, {{ $store.getters.full_name[0] }}</p> -->
          <p class="text-secondary">
            Your upcoming interview requests
          </p>
        </b-col>
        <b-col cols="12" class="mt-5">
          <b-card no-body class="text-center border-0">
            <b-container class="bg-white">
              <b-row>
                <b-col cols="6" class="pt-5 pb-5">
                  <label class="sr-only" for="last_name">L</label>
                  <b-input
                    class="mb-2 mb-sm-0 mr-md-4 ml-md-3 flex-fill"
                    placeholder="Job Title"
                  />
                </b-col>
                <b-col cols="6" class="pt-5 pb-5 pr-5">
                  <label class="sr-only" for="last_name">R</label>
                  <b-input
                    class="mb-2 mb-sm-0 mr-md-4 ml-md-3 flex-fill"
                    placeholder="Experience Required (Optional)"
                  />
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
          v-for="(dates, idy) in [0, 1, 2, 3, 4, 5, 6]"
          :key="idy"
          class="mt-5 ml-5"
        >
          <b-badge
            pill
            class="p-4"
            :class="{
              'bg-primary': idy === active_dateStamp,
              'text-dark': idy === active_dateStamp ? false : true,
              'bg-white': idy === active_dateStamp ? false : true
            }"
            @click="badge_active(idy)"
          >
            {{ day(dates) }}
          </b-badge>
          <h4
            class="p-3"
            :class="{
              'text-dark': idy === active_dateStamp ? false : true,
              'text-primary': idy === active_dateStamp ? true : false
            }"
          >
            {{ date(dates) }}
          </h4>
        </b-col>
      </b-row>
    </b-container>
    <b-container>
      <b-row cols="5">
        <b-col
          v-for="(time, idx) in time_list"
          :key="idx"
        >
          <b-card
            no-body
            class="p-3 pl-5 mt-3 border-0"
            :class="{
              'alert-primary': active_timeStamp.includes(idx)
            }"
            @click="time_stamp(idx)"
          >
            {{ time }}
          </b-card>
        </b-col>
        <b-col cols="12">
          <div class="text-center mt-5 mb-5">
            <b-button variant="primary" @click="submit">
              Create Interview
            </b-button>
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  layout: 'app-page',
  data () {
    return {
      time_list: ['8 am - 9 am', '9 am - 10 am', '10 am - 11 am', '11 am - 12 pm', '12 pm - 1 pm', '2 pm - 3 pm', '4 pm -5 pm', '6 pm - 7 pm', '8 pm - 9 pm', '10 pm - 11 pm'],
      active_dateStamp: null,
      active_timeStamp: [],
      interviewTimes: [],
      date_array: [],
      time_array: [],
      idy_arr: [],
      payload_json: {}
    }
  },
  methods: {
    month () {
      const today = new Date()
      const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
      return months[today.getMonth()]
    },
    day (value) {
      const today = new Date()
      const dayss = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
      return dayss[today.getDay() + value]
    },
    date (val) {
      const today = new Date()
      return today.getDate() + val
    },
    badge_active (idy) {
      const today = new Date()
      const date = parseInt(('0' + today.getDate()).slice(-2)) + idy
      const month = ('0' + (today.getMonth() + 1)).slice(-2)
      const year = today.getFullYear()
      const formatedDate = year + '-' + month + '-' + date
      this.date_array.push(formatedDate)
      this.date_array.forEach((element) => {
        this.payload_json[element] = []
      })
      this.time_array.push([...this.active_timeStamp, -1, idy])
      this.active_timeStamp = []
      // if (idy === this.idy_arr[this.idy_arr.length - 1]) {
      //   this.active_timeStamp = this.time_array[this.time_array.length - 1]
      // }
      this.time_array.forEach((element) => {
        if (element.length > 2) {
          if (idy === element[element.length - 1]) {
            const new2 = element.slice(0, -2)
            this.active_timeStamp = new2
          }
        }
      })
      this.time_array.push([...this.interviewTimes])
      this.active_dateStamp = idy
      this.interviewTimes = []
    },
    time_stamp (idx) {
      this.active_timeStamp.includes(idx) ? this.active_timeStamp.splice(this.active_timeStamp.indexOf(idx), 1) : this.active_timeStamp.push(idx)
      this.interviewTimes.includes(this.time_list[idx]) ? this.interviewTimes.splice(this.interviewTimes.indexOf(this.time_list[idx]), 1) : this.interviewTimes.push(this.time_list[idx])
      // this.interviewTimes.forEach((element) => {
      //   this.payload_json[Object.keys(this.payload_json)[Object.keys(this.payload_json).length - 1]] = [element]
      // })
      this.payload_json[Object.keys(this.payload_json)[Object.keys(this.payload_json).length - 1]] = [...this.interviewTimes]
    },
    submit () {
    }
  }
}
</script>

<style>
</style>
