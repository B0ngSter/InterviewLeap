<template>
  <div style="position:absolute; width: 90%">
    <b-input-group size="md" class="mb-2">
      <b-form-input
        v-model="selection"
        class="form-control bg-light"
        type="text"
        @keydown.enter="enter"
        @keydown.down="down"
        @keydown.up="up"
        @input="change"
        @blur="inputBlurred"
        @focus="open=true"
      />
      <b-input-group-prepend is-text>
        <b-icon icon="search" />
      </b-input-group-prepend>
    </b-input-group>
    <b-list-group style="position: relative; z-index: 1" :class="openSuggestion ? 'd-block' : 'd-none'">
      <b-list-group-item
        v-for="(suggestion, idx) in suggestions"
        :key="idx"
        :class="{'active': isActive(idx)}"
        button
        @click="suggestionClick(idx)"
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
