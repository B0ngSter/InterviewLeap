<template>
  <b-container>
    <b-row class="mt-5">
      <b-col cols="12" md="6" class="mt-5 mb-5">
        <h4 class="font-weight-bold">
          Open Mock Interviews
        </h4>
      </b-col>
      <b-col cols="12" md="6" class="mt-5 mb-5">
        <b-input-group size="md" class="mb-2">
          <b-form-input
            v-model="keyword_search"
            class="bg-light"
            list="search-options"
            debounce="500"
            placeholder="Search by role"
          />
          <datalist id="search-options">
            <option v-for="(searchResult, idx) in tempmocks" :key="idx">
              <p @click="action(idx)">
                {{ searchResult.job_title }}
              </p>
            </option>
          </datalist>
          <!-- <b-form-datalist id="search-options">
            <option v-for="(searchResult, idx) in tempmocks" :key="idx">
              <p @click="action(idx)">
                {{ searchResult.job_title }}
              </p>
            </option>
          </b-form-datalist> -->
          <b-input-group-prepend is-text @click="resetMockListing">
            <b-icon icon="search" class="cursor-pointer" />
          </b-input-group-prepend>
        </b-input-group>
      </b-col>
      <b-col v-for="(mockInterview, idx) in mocks" :key="idx" class="mt-3" cols="12">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row align-v="center" align-content="start">
              <b-col cols="4" class="pt-5 pl-5 pb-5">
                <p class="text-left font-weight-bold">
                  {{ mockInterview.job_title }}
                </p>
                <p class="text-left text-secondary">
                  {{ mockInterview.exp_years }} year
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
                    variant="primary"
                    :to="`/book-mock/${mockInterview.slug}`"
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
      keyword_search: null,
      mocks: [
        // {
        //   slug: 'ufsadsa2',
        //   job_title: 'Senior Android Developer',
        //   company: 'Amazon',
        //   exp_years: '5-8 Years'
        // },
        // {
        //   slug: 'ufsadsa3',
        //   job_title: 'Hadoop Developer',
        //   company: 'E & Y',
        //   exp_years: '5-8 Years'
        // },
        // {
        //   slug: 'ufsadsa4',
        //   job_title: '.NET Developer',
        //   company: 'JP Morgan',
        //   exp_years: '5-8 Years'
        // },
        // {
        //   slug: 'ufsadsa5',
        //   job_title: 'UX Desiger',
        //   company: 'Deloitte',
        //   exp_years: '5-8 Years'
        // }
      ],
      upcoming_interviews: [
        // {
        //   date: '2020-08-21',
        //   job_title: 'Byjus',
        //   slug: 'rvfw5lvb'
        // },
        // {
        //   date: '2020-08-21',
        //   job_title: 'Byjus',
        //   slug: 'ip3fjjmo'
        // }
      ],
      tempmocks: [],
      companyName: ''
    }
  },
  // computed: {
  //   filteredMocks () {
  //     let searchStr = this.searchString
  //     let mocks = this.mocks
  //     if (!searchStr) {
  //       return mocks
  //     }
  //     searchStr = searchStr.trim().toLowerCase()
  //     mocks = mocks.filter((item) => {
  //       if (item.job_title.toLowerCase().includes(searchStr)) {
  //         return item
  //       }
  //     })
  //     return mocks
  //   }
  // },
  watch: {
    keyword_search (searchQuery) {
      this._perform_keyword_search(searchQuery)
    }
  },
  mounted () {
    this.$axios.get('/interview-list/').then((response) => {
      this.mocks = response.data.mocks
    })
      .catch((errorResponse) => {
        this.$toast.error(
          errorResponse.response.data.message || 'Something went wrong'
        )
      })
  },
  methods: {
    _perform_keyword_search (searchQuery) {
      this.$axios.get(`/interview-list?keyword=${searchQuery}`)
        .then((response) => {
          this.tempmocks = response.data.search_list
        })
    },
    action (idx) {
      this.mocks = this.tempmocks[idx]
    },
    resetMockListing () {
      this.$axios.get('/interview-list/').then((response) => {
        this.mocks = response.data.mocks
      })
        .catch((errorResponse) => {
          this.$toast.error(
            errorResponse.response.data.message || 'Something went wrong'
          )
        })
    }
  }
}
</script>

<style>
</style>
