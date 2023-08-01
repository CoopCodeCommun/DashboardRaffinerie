<template>
  <div>
    <div @click="toggle" style="cursor: pointer;">
      <span>{{ isOpen ? '-' : '+' }}</span>
      {{ title }}
    </div>
    <div v-if="isOpen">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      isOpen: true
    }
  },
  methods: {
    toggle() {
      this.isOpen = !this.isOpen
    }
  }
}
</script>
