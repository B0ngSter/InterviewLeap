<template>
  <b-container class="py-5">
    <b-row align-v="start" align-content="start" class="flex-grow-1">
      <b-col cols="12">
        <p v-if="!$store.getters.is_profile_completed && $store.getters.is_interviewer" class="float-right text-danger-dark">
          *Please update your profile which’ll help us
          schedule right interview for you.
        </p>
        <p v-if="!$store.getters.is_profile_completed && $store.getters.is_candidate" class="float-right text-danger-dark">
          *Update your ‘Profile’ before booking
          Interview for right match and complete evaluation !
        </p>
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
              <div class="d-flex justify-content-around flex-column flex-md-row mb-5">
                <label class="sr-only" for="first_name">First Name</label>
                <b-input
                  id="first_name"
                  v-model="profile.first_name"
                  class="mb-2 mb-sm-0 ml-md-4 mr-md-3 flex-fill"
                  placeholder="First Name"
                />
                <label class="sr-only" for="last_name">Last Name</label>
                <b-input
                  id="last_name"
                  v-model="profile.last_name"
                  class="mb-2 mb-sm-0 mr-md-4 ml-md-3 flex-fill"
                  placeholder="Last Name"
                />
              </div>
              <div class="d-flex justify-content-around flex-column flex-md-row mb-5">
                <label class="sr-only" for="email">Email</label>
                <b-input
                  id="email"
                  v-model="profile.email"
                  class="mb-2 mb-sm-0 ml-md-4 mr-md-3 flex-fill"
                  placeholder="Email"
                  type="email"
                />
                <label class="sr-only" for="mobile">Mobile Number</label>
                <b-input
                  id="mobile"
                  v-model="profile.mobile"
                  class="mb-2 mb-sm-0 mr-md-4 ml-md-3 flex-fill"
                  placeholder="Mobile Number"
                />
              </div>
              <div class="text-center">
                <b-button variant="primary" @click="current_tab=1">
                  Next
                </b-button>
              </div>
            </b-tab>
            <b-tab title="Professional Details" title-link-class="border-0">
              <div v-if="$store.getters.is_candidate" class="d-flex justify-content-start flex-column flex-md-row mb-5 ml-0 ml-md-4">
                <b-form-radio-group
                  v-model="profile.professional_status"
                  :options="professional_status_options"
                  value-field="val"
                  text-field="name"
                />
              </div>
              <div class="d-flex justify-content-around flex-column flex-md-row mb-5">
                <div v-if="profile.professional_status === 'Experienced' || $store.getters.is_interviewer" class="mb-2 mb-sm-0 mr-md-3 d-flex flex-fill">
                  <label class="sr-only" for="industry">Industry</label>
                  <b-input
                    id="industry"
                    v-model="profile.industry"
                    list="industry-options"
                    class="mb-2 mb-sm-0 ml-md-4 mr-md-3 flex-fill"
                    placeholder="Industry"
                    autocomplete="off"
                  />
                  <datalist id="industry-options">
                    <option v-for="(industry, idx) in industry_choices" :key="idx">
                      {{ industry }}
                    </option>
                  </datalist>
                </div>
                <div v-if="profile.professional_status === 'Experienced' || $store.getters.is_interviewer" class="mb-2 mb-sm-0 mr-md-4 mr-md-3 d-flex flex-fill">
                  <label class="sr-only" for="exp_years">Total Experience</label>
                  <b-input
                    id="exp_years"
                    v-model="profile.exp_years"
                    class="flex-fill"
                    placeholder="Total Experience"
                    type="number"
                    min="0"
                  />
                </div>
              </div>
              <div
                v-if="profile.professional_status === 'Experienced' || $store.getters.is_interviewer"
                class="d-flex justify-content-around flex-column flex-md-row mb-5"
              >
                <label class="sr-only" for="company">Current Company</label>
                <b-input
                  id="company"
                  v-model="profile.company"
                  class="mb-2 mb-sm-0 ml-md-4 mr-md-3 flex-fill"
                  placeholder="Current Company"
                />
                <label class="sr-only" for="designation">Designation</label>
                <b-input
                  id="designation"
                  v-model="profile.designation"
                  class="mb-2 mb-sm-0 mr-md-4 ml-md-3 flex-fill"
                  placeholder="Designation"
                />
              </div>
              <div
                v-if="profile.professional_status === 'Fresher' && $store.getters.is_candidate"
                class="d-flex justify-content-around flex-column flex-md-row mb-5"
              >
                <label class="sr-only" for="education">Highest Qualification</label>
                <b-input
                  id="education"
                  v-model="profile.education"
                  class="mb-2 mb-sm-0 ml-md-4 mr-md-3 flex-fill"
                  placeholder="Highest Qualification"
                />
                <label class="sr-only" for="college">College / University</label>
                <b-input
                  id="college"
                  v-model="profile.college"
                  class="mb-2 mb-sm-0 mr-md-4 ml-md-3 flex-fill"
                  placeholder="College / University"
                />
              </div>
              <div
                v-if="profile.professional_status === 'Fresher' && $store.getters.is_candidate"
                class="d-flex justify-content-around flex-column flex-md-row mb-5"
              >
                <label class="sr-only" for="years_of_passing">Year of passing</label>
                <b-input
                  id="years_of_passing"
                  v-model="profile.years_of_passing"
                  class="mb-2 mb-sm-0 ml-md-4 mr-md-3 flex-fill"
                  placeholder="Year of passing"
                />
                <label class="sr-only" for="job_title">Position looking for Eg: Java Developer</label>
                <b-input
                  id="job_title"
                  v-model="profile.job_title"
                  class="mb-2 mb-sm-0 mr-md-4 ml-md-3 flex-fill"
                  placeholder="Position looking for Eg: Java Developer"
                />
              </div>
              <div class="d-flex justify-content-around flex-column flex-md-row mb-5">
                <div class="mb-2 mb-sm-0 mr-md-4 d-flex flex-fill">
                  <label class="sr-only" for="resume">Latest Resume</label>
                  <b-form-file
                    id="resume"
                    v-model="profile.resume"
                    placeholder="Your latest resume"
                    drop-placeholder="Drop resume here..."
                    class="mb-2 mb-sm-0 ml-md-4 mr-md-3 flex-fill"
                  />
                </div>
                <div class="mb-2 mb-sm-0 mr-md-4 d-flex flex-fill">
                  <label class="sr-only" for="linkedin">Linkedin URL</label>
                  <b-input
                    id="linkedin"
                    v-model="profile.linkedin"
                    class="flex-fill"
                    placeholder="Linkedin URL"
                  />
                </div>
              </div>
              <div class="w-100 mb-5 px-0 px-md-4">
                <b-input-group>
                  <b-form-input
                    v-model="skill_search_query"
                    placeholder="Core Skills"
                    :disabled="skills_filled"
                  />
                  <b-input-group-append>
                    <b-button variant="secondary" :disabled="skills_filled" @click="addSkill">
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
              </div>
              <div v-if="$store.getters.is_candidate" class="text-center">
                <b-button variant="primary" @click="save_profile">
                  Save
                </b-button>
              </div>
              <div v-if="$store.getters.is_interviewer" class="text-center">
                <b-button variant="primary" @click="current_tab=2">
                  Next
                </b-button>
              </div>
            </b-tab>
            <b-tab v-if="$store.getters.is_interviewer" class="text-dark" title-link-class="border-0" title="Account Details">
              <div class="d-flex justify-content-around flex-column flex-md-row mb-5">
                <label class="sr-only" for="account_holder_name">Account Holder Name</label>
                <b-input
                  v-model="profile.account_holder_name"
                  class="mb-2 mb-sm-0 ml-md-4 mr-md-3 flex-fill"
                  required
                  placeholder="First Name"
                />
                <label class="sr-only" for="account_number">Account Number</label>
                <b-input
                  id="last_name"
                  v-model="profile.account_number"
                  class="mb-2 mb-sm-0 mr-md-4 ml-md-3 flex-fill"
                  placeholder="Account Number"
                />
              </div>
              <div class="d-flex justify-content-around flex-column flex-md-row mb-5">
                <label class="sr-only" for="IFSC">IFSC</label>
                <b-input
                  id="email"
                  v-model="profile.ifsc"
                  class="mb-2 mb-sm-0 ml-md-4 mr-md-3 flex-fill"
                  placeholder="IFSC"
                />
                <label class="sr-only" for="bank_name">Account Number</label>
                <b-input
                  id="mobile"
                  v-model="profile.bank_name"
                  class="mb-2 mb-sm-0 mr-md-4 ml-md-3 flex-fill"
                  placeholder="Bank Name"
                />
              </div>
              <div class="text-center">
                <b-button variant="primary" @click="save_profile">
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
export default {
  data () {
    return {
      profile: {
        first_name: '',
        skills: [],
        resume: null
      },
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
    // this.fetch_profile_data()
  },
  methods: {
    removeTag (skillIndex) {
      this.profile.skills.splice(skillIndex, 1)
    },
    addSkill () {
      if (!this.profile.skills.includes(this.skill_search_query)) {
        this.profile.skills.push(this.skill_search_query)
      }
      this.skill_search_query = ''
    },
    save_profile () {
      const payload = { ...this.profile }
      payload.skills = payload.skills.toString()
      const formData = new FormData()
      Object.keys(payload).map((key) => {
        formData.append(key, payload[key])
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
    },
    fetch_profile_data () {
      // this.profile.first_name = this.$store.getters.user_name
      let profileApiURL
      if (this.$store.getters.is_candidate) {
        profileApiURL = '/auth/candidate-profile'
      } else if (this.$store.getters.is_interviewer) {
        profileApiURL = '/auth/interviewer-profile'
      }
      this.$axios.get(profileApiURL).then((response) => {
        this.profile = response.data.profile
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
</style>
