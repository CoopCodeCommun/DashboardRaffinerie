<template>
  <div>
    <!-- Default cell -->
    <div v-if="type === 'default'">
      {{ content }}
    </div>

    <!-- Text input cell -->
    <div v-else-if="type === 'text'">
      <input v-model="userInput" class="form-control case case_petite case_input" style="margin: 0;"/>
    </div>

    <!-- Dropdown cell -->
    <div v-else-if="type === 'dropdown'">
      <select v-model="userInput" class="form-control case case_petite case_input" style="margin: 0;">
        <option v-for="option in options" :key="option">{{ option }}</option>
      </select>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    type: {
      type: String,
      default: 'default',
    },
    content: {
      type: String,
      default: '',
    },
    options: {
      type: Array,
      default: () => [],
    },
    userInput: {
      type: String,
      default: '',
    },
  },
};
</script>
