<template>
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
</template>

<script>
import { directive } from 'vue-awesome-swiper'

export default {
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
            slidesPerView: 1
          },
          // when window width is >= 640px
          640: {
            slidesPerView: 3
          },
          // when window width is >= 1000px
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
      ]
    }
  }
}
</script>
