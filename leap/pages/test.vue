<template>
  <b-container>
    <b-row>
      <p>{{ car }}</p>
      <!-- <hr> -->
      <!-- <div :class="{'text-primary': car === 'ford'}"> -->
      <!-- <p>IPU</p> -->
      <!-- <a :href="dsadas"></a> -->
      <!-- <img :src="gam" :alt="dsada"> -->
      <!-- </div> -->
      <!-- <hr> -->
      <p v-for="(billi, id) in games" :key="id">
        {{ id }}
      </p>
      <!-- <p v-show="sdajkhdkas">das</p> -->
      <p @click="mejshda">
        nitin
      </p>
      <!-- <input type="text" v> -->
      <!-- <input v-model="kuch" type="text"> -->
      <!-- <input v-if="car === 'fords'" type="text" placeholder="ford wala"> -->
      <!-- <input v-else type="text" placeholder="else wala"> -->
    </b-row>
  </b-container>
</template>

<script>
export default {
  data () {
    return {
      car: 'ford',
      kuch: '',
      games: ['cod4', 'cs1.6', 'pubg', 'http:dsadas/dsada'],
      games2: {}
    }
  },
  // created () {
  //   sdaahskjdhaksjn
  // },
  mounted () {
    this.$axios.get('dasds/').then((res) => {
      this.games = res.data
    })
  },
  methods: {
    car_start () {
      this.car = 'BMW'
    },
    mejshda () {
      this.car = 'bmw'
    }
  }
}
</script>

<style>
  .selected {
    color: red
  }
</style>
