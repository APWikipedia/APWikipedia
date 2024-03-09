<template>
    <div class="search-results-container">
        <div class="search-container-h3">
            <h3 @click="goToHomePage" class="search-h3">APWikipedia</h3>
            <SearchComponent />
        </div>
        <div v-if="searchResults.length > 0" class="results-container">
            <div v-if="searchTime !== null" class="search-time">Search Time: {{ searchTime }} ms</div>
            <div v-for="result in searchResults" :key="result.url" class="search-result">
                <h3><a :href="result.url" target="_blank" class="result-link">{{ result.title }}</a></h3>
                <p class="result-summary">{{ result.summary }}</p>
            </div>
        </div>
        <div v-else-if="searched" class="no-results">No results found.</div>
    </div>
</template>

<script>
import SearchComponent from '../components/SearchComponent.vue';

export default {
    data() {
        return {
            searchQuery: '',
            searchResults: [],
            searchTime: null,
            searched: false, // 用于跟踪是否已经进行了搜索
        };
    },
    components: {
        SearchComponent,
    },
    watch: {
        '$route.query.q': {
            immediate: true,
            handler() {
                this.searchStepTwo();
            },
        },
    },
    methods: {
        async searchStepTwo() {
            this.searchQuery = this.$route.query.q;

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
            } finally {
                this.searched = true;
            }
        },
        goToHomePage() {
            this.$router.push({name: 'HomePage'});
        }
    },
};
</script>

<style>
.search-results-container {
    position: absolute;
    top: 20px;
    left: 15px;
}

.search-container-h3 {
    display: flex;
    align-items: center;
    /* margin-top: -40px; */
}

.search-h3 {
    font-family: Georgia, serif;
    font-size: 22px;
    color: transparent;
    background: rgb(7, 5, 26);
    -webkit-background-clip: text;
    -moz-background-clip: text;
    background-clip: text;
    text-shadow: 0px 3px 3px rgba(255, 255, 255, 0.5);
    margin-right: 10px;
    cursor: pointer;
}

.results-container {
    text-align: left;
    margin-top: 5px;
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
    font-size: 12px;
    margin-top: 0px;
    margin-bottom: 0px;
}

.no-results {
    margin-top: 20px;
}
</style>