<template>
  <div class="full-height">
    <b-container>
      <b-row class="mt-5">
        <b-col cols="12">
          <h2>FAQ's</h2>
        </b-col>
        <b-col v-for="(question, idx) in faq" :key="idx" cols="12" class="mt-4">
          <b-card no-body class="text-center border-0">
            <b-container class="bg-white">
              <b-row>
                <b-col cols="6" class="pt-5 pb-5 pl-4">
                  <p class="text-left font-weight-bold">
                    Question {{ idx + 1 }}
                  </p>
                </b-col>
                <b-col cols="6" md="3" offset-md="3">
                  <div class="mt-5 mb-5 text-right">
                    <h1 class="text-primary cursor-pointer" @click="openTheQuestion">
                      <a v-b-toggle :href="'#accordion-'+ idx" @click.prevent>+</a>
                    </h1>
                  </div>
                </b-col>
                <b-col v-if="expand" cols="12">
                  <b-collapse :id="'accordion-'+ idx">
                    <p>{{ question.question }}</p>
                  </b-collapse>
                </b-col>
              </b-row>
            </b-container>
          </b-card>
        </b-col>
        <b-col cols="12">
          <div class="text-center text-secondary mt-5">
            2020 Stellar Software Technologies Pvt ltd
          </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  layout: 'app-page',
  data () {
    return {
      expand: false,
      faq: [
        {
          question: 'lorem ipsum'
        },
        {
          question: 'lorem ipsum'
        }
      ]
    }
  },
  methods: {
    openTheQuestion () {
      this.expand = true
    }
  }
}
</script>

<style>
.full-height {
  min-height: 100vh
}
a {
  text-decoration: none;
}
</style>
