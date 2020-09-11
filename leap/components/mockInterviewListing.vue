<template>
  <b-container>
    <b-row class="mt-5">
      <b-col cols="12" md="6" class="mt-5 mb-5">
        <h4 class="font-weight-bold">
          Open Mock Interviews
        </h4>
      </b-col>
      <b-col cols="12" md="6" class="mt-5 mb-5">
        <autocomplete
          search-endpoint="/interview-list"
          search-param-name="keyword"
          result-key="search_list"
          item-title-key="job_title"
          @select="selectSearchResult"
        />
      </b-col>
      <b-col v-if="mocks.length === 0" cols="12" class="mt-5">
        <div class="text-center pt-4">
          <b-img
            src="@/static/kio.svg"
            alt="InterviewLeap logo"
          />
          <p class="font-weight-bold mt-5">
            Didn’t find any suitable interviewer.
          </p>
          <p class="text-secondary">
            No worries you can book directly and we’ll find right
            Interviewer for you
          </p>
        </div>
        <div class="text-center mt-4">
          <b-button variant="primary" class="text-white" to="/book-interview">
            Book interview >
          </b-button>
        </div>
      </b-col>
      <b-col v-for="(mockInterview, idx) in mocks" :key="idx" class="mt-3" cols="12">
        <b-card no-body class="text-center border-0">
          <b-container class="bg-white">
            <b-row align-v="center" class="p-4 mt-3 mb-1" align-content="start">
              <b-col cols="3">
                <p class="text-left font-weight-bold">
                  {{ mockInterview.job_title }}
                </p>
                <p class="text-left text-secondary">
                  {{ mockInterview.exp_years }} year
                </p>
              </b-col>
              <b-col cols="5" class="border-left border-light">
                <p class="text-left text-secondary pl-3 pb-0 pt-2">
                  Interviewer From
                </p>
                <p class="text-left text-danger-dark pl-3 pb-0">
                  {{ mockInterview.company }}
                </p>
              </b-col>
              <b-col cols="4">
                <div class="text-right">
                  <b-button
                    class="alert-success text-primary"
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
import Autocomplete from './Autocomplete.vue'

export default {
  components: {
    Autocomplete
  },
  data: () => {
    return {
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
      searchResultMocks: [],
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
    'keyword_search.query' (searchQuery) {
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
    selectSearchResult (selectedResult) {
      this.$router.push(`/book-mock/${selectedResult.slug}`)
    },
    _perform_keyword_search (searchQuery) {
      this.$axios.get(`/interview-list?keyword=${searchQuery}`)
        .then((response) => {
          this.searchResultMocks = response.data.search_list
        })
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
