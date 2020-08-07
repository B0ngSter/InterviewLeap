<template>
  <b-container>
    <b-row class="mt-5">
      <b-col cols="12" md="3" class="pb-5 mb-5">
        <h3 class="font-weight-bold">
          Hello, Tessa
        </h3>
        <p class="text-secondary">
          Your upcoming interviews
        </p>
      </b-col>
      <b-col cols="12" md="6" class="pb-5 mb-5">
        <div class="text-center">
          <b-img
            class="cursor-pointer"
            src="@/static/kio.svg"
            alt="Mock"
            height="308"
          />
          <p class="font-weight-bold">
            No interview scheduled for now
          </p>
        </div>
      </b-col>
      <b-col cols="12" md="3" class="pb-5 mb-5">
        <div class="text-right">
          <b-button class="bg-primary">
            Book interview
          </b-button>
        </div>
      </b-col>
      <b-col cols="12" md="6" class="mt-5 mb-5">
        <h4 class="font-weight-bold">
          Open Mock Interviews
        </h4>
      </b-col>
      <b-col cols="12" md="6" class="mt-5 mb-5">
        <b-input-group size="md" class="mb-2">
          <b-form-input
            v-model="searchString"
            type="search"
            class="bg-light"
            placeholder="Search by role"
          />
          <b-input-group-prepend is-text>
            <b-icon icon="search" />
          </b-input-group-prepend>
        </b-input-group>
      </b-col>
      <b-col v-for="(mockInterview, idx) in filteredMocks" :key="idx" class="mt-3" cols="12">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row align-v="center" align-content="start">
              <b-col cols="4" class="pt-5 pb-5">
                <p class="text-left font-weight-bold">
                  {{ mockInterview.jobTitle }}
                </p>
                <p class="text-left text-secondary">
                  {{ mockInterview.Exp }}
                </p>
              </b-col>
              <b-col cols="4">
                <p class="text-left text-secondary">
                  Interviewer From
                </p>
                <p class="text-left text-danger-dark">
                  {{ mockInterview.company }}
                </p>
              </b-col>
              <b-col cols="4">
                <div class="text-right">
                  <b-button class="bg-primary" @click="BookMockInterview(idx)">
                    Book
                  </b-button>
                </div>
              </b-col>
            </b-row>
          </b-container>
        </b-card>
      </b-col>
      <b-col cols="12">
        <p class="text-secondary mt-5 mb-5 pb-5 pt-5 text-center">
          2020 Stellar Software Technologies Pvt ltd
        </p>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  data: () => {
    return {
      searchString: '',
      mocks: [
        {
          jobTitle: 'Senior Android Developer',
          company: 'Amazon',
          Exp: '5-8 Years'
        },
        {
          jobTitle: 'Hadoop Developer',
          company: 'E & Y',
          Exp: '5-8 Years'
        },
        {
          jobTitle: '.NET Developer',
          company: 'JP Morgan',
          Exp: '5-8 Years'
        },
        {
          jobTitle: 'UX Desiger',
          company: 'Deloitte',
          Exp: '5-8 Years'
        }
      ],
      companyName: ''
    }
  },
  computed: {
    filteredMocks () {
      let searchStr = this.searchString
      let mocks = this.mocks
      if (!searchStr) {
        return mocks
      }
      searchStr = searchStr.trim().toLowerCase()
      mocks = mocks.filter((item) => {
        if (item.jobTitle.toLowerCase().includes(searchStr)) {
          return item
        }
      })
      return mocks
    }
  },
  mounted () {
    this.$axios.get('/dashboard/').then((response) => {
    })
  },
  methods: {
    BookMockInterview (idx) {
      this.$store.commit('mock_interview_company_name', this.mocks[idx].company)
      this.$router.push('/book-mock')
    }
  }
}
</script>

<style>
</style>
