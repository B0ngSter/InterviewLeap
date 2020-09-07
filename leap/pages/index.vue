<template>
  <div class="d-flex flex-grow-1 flex-column">
    <section class="bg-dark text-light min-h-100">
      <b-container fluid>
        <b-row class="align-items-center">
          <b-col cols="12" md="6" class="banner-block">
            <b-img src="~/static/banners/landing.png" class="pt-2 banner-img" fluid />
          </b-col>
          <b-col cols="12" md="4" class="text-center text-md-left">
            <h1 class="display-4 font-weight-bold mt-5 mt-md-0">
              Practice to Perfection
            </h1>
            <p class="h4 font-weight-normal mt-4">
              Warm up with  mock interviews with
              industry experts from
            </p>
            <p class="h4 font-weight-normal text-danger-dark mb-5">Google, Facebook, & more…</p>
            <b-button variant="outline-light mb-5 mb-md-0">Register Now</b-button>
          </b-col>
        </b-row>
      </b-container>
    </section>
    <section>
      <b-container fluid>
        <b-row class="justify-content-center bg-success-dark text-light">
          <b-col cols="11" md="9">
            <p class="h1 mw-660 py-11 mb-11 font-weight-bold">
              We help candidates shine by giving
              them a flexible and fair interview
              experience. <br>
              <u>
                <span class="text-smiley-green">Here's how</span>
              </u>
            </p>
          </b-col>
        </b-row>
        <b-row class="justify-content-center mt-n12 d-none d-md-flex">
          <b-col cols="9">
            <b-img src="~/static/img/4A69859D-B62F-4888-9D68-C6418DDA8FD6.png" fluid />
          </b-col>
        </b-row>
        <b-row class="justify-content-center mt-n12">
          <b-col cols="12" md="9">
            <div class="mw-660 bg-white p-6 text-joyful-dark font-weight-normal h5">
              <p>
                Interview Leap is built on the premise that practice & preparation are crucial to get over your
                anxieties when attending an interview.
              </p>

              <p>
                Book interviews with senior engineers, who’ll run you through hyperrealistic questions and give you
                actionable feedback. They won’t know a thing about you— they’re just here to help you get better.
              </p>
            </div>
          </b-col>
        </b-row>
        <b-row class="justify-content-center">
          <b-col cols="11" md="9">
            <b-container>
              <b-row class="justify-content-center">
                <b-col cols="11" md="5">
                  <b-card border-variant="white">
                    <b-card-body>
                      <b-img
                        height="66"
                        src="https://cdn.zeplin.io/5ef9852ffe48f580cf1a311f/assets/A0E65C66-4C78-460E-8F56-1629F58F801D.svg"
                      />
                      <p class="h5 mt-4 mb-3">Curated Resources</p>
                      <p class="text-joyful-dark">
                        Prime your interview skills & etiquette
                        by accessing the best hand-picked
                        and curated content covering every
                        aspect of the interview cycle
                      </p>
                    </b-card-body>
                  </b-card>
                </b-col>
                <b-col cols="11" md="5">
                  <b-card border-variant="white">
                    <b-card-body>
                      <b-img
                        height="66"
                        src="https://cdn.zeplin.io/5ef9852ffe48f580cf1a311f/assets/7B27535F-373D-4307-8630-BF988330F4EF.svg"
                      />
                      <p class="h5 mt-4 mb-3">Performance Feedback</p>
                      <p class="text-joyful-dark">
                        Get a detailed interview scorecard with
                        performance-based metrics and
                        comprehensive feedback on your
                        strengths &weaknesses.
                      </p>
                    </b-card-body>
                  </b-card>
                </b-col>
                <b-col cols="11" md="5">
                  <b-card border-variant="white">
                    <b-card-body>
                      <b-img
                        height="66"
                        src="https://cdn.zeplin.io/5ef9852ffe48f580cf1a311f/assets/09EF275B-62F0-4DF6-A9C7-6C554CE2BEBF.svg"
                      />
                      <p class="h5 mt-4 mb-3">Playback your Interview</p>
                      <p class="text-joyful-dark">
                        Our video interviewing system automatically records your interview so that you can review it
                        anytime.
                      </p>
                    </b-card-body>
                  </b-card>
                </b-col>
                <b-col cols="11" md="5">
                  <b-card border-variant="white">
                    <b-card-body>
                      <b-img
                        height="66"
                        src="https://cdn.zeplin.io/5ef9852ffe48f580cf1a311f/assets/7EC8B2CA-A9AA-4485-A542-1598E2138FE6.svg"
                      />
                      <p class="h5 mt-4 mb-3">Reduce Stress &amp; Anxiety</p>
                      <p class="text-joyful-dark">
                        Doubts about how to answer tricky
                        interview questions may stress you
                        out & create anxiety. Get over your
                        nerves with mock interviews.
                      </p>
                    </b-card-body>
                  </b-card>
                </b-col>
              </b-row>
            </b-container>
          </b-col>
        </b-row>
      </b-container>
    </section>
    <section>
      <b-container fluid>
        <b-row class="justify-content-center bg-light text-dark py-11">
          <b-col cols="11" md="7" class="mb-5">
            <p class="h1 text-dark mw-660 font-weight-bold">
              Hear from others on how we
              are <span class="text-success-dark">making a difference.</span>
            </p>
          </b-col>
          <b-col cols="11" md="7">
            <div v-swiper:mySwiper="swiperOptions">
              <div class="swiper-wrapper">
                <div
                  class="text-center swiper-slide"
                  v-for="(testimonial, idx) in testimonials"
                  :key="idx"
                >
                  <b-card border-variant="light" class="text-left bg-transparent">
                    <b-card-body>{{ testimonial.text }}</b-card-body>
                    <b-dropdown-divider />
                    <b-card-body>
                      <b-media class="align-items-center">
                        <template v-slot:aside>
                          <b-img :src="testimonial.user_dp" width="70" height="70" contain />
                        </template>
                        <h5 class="mt-0">{{ testimonial.user }}</h5>
                        {{ testimonial.credibility }}
                      </b-media>
                    </b-card-body>
                  </b-card>
                </div>
              </div>
              <div class="swiper-pagination"></div>
            </div>
            <!-- Alternative implementation: works only on client-side(SSR Disabled) -->
            <!--<client-only>
              <swiper class="swiper" :options="swiperOptions">
                <b-icon icon="arrow-right" class="swiper-button-next"></b-icon>
                <swiper-slide
                  class="text-center"
                  v-for="(testimonial, idx) in testimonials"
                  :key="idx"
                >
                  <b-card border-variant="light" class="text-left bg-transparent">
                    <b-card-body>{{ testimonial.text }}</b-card-body>
                    <b-dropdown-divider />
                    <b-card-body>
                      <b-media class="align-items-center">
                        <template v-slot:aside>
                          <b-img :src="testimonial.user_dp" width="70" height="70" contain />
                        </template>
                        <h5 class="mt-0">{{ testimonial.user }}</h5>
                        {{ testimonial.credibility }}
                      </b-media>
                    </b-card-body>
                  </b-card>
                </swiper-slide>
                <b-icon icon="arrow-left" class="swiper-button-prev"></b-icon>
                <div class="swiper-pagination" slot="pagination"></div>
              </swiper>
            </client-only>-->
          </b-col>
        </b-row>
      </b-container>
    </section>
    <section>
      <b-container fluid>
        <b-row class="justify-content-center bg-white text-dark py-11">
          <b-col cols="11" md="7">
            <p class="h1 font-weight-bold">
              Our Interviewers are from
            </p>
          </b-col>
          <b-col cols="11" md="7">
            <div v-swiper:interviewerSwiper="interviewerSwiperOptions">
              <div class="swiper-wrapper d-flex align-items-center py-5">
                <div
                  class="text-center swiper-slide"
                  v-for="(interviewer, idx) in interviewers"
                  :key="idx"
                >
                  <b-img :src="interviewer" contain />
                </div>
              </div>
              <div class="interviewer-pagination"></div>
            </div>
          </b-col>
        </b-row>
      </b-container>
    </section>
    <section>
      <b-container fluid>
        <b-row class="justify-content-center bg-success-dark text-white py-11">
          <b-col cols="11" md="7">
            <p class="h1 font-weight-bold">
              Are you interested in becoming
              an Interviewer.
              <u>
                <span class="text-smiley-green">
                  Learn More
                </span>
              </u>
            </p>
          </b-col>
        </b-row>
      </b-container>
    </section>
    <section>
      <b-container fluid>
        <b-row class="justify-content-center bg-dark text-white py-5">
          <b-col cols="11" md="7">
            <div class="d-flex flex-column flex-md-row">
              <Logo dark_long class="mx-0" />
              <b-button variant="outline-light" class="ml-auto mr-auto mr-md-0 mt-5 mt-md-0">Get Started</b-button>
            </div>
          </b-col>
          <b-col cols="11" md="7">
            <div class="pt-5 font-weight-bold d-flex flex-column flex-md-row">
              <div class="mb-5 mb-md-0 d-flex flex-column flex-md-row text-center">
                <nuxt-link to="/" class="mr-0 mr-md-3 text-white">Home</nuxt-link>
                <nuxt-link to="/candidate" class="mr-0 mr-md-3 text-white">For Candidates</nuxt-link>
                <nuxt-link to="/interviewer" class="mr-0 mr-md-3 text-white">For Interviewers</nuxt-link>
                <nuxt-link to="/about" class="text-white">About</nuxt-link>
              </div>
              <div class="mr-auto mr-md-0 ml-auto">
                <a href="#" class="text-white mr-3">
                  <b-img height="25" width="25" contain src="~/static/icons/linkedin.svg" />
                </a>
                <a href="#" class="text-white">
                  <b-img height="25" width="25" contain src="~/static/icons/instagram.svg" />
                </a>
              </div>
            </div>
          </b-col>
        </b-row>
      </b-container>
    </section>
  </div>
