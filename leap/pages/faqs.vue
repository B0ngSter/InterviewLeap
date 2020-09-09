<template>
  <div class="full-height">
    <b-container>
      <b-row class="mt-5">
        <b-col cols="12">
          <h2>FAQ's</h2>
        </b-col>
        <b-col v-for="(question, idx) in faq" :key="idx" cols="12" class="mt-4" @click="openTheQuestion(idx)">
          <a v-b-toggle :href="'#accordion-'+ idx" style="text-decoration: none;" @click.prevent>
            <b-card no-body class="border-0">
              <b-container class="bg-white">
                <b-row>
                  <b-col cols="6" class="pl-5 pr-5 pt-5 pb-2">
                    <p class="text-left text-dark font-weight-bold">
                      Question {{ idx + 1 }}
                    </p>
                  </b-col>
                  <b-col cols="6" md="3" offset-md="3">
                    <div class="p-4 text-right">
                      <h1 class="text-primary cursor-pointer">
                        <h1 v-if="ext.includes(idx)">+</h1>
                        <h1 v-if="!ext.includes(idx)">-</h1>
                      </h1>
                    </div>
                  </b-col>
                  <b-col cols="12" class="pl-5 pr-5 pb-5">
                    <b-collapse :id="'accordion-'+ idx" class="border-top border-light">
                      <p class="text-secondary text-left pt-5">{{ question.question }}</p>
                    </b-collapse>
                  </b-col>
                </b-row>
              </b-container>
            </b-card>
          </a>
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
      ext: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
      counter: 0,
      faq: [
        {
          question: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam tempus et risus vestibulum egestas. Pellentesque aliquam fermentum nulla, quis sollicitudin arcu pretium vitae. Proin varius placerat dapibus. Curabitur finibus, ante ac varius interdum,'
        },
        {
          question: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam tempus et risus vestibulum egestas. Pellentesque aliquam fermentum nulla, quis sollicitudin arcu pretium vitae. Proin varius placerat dapibus. Curabitur finibus, ante ac varius interdum,'
        }
      ]
    }
  },
  methods: {
    openTheQuestion (idx) {
      this.ext.includes(idx) ? this.ext.splice(this.ext.indexOf(idx), 1) : this.ext.push(idx)
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
