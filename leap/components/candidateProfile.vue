<template>
  <b-container class="py-5">
    <b-row>
      <b-col cols="12">
        <b-breadcrumb class="bg-light pl-0">
          <b-breadcrumb-item to="/dashboard">
            Dashboard
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
          <b-button variant="primary" class="text-white">
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
        <p><span class="text-secondary">Current Designation:</span> <span>{{ profileResponse.designation }}</span></p>
        <p><span class="text-secondary">Current Company:</span> <span>{{ profileResponse.company }}</span></p>
        <p><span class="text-secondary">Total Years of Experience:</span> <span>{{ profileResponse.exp_years }}</span></p>
        <p><span class="text-secondary">LinkedIn Profile:</span> <span>{{ profileResponse.linkedin }}</span></p>
        <p>Skills:</p>
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
  layout: 'app-page',
  props: {
    profileResponse: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
    }
  }
}
</script>

<style>
</style>