</template>

<script>
// import { Swiper, SwiperSlide } from 'vue-awesome-swiper'
// import 'swiper/css/swiper.css'
import { directive } from 'vue-awesome-swiper'
import Logo from '~/components/Logo'

export default {
  auth: false,
  layout: 'landing-page',
  components: {
    Logo
    // Swiper,
    // SwiperSlide
  },
  directives: {
    swiper: directive
  },
  head: {
    link: [
      {
        rel: 'stylesheet',
        href: 'https://cdn.jsdelivr.net/npm/swiper@5.3.6/css/swiper.min.css'
      }
    ]
  },
  data () {
    return {
      swiperOptions: {
        slidesPerView: 2,
        spaceBetween: 30,
        loop: true,
        pagination: {
          el: '.swiper-pagination'
        }
      },
      interviewerSwiperOptions: {
        slidesPerView: 4,
        // spaceBetween: 30,
        loop: true,
        pagination: {
          el: '.interviewer-pagination'
        },
        // Responsive breakpoints
        breakpoints: {
          // when window width is >= 320px
          320: {
            slidesPerView: 2
          },
          // when window width is >= 640px
          640: {
            slidesPerView: 3
          },
          // when window width is >= 640px
          1000: {
            slidesPerView: 4
          }
        }
      },
      interviewers: [
        'https://cdn.zeplin.io/5ef9852ffe48f580cf1a311f/assets/84BA0E4C-1EC0-4ACC-882E-4F546C785A92.svg',
        'https://cdn.zeplin.io/5ef9852ffe48f580cf1a311f/assets/549F916E-F3B0-4DE6-854D-6C37CFF06E9F.svg',
        'https://cdn.zeplin.io/5ef9852ffe48f580cf1a311f/assets/C866AB01-2039-42FE-B1AA-C599C8EA0BC2.svg',
        'https://cdn.zeplin.io/5ef9852ffe48f580cf1a311f/assets/F65C7AC7-3C92-4460-82FE-86F6429EB3AB.svg',
        'https://cdn.zeplin.io/5ef9852ffe48f580cf1a311f/assets/6F3EF2EA-DC77-4ECD-8E7C-0AC1E35B1315.svg'
      ],
      testimonials: [
        {
          text: 'This is the best on-call interview experience. The technical interviewer gave me the luxury to keep coding while he was monitoring. This experience could not have been better!',
          user: 'Shreyash Singh',
          credibility: 'Placed in Indeed',
          user_dp: 'https://cdn.zeplin.io/5ef9852ffe48f580cf1a311f/assets/B1E33689-9D98-4582-BD58-B492BBAA5B3F.png'
        }, {
          text: 'The recruiter called me with an offer! I just wanted to drop you a quick line to tell you that interview Leap is probably the greatest idea for technical recruiting since sliced bread.',
          user: 'Shreyash Singh',
          credibility: 'Placed in Indeed',
          user_dp: 'https://cdn.zeplin.io/5ef9852ffe48f580cf1a311f/assets/1295A866-45C2-48B2-9E80-458C509B37D7.png'
        }
      ]
    }
  }
}
</script>

<style scoped>
.min-h-100 {
  min-height: 100vh;
}

.banner-img {
  width: 100%;
}

.mw-660 {
  max-width: 660px;
}
</style>
