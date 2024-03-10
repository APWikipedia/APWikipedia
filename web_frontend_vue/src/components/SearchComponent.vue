<template>
  <div>
    <input v-model="searchQuery" @keyup.enter="searchStepOne" placeholder="Enter the search query..."
      class="search-input" />
    <button @click="searchStepOne" class="search-button">Search</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
    };
  },
  methods: {
    searchStepOne() {
      if (this.searchQuery.trim() === '') {
        alert('The search query cannot be empty');
        return;
      }

      this.$router.push({ name: 'ResultPage', query: { q: this.searchQuery } });
    },
  },
};
</script>

<style>
.search-input {
  width: 300px;
  padding: 10px;
  margin-right: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.search-button {
  padding: 10px 20px;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.search-button:hover {
  background-color: #455a64;
}
</style>