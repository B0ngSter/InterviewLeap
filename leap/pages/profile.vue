<template>
  <b-container class="py-5 bg-light">
    <b-row align-v="start" align-content="start" class="flex-grow-1">
      <b-col cols="12">
        <div class="ml-3 mb-5">
          <b-breadcrumb class="bg-light pl-0">
            <b-breadcrumb-item to="/dashboard">
              Dashboard
            </b-breadcrumb-item>
            <b-breadcrumb-item active>
              Profile
            </b-breadcrumb-item>
          </b-breadcrumb>
        </div>
      </b-col>
      <b-col cols="12">
        <span v-if="!$store.getters.is_profile_completed && $store.getters.is_interviewer" class="float-right text-danger-dark">
          *Please update your profile which’ll help us
          schedule right interview for you.
        </span>
        <span v-if="!$store.getters.is_profile_completed && $store.getters.is_candidate" class="float-right text-danger-dark">
          *Update your ‘Profile’ before booking
          Interview for right match and complete evaluation !
        </span>
        <h3>Profile</h3>
      </b-col>
      <b-col cols="12" class="bg-light py-3">
        <b-form id="auth_form">
          <b-tabs
            v-model="current_tab"
            content-class="py-5 px-4 bg-white"
            class="flex-grow-1 font-weight-bold"
            nav-class="border-0 form_container"
            active-nav-item-class="text-primary"
            fill
          >
            <b-tab title="Personal Details" active title-link-class="border-0">
              <b-container>
                <b-row>
                  <b-col
                    class="mt-4"
                    cols="12"
                    md="6"
                  >
                    <b-form-group>
                      <b-form-input
                        v-model="$v.profile.first_name.$model"
                        class="bg-white"
                        required
                        placeholder="First Name"
                        :state="validateState('first_name')"
                        aria-describedby="input-1-live-feedback"
                      />
                      <b-form-invalid-feedback
                        id="input-1-live-feedback"
                      >
                        This is a required field.
                      </b-form-invalid-feedback>
                    </b-form-group>
                  </b-col>
                  <b-col
                    class="mt-4"
                    cols="12"
                    md="6"
                  >
                    <b-form-group>
                      <b-form-input
                        v-model="$v.profile.last_name.$model"
                        class="bg-white"
                        required
                        placeholder="Last Name"
                        :state="validateState('last_name')"
                        aria-describedby="input-1-live-feedback"
                      />
                      <b-form-invalid-feedback
                        id="input-1-live-feedback"
                      >
                        This is a required field.
                      </b-form-invalid-feedback>
                    </b-form-group>
                  </b-col>
                  <b-col
                    class="mt-4"
                    cols="12"
                    md="6"
                  >
                    <b-input
                      v-model="profile.email"
                      placeholder="Email"
                      type="email"
                      disabled
                    />
                  </b-col>
                  <b-col
                    class="mt-4"
                    cols="12"
                    md="6"
                  >
                    <b-form-group>
                      <b-form-input
                        v-model="$v.profile.mobile_number.$model"
                        class="bg-white"
                        required
                        placeholder="Mobile Number"
                        :state="validateState('mobile_number')"
                        aria-describedby="input-1-live-feedback"
                      />
                      <b-form-invalid-feedback
                        id="input-1-live-feedback"
                      >
                        Not a valid number.
                      </b-form-invalid-feedback>
                    </b-form-group>
                  </b-col>
                  <b-col cols="12" class="mt-4">
                    <div class="text-center">
                      <b-button class="text-white" variant="primary" :disabled="!profile.mobile_number || profile.mobile_number.length > 10 || profile.mobile_number.length < 10" @click="current_tab=1">
                        Next
                      </b-button>
                    </div>
                  </b-col>
                </b-row>
              </b-container>
            </b-tab>
            <b-tab title="Professional Details" title-link-class="border-0">
              <b-container>
                <b-row>
                  <b-col v-if="$store.getters.is_candidate" class="mt-4" cols="12">
                    <b-form-radio-group
                      v-model="profile.professional_status"
                      :options="professional_status_options"
                      value-field="val"
                      text-field="name"
                    />
                  </b-col>
                  <b-col
                    v-if="profile.professional_status === 'Experienced' || $store.getters.is_interviewer"
                    class="mt-4"
                    cols="12"
                    md="6"
                  >
                    <b-form-group>
                      <b-form-input
                        v-model="$v.profile.industry.$model"
                        class="bg-white"
                        required
                        :state="validateState('industry')"
                        aria-describedby="input-1-live-feedback"
                        list="industry-options1"
                        placeholder="Industry"
                        autocomplete="off"
                      />
                      <datalist id="industry-options1">
                        <option v-for="(industry, idx) in industry_choices" :key="idx">
                          {{ industry }}
                        </option>
                      </datalist>
                      <b-form-invalid-feedback
                        id="input-1-live-feedback"
                      >
                        This is a required field.
                      </b-form-invalid-feedback>
                    </b-form-group>
                  </b-col>
                  <b-col
                    v-if="profile.professional_status === 'Experienced' || $store.getters.is_interviewer"
                    class="mt-4"
                    cols="12"
                    md="6"
                  >
                    <b-form-group>
                      <b-form-input
                        v-model="$v.profile.exp_years.$model"
                        class="bg-white"
                        min="0"
                        required
                        type="number"
                        placeholder="Total Experience"
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
                  <b-col
                    v-if="profile.professional_status === 'Experienced' || $store.getters.is_interviewer"
                    class="mt-4"
                    cols="12"
                    md="6"
                  >
                    <b-form-group>
                      <b-form-input
                        v-model="$v.profile.company.$model"
                        class="bg-white"
                        required
                        placeholder="Current Company"
                        :state="validateState('company')"
                        aria-describedby="input-1-live-feedback"
                      />
                      <b-form-invalid-feedback
                        id="input-1-live-feedback"
                      >
                        This is a required field.
                      </b-form-invalid-feedback>
                    </b-form-group>
                  </b-col>
                  <b-col
                    v-if="profile.professional_status === 'Experienced' || $store.getters.is_interviewer"
                    class="mt-4"
                    cols="12"
                    md="6"
                  >
                    <b-form-group>
                      <b-form-input
                        v-model="$v.profile.designation.$model"
                        class="bg-white"
                        required
                        placeholder="Designation"
                        :state="validateState('designation')"
                        aria-describedby="input-1-live-feedback"
                      />
                      <b-form-invalid-feedback
                        id="input-1-live-feedback"
                      >
                        This is a required field.
                      </b-form-invalid-feedback>
                    </b-form-group>
                  </b-col>
                  <b-col
                    v-if="profile.professional_status === 'Fresher' && $store.getters.is_candidate"
                    class="mt-4"
                    cols="12"
                    md="6"
                  >
                    <b-form-group>
                      <b-form-input
                        v-model="$v.profile.education.$model"
                        class="bg-white"
                        required
                        placeholder="Highest Qualification"
                        :state="validateState('education')"
                        aria-describedby="input-1-live-feedback"
                      />
                      <b-form-invalid-feedback
                        id="input-1-live-feedback"
                      >
                        This is a required field.
                      </b-form-invalid-feedback>
                    </b-form-group>
                  </b-col>
                  <b-col
                    v-if="profile.professional_status === 'Fresher' && $store.getters.is_candidate"
                    class="mt-4"
                    cols="12"
                    md="6"
                  >
                    <b-form-group>
                      <b-form-input
                        v-model="$v.profile.college.$model"
                        class="bg-white"
                        required
                        placeholder="College / University"
                        :state="validateState('college')"
                        aria-describedby="input-1-live-feedback"
                      />
                      <b-form-invalid-feedback
                        id="input-1-live-feedback"
                      >
                        This is a required field.
                      </b-form-invalid-feedback>
                    </b-form-group>
                  </b-col>
                  <b-col
                    v-if="profile.professional_status === 'Fresher' && $store.getters.is_candidate"
                    class="mt-4"
                    cols="12"
                    md="6"
                  >
                    <b-form-group>
                      <b-form-input
                        v-model="$v.profile.year_of_passing.$model"
                        class="bg-white"
                        required
                        type="number"
                        placeholder="Year of passing"
                        :state="validateState('year_of_passing')"
                        aria-describedby="input-1-live-feedback"
                      />
                      <b-form-invalid-feedback
                        id="input-1-live-feedback"
                      >
                        This is a required field.
                      </b-form-invalid-feedback>
                    </b-form-group>
                  </b-col>
                  <b-col
                    v-if="profile.professional_status === 'Fresher' && $store.getters.is_candidate"
                    class="mt-4"
                    cols="12"
                    md="6"
                  >
                    <b-form-group>
                      <b-form-input
                        v-model="$v.profile.job_title.$model"
                        class="bg-white"
                        required
                        placeholder="Position looking for Eg: Java Developer"
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
                  <b-col class="mt-4" cols="12" md="6">
                    <div v-if="existing_resume && !re_upload_resume">
                      <a :href="existing_resume" target="_blank">Current Resume</a>
                      <b-button class="text-white ml-5" variant="primary" @click="re_upload_resume = true">
                        Click to change
                      </b-button>
                    </div>
                    <b-form-file
                      v-else
                      id="resume"
                      style="width: 100%;"
                      placeholder="Your latest resume"
                      drop-placeholder="Drop resume here..."
                    />
                  </b-col>
                  <b-col class="mt-4" cols="12" md="6">
                    <b-form-group>
                      <b-form-input
                        v-model="$v.profile.linkedin.$model"
                        class="bg-white"
                        required
                        placeholder="Linkedin URL"
                        :state="validateState('linkedin') && profile.linkedin.includes('linkedin')"
                        aria-describedby="input-1-live-feedback"
                      />
                      <b-form-invalid-feedback
                        id="input-1-live-feedback"
                      >
                        This is a required field.
                      </b-form-invalid-feedback>
                    </b-form-group>
                  </b-col>
                  <b-col v-if="profile.professional_status === 'Fresher' && $store.getters.is_candidate" class="mt-4" cols="12">
                    <b-form-group>
                      <b-form-input
                        v-model="$v.profile.industry.$model"
                        class="bg-white"
                        required
                        :state="validateState('industry')"
                        aria-describedby="input-1-live-feedback"
                        list="industry-options"
                        placeholder="Industry"
                        autocomplete="off"
                      />
                      <datalist id="industry-options">
                        <option v-for="(industry, idx) in industry_choices" :key="idx">
                          {{ industry }}
                        </option>
                      </datalist>
                      <b-form-invalid-feedback
                        id="input-1-live-feedback"
                      >
                        This is a required field.
                      </b-form-invalid-feedback>
                    </b-form-group>
                  </b-col>
                  <b-col class="mt-4" cols="12">
                    <b-input-group>
                      <b-form-input
                        v-model="skill_search_query"
                        placeholder="Core Skills"
                        list="skill-options"
                        :disabled="skills_filled"
                        @keypress="fetchSkills"
                        @keydown.enter="addSkill"
                      />
                      <datalist id="skill-options">
                        <option v-for="(Skill, idp) in fetchedSkill" :key="idp">
                          {{ Skill }}
                        </option>
                      </datalist>
                      <b-input-group-append>
                        <b-button class="text-white" variant="primary" :disabled="skills_filled" @click="addSkill">
                          Add
                        </b-button>
                      </b-input-group-append>
                    </b-input-group>
                    <p class="mt-2 text-muted font-weight-normal">
                      {{ profile.skills.length }}/5 skills selected
                    </p>
                    <h4>
                      <b-badge
                        v-for="(skill, id_s) in profile.skills"
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
                  <b-col class="mt-4" cols="12">
                    <div v-if="$store.getters.is_candidate" class="text-center">
                      <b-button variant="primary" class="text-white" :disabled="profile.linkedin === null || profile.skills.length === 0 || profile.professional_status === ''" @click="save_profile">
                        Save
                      </b-button>
                    </div>
                    <div v-if="$store.getters.is_interviewer" class="text-center">
                      <b-button class="text-white" :disabled="profile.linkedin === null || profile.skills.length === 0" variant="primary" @click="current_tab=2">
                        Next
                      </b-button>
                    </div>
                  </b-col>
                </b-row>
              </b-container>
            </b-tab>
            <b-tab v-if="$store.getters.is_interviewer" class="text-dark" title-link-class="border-0" title="Account Details">
              <p class="text-secondary mb-5">
                Account Details required after verification. Optional before verification.
              </p>
              <b-container>
                <b-row>
                  <b-col class="mt-4" cols="12" md="6">
                    <b-form-group>
                      <b-form-input
                        v-model="$v.profile.account_info.acc_name.$model"
                        class="bg-white"
                        required
                        placeholder="Account holder’s name"
                        :state="validateState_forAccount('acc_name')"
                        aria-describedby="input-1-live-feedback"
                      />
                      <b-form-invalid-feedback
                        id="input-1-live-feedback"
                      >
                        This is a required field.
                      </b-form-invalid-feedback>
                    </b-form-group>
                  </b-col>
                  <b-col class="mt-4" cols="12" md="6">
                    <b-form-group>
                      <b-form-input
                        v-model="$v.profile.account_info.account_number.$model"
                        class="bg-white"
                        required
                        placeholder="Account Number"
                        :state="validateState_forAccount('account_number')"
                        aria-describedby="input-1-live-feedback"
                      />
                      <b-form-invalid-feedback
                        id="input-1-live-feedback"
                      >
                        This is a required field.
                      </b-form-invalid-feedback>
                    </b-form-group>
                  </b-col>
                  <b-col class="mt-4" cols="12" md="6">
                    <b-form-group>
                      <b-form-input
                        v-model="$v.profile.account_info.ifsc_code.$model"
                        class="bg-white"
                        required
                        placeholder="IFSC"
                        :state="validateState_forAccount('ifsc_code')"
                        aria-describedby="input-1-live-feedback"
                      />
                      <b-form-invalid-feedback
                        id="input-1-live-feedback"
                      >
                        This is a required field.
                      </b-form-invalid-feedback>
                    </b-form-group>
                  </b-col>
                  <b-col class="mt-4" cols="12" md="6">
                    <b-form-group>
                      <b-form-input
                        v-model="$v.profile.account_info.bank.$model"
                        class="bg-white"
                        required
                        placeholder="Bank Name"
                        :state="validateState_forAccount('bank')"
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
              <div class="text-center mt-4">
                <b-button class="text-white" variant="primary" @click="save_profile">
                  Save
                </b-button>
              </div>
            </b-tab>
          </b-tabs>
        </b-form>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, minLength, maxLength, url, numeric } from 'vuelidate/lib/validators'
