<template>
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
</template>

<script>
// import { Swiper, SwiperSlide } from 'vue-awesome-swiper'
// import 'swiper/css/swiper.css'
import { directive } from 'vue-awesome-swiper'

export default {
  props: {
    testimonials: {
      type: Array
    }
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
        },
        // Responsive breakpoints
        breakpoints: {
          // when window width is >= 320px
          320: {
            slidesPerView: 1
          },
          // when window width is >= 800px
          800: {
            slidesPerView: 2
          }
        }
      }
    }
  }
}
</script>
