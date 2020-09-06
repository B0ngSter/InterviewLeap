<template>
  <div style="position:absolute; width: 100%">
    <input
      class="form-control"
      type="text"
      v-model="selection"
      @keydown.enter='enter'
      @keydown.down='down'
      @keydown.up='up'
      @input='change'
      @blur="inputBlurred"
      @focus="open=true"
    />
    <b-list-group style="position: relative; z-index: 1" v-bind:class="openSuggestion ? 'd-block' : 'd-none'">
      <b-list-group-item
        v-for="(suggestion, idx) in suggestions"
        :key="idx"
        v-bind:class="{'active': isActive(idx)}"
        @click="suggestionClick(idx)"
        button
      >
        {{ itemTitleKey ? suggestion[itemTitleKey] : suggestion }}
      </b-list-group-item>
    </b-list-group>
  </div>
</template>

<script>
export default {
  props: {
    searchParamName: {
      type: String,
      default: 'query'
    },
    searchEndpoint: {
      type: String,
      default: ''
    },
    searchDebounce: {
      type: Number,
      default: 200
    },
    resultKey: {
      default: false
    },
    itemTitleKey: {
      default: false
    }
  },
  data: () => {
    return {
      open: false,
      current: 0,
      suggestions: [],
      selection: ''
    }
  },
  computed: {
    // Filtering the suggestion based on the input
    /* matches () {
      return this.suggestions.filter((str) => {
        return str.includes(this.selection)
      })
    }, */

    // The flag
    openSuggestion () {
      return this.selection !== '' &&
        this.suggestions.length !== 0 &&
        this.open === true
    }
  },
  methods: {
    inputBlurred () {
      window.setTimeout(function () {
        this.open = false
      }.bind(this), 100)
    },
    // When enter pressed on the input
    enter () {
      this.suggestionClick(this.current)
      // this.selection = this.suggestions[this.current]
      // this.open = false
    },

    // When up pressed while suggestions are open
    up () {
      if (this.current > 0) {
        this.current--
      }
    },

    // When up pressed while suggestions are open
    down () {
      if (this.current < this.suggestions.length - 1) {
        this.current++
      }
    },

    // For highlighting element
    isActive (index) {
      return index === this.current
    },

    // When the user changes input
    change ($event) {
      this._perform_keyword_search($event.target.value)
      if (this.open === false) {
        this.open = true
        this.current = 0
      }
    },

    _perform_keyword_search (searchQuery) {
      this.$axios.get(`${this.searchEndpoint}?${this.searchParamName}=${searchQuery}`)
        .then((response) => {
          this.suggestions = this.resultKey ? response.data[this.resultKey] : response.data
        })
    },

    // When one of the suggestion is clicked
    suggestionClick (index) {
      debugger
      this.selection = this.itemTitleKey ? this.suggestions[index][this.itemTitleKey] : this.suggestions[index]
      this.$emit('select', this.suggestions[index])
      this.open = false
    }
  }
}
</script>
