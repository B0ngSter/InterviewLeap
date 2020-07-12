<template>
  <b-container class="py-5">
    <b-row align-v="start" align-content="start" class="flex-grow-1">
      <b-col cols="12">
        <p class="float-right text-danger-dark">
          *Update your ‘Profile’ before booking
          Interview for right match and complete evaluation !
        </p>
        <h3>Profile</h3>
      </b-col>
      <b-col cols="12" class="bg-light py-3">
        <b-form inline>
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
                  class="mb-2 mb-sm-0 ml-md-4 mr-md-3 flex-fill"
                  placeholder="First Name"
                ></b-input>
                <label class="sr-only" for="last_name">Last Name</label>
                <b-input
                  id="last_name"
                  class="mb-2 mb-sm-0 mr-md-4 ml-md-3 flex-fill"
                  placeholder="Last Name"
                ></b-input>
              </div>
              <div class="d-flex justify-content-around flex-column flex-md-row mb-5">
                <label class="sr-only" for="email">Email</label>
                <b-input
                  id="email"
                  class="mb-2 mb-sm-0 ml-md-4 mr-md-3 flex-fill"
                  placeholder="Email"
                  type="email"
                ></b-input>
                <label class="sr-only" for="mobile">Mobile Number</label>
                <b-input
                  id="mobile"
                  class="mb-2 mb-sm-0 mr-md-4 ml-md-3 flex-fill"
                  placeholder="Mobile Number"
                ></b-input>
              </div>
              <div class="text-center">
                <b-button variant="primary" @click="current_tab=1">
                  Next
                </b-button>
              </div>
            </b-tab>
            <b-tab title="Professional Details" title-link-class="border-0">
              <div class="d-flex justify-content-start flex-column flex-md-row mb-5 ml-0 ml-md-4">
                <b-form-radio-group
                  v-model="profile.professional_status"
                  :options="professional_status_options"
                  value-field="val"
                  text-field="name"
                ></b-form-radio-group>
              </div>
              <div class="d-flex justify-content-around flex-column flex-md-row mb-5">
                <label class="sr-only" for="industry">Industry</label>
                <b-input
                  list="industry-options"
                  id="industry"
                  class="mb-2 mb-sm-0 ml-md-4 mr-md-3 flex-fill"
                  placeholder="Industry"
                  autocomplete="off"
                ></b-input>
                <datalist id="industry-options">
                  <option v-for="(industry, idx) in industry_choices" :key="idx">{{ industry }}</option>
                </datalist>
                <label class="sr-only" for="resume">Latest Resume</label>
                <b-form-file
                  id="resume"
                  v-model="profile.resume"
                  placeholder="Your latest resume"
                  drop-placeholder="Drop resume here..."
                  class="mb-2 mb-sm-0 ml-md-4 mr-md-3 flex-fill"
                ></b-form-file>
              </div>
              <div class="d-flex justify-content-around flex-column flex-md-row mb-5">
                <label class="sr-only" for="current_company">Current Company</label>
                <b-input
                  id="current_company"
                  class="mb-2 mb-sm-0 ml-md-4 mr-md-3 flex-fill"
                  placeholder="Current Company"
                ></b-input>
                <label class="sr-only" for="designation">Designation</label>
                <b-input
                  id="designation"
                  class="mb-2 mb-sm-0 mr-md-4 ml-md-3 flex-fill"
                  placeholder="Designation"
                ></b-input>
              </div>
              <div class="d-flex justify-content-around flex-column flex-md-row mb-5">
                <label class="sr-only" for="exp">Total Experience</label>
                <b-input
                  id="exp"
                  class="mb-2 mb-sm-0 ml-md-4 mr-md-3 flex-fill"
                  placeholder="Total Experience"
                  type="number"
                ></b-input>
                <label class="sr-only" for="linkedin">Linkedin URL</label>
                <b-input
                  id="linkedin"
                  class="mb-2 mb-sm-0 mr-md-4 ml-md-3 flex-fill"
                  placeholder="Linkedin URL"
                ></b-input>
              </div>
              <div class="w-100 mb-5 px-0 px-md-4">
                <b-input-group>
                  <!-- Always bind the id to the input so that it can be focused when needed -->
                  <b-form-input
                    v-model="skill_search_query"
                    placeholder="Core Skills"
                    :disabled="skills_filled"
                  ></b-form-input>
                  <b-input-group-append>
                    <b-button @click="addSkill" variant="secondary" :disabled="skills_filled">Add</b-button>
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
                          @click="removeTag(id_s)"
                          class="cursor-pointer"
                        />
                      </span>
                  </b-badge>
                </h4>
                <!--<b-form-tags v-model="skills" @input="$emit('input', $event)">
                  <template v-slot="{ tags, addTag, removeTag }">
                    Tags: <b-badge v-for="(tag, idx) in tags" :key="idx" @click="removeTag(tag)">{{ tag }}</b-badge>
                    <hr>
                    &lt;!&ndash;<b-button @click="addTag(value)" variant="primary">Add</b-button>&ndash;&gt;
                    &lt;!&ndash;<b-input-group aria-controls="my-custom-tags-list">
                      <input
                        v-bind="inputAttrs"
                        v-on="inputHandlers"
                        placeholder="Skills"
                        class="form-control">
                      <b-input-group-append>
                        <b-button @click="addTag()" variant="primary">Add</b-button>
                      </b-input-group-append>
                    </b-input-group>&ndash;&gt;
                    &lt;!&ndash;<b-form-input list="my-list-id" v-bind="inputAttrs" v-on="inputHandlers" placeholder="Skills"></b-form-input>&ndash;&gt;
                    &lt;!&ndash;<datalist id="my-list-id">
                      <option>Manual Option</option>
                      <option v-for="size in sizes">{{ size }}</option>
                    </datalist>&ndash;&gt;
                    <b-input-group class="mb-2">
                      <b-form-input
                        v-model="skill_search_query"
                        placeholder="New tag - Press enter to add"
                        class="form-control"
                        list="my-list-id"
                        debounce="300"
                      ></b-form-input>
                      <datalist id="my-list-id">
                        <option v-for="(skill, idy) in skill_search_results" :key="idy">{{ skill }}</option>
                        <option>Manual Option</option>
                      </datalist>
                      <b-input-group-append>
                        <b-button @click="addTag()" variant="primary">Add</b-button>
                      </b-input-group-append>
                    </b-input-group>

                  </template>
                </b-form-tags>-->
              </div>
            </b-tab>
          </b-tabs>

          <!--<b-form-group id="input-group-2" label="Your Name:" label-for="input-2">
            <b-form-input
              id="input-2"
              v-model="form.name"
              required
              placeholder="Enter name"
            ></b-form-input>
          </b-form-group>

          <b-form-group id="input-group-3" label="Food:" label-for="input-3">
            <b-form-select
              id="input-3"
              v-model="form.food"
              :options="foods"
              required
            ></b-form-select>
          </b-form-group>

          <b-form-group id="input-group-4">
            <b-form-checkbox-group v-model="form.checked" id="checkboxes-4">
              <b-form-checkbox value="me">Check me out</b-form-checkbox>
              <b-form-checkbox value="that">Check that out</b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>

          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>-->
        </b-form>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  layout: 'app-page',
  data () {
    return {
      profile: {
        skills: []
      },
      current_tab: 0,
      industry_choices: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15].map(num => `static ${num}`),
      professional_status_options: [
        {
          name: 'I am Employed',
          val: 'Employed'
        }, {
          name: 'I am a Fresher',
          val: 'Fresher'
        }
      ],
      // skill_search_results: [],
      skill_search_query: ''
    }
  },
  computed: {
    skills_filled () {
      return this.profile.skills.length >= 5
    }
  },
  methods: {
    /* search_skills (query) {
      debugger
      this.skill_search_results = [1, 2, 3, 4, 5, 6].map(num => `${query} ${num}`)
    }, */
    removeTag (skillIndex) {
      this.profile.skills.splice(skillIndex, 1)
    },
    addSkill () {
      if (!this.profile.skills.includes(this.skill_search_query)) {
        this.profile.skills.push(this.skill_search_query)
      }
      this.skill_search_query = ''
    }
  }
  /* watch: {
    skill_search_query (newVal, oldVal) {
      debugger
      if (newVal !== oldVal) {
        this.search_skills(newVal)
      }
    }
  } */
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
