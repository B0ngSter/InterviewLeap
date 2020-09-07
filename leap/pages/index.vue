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
    <TestimonialSection :testimonials="testimonials" />
    <InterviewerPedigreeShowcase />
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
    <FooterSection />
  </div>
</template>

<script>
import TestimonialSection from '~/components/TestimonialSection'
import InterviewerPedigreeShowcase from '~/components/InterviewerPedigreeShowcase'
import FooterSection from '~/components/FooterSection'

export default {
  auth: false,
  layout: 'landing-page',
  components: {
    TestimonialSection,
    InterviewerPedigreeShowcase,
    FooterSection
  },
  data () {
    return {
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
