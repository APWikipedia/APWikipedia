<template>
    <div class="search-container">
      <input
        v-model="searchQuery"
        @keyup.enter="search"
        placeholder="请输入搜索内容..."
        class="search-input"
      />
      <button @click="search" class="search-button">搜索</button>
      <div v-if="searchResults.length > 0" class="results-container">
        <div v-for="result in searchResults" :key="result.url" class="search-result">
          <h3 class="result-title">{{ result.title }}</h3>
          <p class="result-summary">{{ result.summary }}</p>
          <a :href="result.url" target="_blank" class="result-link">阅读更多</a>
        </div>
      </div>
      <div v-if="searchTime !== null" class="search-time">搜索耗时：{{ searchTime }}毫秒</div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const searchQuery = ref('');
  const searchResults = ref([]);
  const searchTime = ref(null);
  
const search = async () => {
  if (searchQuery.value.trim() === '') {
    alert('请输入搜索关键词');
    return;
  }

  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query: searchQuery.value })
  };

  try {
    const response = await fetch('http://127.0.0.1:5000/ranked_search', requestOptions);
    const data = await response.json();
    searchResults.value = data.results || [];
    searchTime.value = data['search_time(Ms)'] || null;
  } catch (error) {
    console.error("搜索请求失败:", error);
    searchResults.value = [];
  }
};

  </script>
  
  <style>
  .search-container {
    text-align: center;
    margin-top: 20px;
  }
  
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
    margin-top: 20px;
  }
  
  .search-result {
    border-bottom: 1px solid #eee;
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
  </style>
  