export default {
  mixins: [validationMixin],
  layout: 'app-page',
  data () {
    return {
      re_upload_resume: false,
      existing_resume: false,
      profile: {
        skills: [],
        first_name: null,
        last_name: null,
        email: null,
        exp_years: null,
        industry: null,
        designation: null,
        mobile_number: null,
        education: null,
        year_of_passing: null,
        job_title: null,
        company: null,
        account_info: {
          acc_name: null,
          account_number: null,
          ifsc_code: null,
          bank: null
        },
        college: null,
        linkedin: null,
        resume: null,
        professional_status: ''
      },
      fetchedSkill: [],
      current_tab: 0,
      industry_choices: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15].map(num => `static ${num}`),
      professional_status_options: [
        {
          name: 'I am Employed',
          val: 'Experienced'
        }, {
          name: 'I am a Fresher',
          val: 'Fresher'
        }
      ],
      skill_search_query: ''
    }
  },
  computed: {
    skills_filled () {
      return this.profile.skills.length >= 5
    }
  },
  mounted () {
    this.fetch_industry_choices()
    this.fetch_profile_data()
  },
  validations: {
    profile: {
      first_name: { required },
      last_name: { required },
      college: { required },
      exp_years: { required },
      industry: { required },
      designation: { required },
      mobile_number: { required, minLength: minLength(10), maxLength: maxLength(10), numeric },
      education: { required },
      company: { required },
      year_of_passing: { required },
      job_title: { required },
      linkedin: { required, url },
      account_info: {
        acc_name: { required },
        account_number: { required, numeric },
        ifsc_code: { required },
        bank: { required }
      }
    }
  },
  methods: {
    validateState (name) {
      const { $dirty, $error } = this.$v.profile[name]
      return $dirty ? !$error : null
    },
    validateState_forAccount (name) {
      const { $dirty, $error } = this.$v.profile.account_info[name]
      return $dirty ? !$error : null
    },
    removeTag (skillIndex) {
      this.profile.skills.splice(skillIndex, 1)
    },
    addSkill () {
      if (this.skill_search_query.length === 0) {
      } else if (!this.profile.skills.includes(this.skill_search_query)) {
        this.profile.skills.push(this.skill_search_query)
      }
      this.skill_search_query = ''
    },
    save_profile () {
      // this.$v.profile.$touch()
      // if (this.$v.profile.$anyError) {
      // }
      const payload = { ...this.profile }
      payload.skills = payload.skills.toString() // to make skills in "python,java,vue.js" in this form
      // if (payload.company == null && payload.college !== null) {
      //   delete payload.company
      //   delete payload.designation
      //   delete payload.exp_years
      //   delete payload.industry
      //   delete payload.account_info
      // }
      // if (payload.college == null && payload.company !== null) {
      //   delete payload.college
      //   delete payload.year_of_passing
      //   delete payload.education
      //   delete payload.job_title
      //   delete payload.account_info
      // }
      // if (payload.college == null && payload.company == null) {
      //   delete payload.college
      //   delete payload.year_of_passing
      //   delete payload.education
      //   delete payload.job_title
      //   delete payload.company
      //   delete payload.designation
      //   delete payload.exp_years
      //   delete payload.industry
      // }
      const formData = new FormData()
      if (!this.existing_resume) {
        formData.append('resume', document.getElementById('resume').files[0])
      }
      Object.keys(payload).map((key) => {
        if (key === 'account_info') {
          formData.append(key, JSON.stringify(payload[key]))
        } else {
          formData.append(key, payload[key])
        }
      })
      let profileApiURL
      if (this.$store.getters.is_candidate) {
        profileApiURL = '/auth/candidate-profile/'
      } else if (this.$store.getters.is_interviewer) {
        profileApiURL = '/auth/interviewer-profile/'
      }
      this.$axios.post(profileApiURL, formData
      ).then((response) => {
        if (response.status === 200) {
          this.$router.push('/dashboard')
          this.$toast.success('Your profile changes were saved', {
            action: {
              text: 'Close',
              onClick: (e, toastObject) => {
                toastObject.goAway(0)
              }
            }
          })
        }
      }).catch((errorResponse) => {
        this.$toast.error(
          errorResponse.response.data.message || 'Could not save your profile. Please try again later'
        )
      })
    },
    fetch_industry_choices () {
      this.$axios.get('/industries')
        .then((response) => {
          this.industry_choices = response.data.industries
        })
        .catch((errorResponse) => {
          this.$toast.error(
            errorResponse.response.data.message || 'Something went wrong'
          )
        })
    },
    fetch_profile_data () {
      let profileApiURL
      if (this.$store.getters.is_candidate) {
        profileApiURL = '/auth/candidate-profile/'
      } else if (this.$store.getters.is_interviewer) {
        profileApiURL = '/auth/interviewer-profile/'
      }
      this.$axios.get(profileApiURL).then((response) => {
        this.existing_resume = response.data.resume
        if (response.data.skills) {
          response.data.skills = response.data.skills.map((key) => {
            return key.title
          })
        } else {
          response.data.skills = []
        }
        if (!response.data.account_info) {
          response.data.account_info = {
            acc_name: null,
            account_number: null,
            ifsc_code: null,
            bank: null
          }
        }
        if (!response.data.linkedin) {
          response.data.college = null
          response.data.exp_years = null
          response.data.industry = null
          response.data.designation = null
          response.data.mobile_number = null
          response.data.education = null
          response.data.company = null
          response.data.year_of_passing = null
          response.data.job_title = null
          response.data.linkedin = null
        }
        this.profile = response.data
        delete this.profile.resume
      })
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
.form_container a.nav-link {
  color: #555;
  padding: 20px 0;
  border-radius: 0;
}
.custom-file {
  width: unset;
}
.form_container a.nav-link:hover {
  color: #5dcc99;
}
</style>
