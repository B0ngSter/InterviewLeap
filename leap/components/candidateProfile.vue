<template>
  <b-container class="py-5">
    <b-row>
      <b-col cols="12">
        <b-breadcrumb class="bg-light pl-0">
          <b-breadcrumb-item v-if="hideIr" @click="goBack">
            Dashboard
          </b-breadcrumb-item>
          <b-breadcrumb-item v-if="!hideIr" @click="goBack">
            Interview Requests
          </b-breadcrumb-item>
          <b-breadcrumb-item active>
            Profile
          </b-breadcrumb-item>
        </b-breadcrumb>
      </b-col>
      <b-col cols="6">
        <h2 class="mt-3 font-weight-bold">
          Candidate Profile
        </h2>
      </b-col>
      <b-col cols="6">
        <div class="text-right">
          <b-button variant="primary" class="text-white" @click="resume">
            Download Resume
          </b-button>
        </div>
      </b-col>
      <b-col cols="12" class="mt-5">
        <h3>Personal Details</h3>
        <p><span class="text-secondary">Name:</span> <span class="pl-2"> {{ profileResponse.first_name }} {{ profileResponse.last_name }}</span></p>
        <p><span class="text-secondary">Email Id:</span> <span class="pl-2">{{ profileResponse.email }}</span></p>
        <p><span class="text-secondary">Mobile No:</span> <span class="pl-2">{{ profileResponse.mobile_number }}</span></p>
      </b-col>
      <b-col cols="12" class="mt-5">
        <h3>Professional Details</h3>
        <p><span class="text-secondary">Employment Experience:</span> <span>{{ profileResponse.professional_status }}</span></p>
        <p><span class="text-secondary">Industry:</span> <span>{{ profileResponse.industry }}</span></p>
        <p v-if="profileResponse.professional_status === 'Employed'">
          <span class="text-secondary">Current Designation:</span> <span>{{ profileResponse.designation }}</span>
        </p>
        <p v-if="profileResponse.professional_status === 'Fresher'">
          <span class="text-secondary">Applied position:</span> <span>{{ profileResponse.job_title }}</span>
        </p>
        <p v-if="profileResponse.professional_status === 'Fresher'">
          <span class="text-secondary">College:</span> <span>{{ profileResponse.college }}</span>
        </p>
        <p v-if="profileResponse.professional_status === 'Fresher'">
          <span class="text-secondary">Year of passing:</span> <span>{{ profileResponse.year_of_passing }}</span>
        </p>
        <p v-if="profileResponse.professional_status === 'Fresher'">
          <span class="text-secondary">Qualification:</span> <span>{{ profileResponse.education }}</span>
        </p>
        <p v-if="profileResponse.professional_status === 'Employed'">
          <span class="text-secondary">Current Company:</span> <span>{{ profileResponse.company }}</span>
        </p>
        <p v-if="profileResponse.professional_status === 'Employed'">
          <span class="text-secondary">Total Years of Experience:</span> <span>{{ profileResponse.exp_years }}</span>
        </p>
        <p><span class="text-secondary">LinkedIn Profile:</span> <span>{{ profileResponse.linkedin }}</span></p>
        <p><span class="text-secondary">Skills:</span> <span v-for="(skill, idx) in profileResponse.skills" :key="idx">{{ skill.title }} </span></p>
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
    profileResponse: {
      type: Object,
      required: true
    },
    hideIr: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    goBack () {
      this.$emit('Back', false)
    },
    resume () {
      window.open(this.profileResponse.resume, '_blank')
    }
  }
}
</script>

<style>
</style>
