<template>
  <b-container class="align-items-start">
    <b-row align-v="start" align-content="start">
      <b-col cols="12">
        <h1>Testing page</h1>
        <b-btn variant="danger">Reschedule</b-btn>
        <b-btn variant="primary">Decline</b-btn>
        <b-btn variant="danger">Error</b-btn>
        <b-btn variant="info">Accept</b-btn>
        <b-btn variant="success">Book</b-btn>
      </b-col>
      <div>
        testing: {{ date_row }}
        <p v-for="(timeslots, date, idx) in date_row" :key="idx" @click="select_date(date)" :class="{'selected': date === selected_date}">
          {{ date }}
        </p>
      </div>
      <div v-if="selected_date">
        <button v-for="(timeslot, idy) in time_slots" :key="idy" @click="toggle_timeslot(timeslot)" :class="{'selected': date_row[selected_date].includes(timeslot)}">{{ timeslot }}</button>
      </div>
    </b-row>
  </b-container>
</template>

<script>
import Vue from 'vue'
export default {
  layout: 'app-page',
  data () {
    return {
      selected_date: null,
      date_row: {},
      time_slots: [
        '0 - 6',
        '6 - 12',
        '12 - 18',
        '18 - 0'
      ]
    }
  },
  methods: {
    toggle_timeslot (timeslot) {
      const timeslotIdx = this.date_row[this.selected_date].indexOf(timeslot)
      if (timeslotIdx > -1) {
        this.date_row[this.selected_date].splice(timeslotIdx, 1)
      } else {
        this.date_row[this.selected_date].push(timeslot)
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
      for (let i = 0; i < dates.length; i++) {
        const date = dates[i]
        Vue.set(this.date_row, new Date(date), [])
      }
    }
  },
  mounted () {
    this.generate_dates()
  }
}
</script>

<style>
  .selected {
    color: red
  }
</style>
