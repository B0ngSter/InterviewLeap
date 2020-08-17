<template>
  <b-container>
    <b-row class="mt-5">
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
                  <b-button
                    class="bg-primary"
                    @click="BookMockInterview(idx)"
                  >
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
          slug: 'ufsadsa2',
          jobTitle: 'Senior Android Developer',
          company: 'Amazon',
          Exp: '5-8 Years'
        },
        {
          slug: 'ufsadsa3',
          jobTitle: 'Hadoop Developer',
          company: 'E & Y',
          Exp: '5-8 Years'
        },
        {
          slug: 'ufsadsa4',
          jobTitle: '.NET Developer',
          company: 'JP Morgan',
          Exp: '5-8 Years'
        },
        {
          slug: 'ufsadsa5',
          jobTitle: 'UX Desiger',
          company: 'Deloitte',
          Exp: '5-8 Years'
        }
      ],
      upcoming_interviews: [
        {
          date: '2020-08-21',
          job_title: 'Byjus',
          slug: 'rvfw5lvb'
        },
        {
          date: '2020-08-21',
          job_title: 'Byjus',
          slug: 'ip3fjjmo'
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
      this.mock = response.data.mocks
    })
      .catch((errorResponse) => {
        this.$toast.error(
          errorResponse.response.data.message || 'Something went wrong'
        )
      })
  },
  methods: {
    BookMockInterview (idx) {
      this.$store.commit('mock_interview_company_name', this.mocks[idx].company)
      this.$router.push('/book-mock?id=${' + this.filteredMocks[idx].slug + '}')
    }
  }
}
</script>

<style>
</style>
