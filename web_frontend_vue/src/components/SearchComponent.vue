<template>
  <div class="search-container">
    <!-- <h1 class="search-h1" v-show="!searched">APWikipedia</h1> -->
    <h1 class="search-h1">APWikipedia</h1>
    <!-- <div :class="['search-box', searched ? 'top-left-search-box' : 'centered-search-box']"> -->
      <!-- <h3 class="search-h3" v-show="searched">APWikipedia</h3> -->
      <input v-model="searchQuery" @keyup.enter="search" placeholder="Enter the search query..." class="search-input" />
      <button @click="search" class="search-button">Search</button>
    <!-- </div> -->
    <div v-if="searchResults.length > 0" class="results-container">
      <div v-for="result in searchResults" :key="result.url" class="search-result">
        <h3><a :href="result.url" target="_blank" class="result-link">{{ result.title }}</a></h3>
        <p class="result-summary">{{ result.summary }}</p>
      </div>
      <div v-if="searchTime !== null" class="search-time">Search Time: {{ searchTime }} ms</div>
    </div>
    <div v-if="searchResults.length === 0 && searched" class="no-results">No results found.</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
      searchResults: [],
      searchTime: null,
      searched: false, // 用于跟踪是否已经进行了搜索
    };
  },
  methods: {
    async search() {
      this.searched = true; // 用户点击搜索，更新状态
      if (this.searchQuery.trim() === '') {
        alert('The search query cannot be empty');
        return;
      }

      const requestOptions = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: this.searchQuery }),
      };

      try {
        const response = await fetch('http://127.0.0.1:5000/ranked_search', requestOptions);
        const data = await response.json();
        this.searchResults = data.results || [];
        this.searchTime = data['search_time(Ms)'] || null;
      } catch (error) {
        console.error("Request Error:", error);
        this.searchResults = [];
      }
    },
  },
};
</script>

<style>
.search-container {
  text-align: center;
  margin-top: 20px;
}

.search-h1 {
  font-family: Georgia, serif;
  font-size: 50px;
  color: transparent;
  background: rgb(7, 5, 26);
  -webkit-background-clip: text;
  -moz-background-clip: text;
  background-clip: text;
  text-shadow: 0px 3px 3px rgba(255, 255, 255, 0.5);
}

/* .search-h3 {
  font-family: Georgia, serif;
  font-size: 20px;
  color: transparent;
  background: rgb(7, 5, 26);
  -webkit-background-clip: text;
  -moz-background-clip: text;
  background-clip: text;
  text-shadow: 0px 3px 3px rgba(255, 255, 255, 0.5);
  margin-right: 10px;
} */

/* .centered-search-box {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
}

.top-left-search-box {
  position: absolute;
  top: 10%;
  left: 10%;
  transform: translate(-10%, -10%);
  display: flex;
  align-items: center;
} */

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

.results-container {
  text-align: left;
  margin-top: 20px;
  /* margin-top: 20vh; */
}

.search-result {
  /* border-bottom: 1px solid #eee; */
  padding: 10px 0;
}

.result-title {
  color: #2c3e50;
  margin: 0;
}

.result-summary {
  color: #666;
  font-size: 14px;
}

.result-link {
  color: #1e88e5;
  text-decoration: none;
}

.search-time {
  margin-top: 10px;
  margin-bottom: 10px;
}

.no-results {
  margin-top: 20px;
}
</style>