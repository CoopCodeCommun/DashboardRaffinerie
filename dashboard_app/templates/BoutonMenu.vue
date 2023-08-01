<template>
  <div style="position: relative; display: inline-block;">
    <button class="bleu case style_input case_clair" @click="toggleDropdown">{{ selectedOption || buttonText }}</button>
    <div v-if="isDropdownOpen" class="dropdown case bleu p-2 g-2" style="position: absolute; top: 110%; right: 100;">
      <ul>
        <li v-for="(option, index) in options" :key="index" @click="selectOption(option)">{{ option }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  props: ['options'],  // Ajouté ici
  data() {
    return {
      buttonText: 'Groupe / pôle / projet',
      isDropdownOpen: false,
      selectedOption: null,
    };
  },
  methods: {
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    selectOption(option) {
      this.selectedOption = option;
      this.isDropdownOpen = false;
    },
  },
};
</script>