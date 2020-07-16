<template>
  <b-container class="align-items-start">
    <b-row align-v="start" align-content="start">
      <b-col cols="12">
        <h1>Testing page</h1>
        <b-btn variant="danger">
          Reschedule
        </b-btn>
        <b-btn variant="primary">
          Decline
        </b-btn>
        <b-btn variant="danger">
          Error
        </b-btn>
        <b-btn variant="info">
          Accept
        </b-btn>
        <b-btn variant="success">
          Book
        </b-btn>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  layout: 'app-page'
}
</script>
