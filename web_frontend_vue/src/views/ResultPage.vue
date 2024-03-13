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
            <!-- <PaginationComponent :currentPage="currentPage" :pageSize="pageSize" :totalCount="searchResults.length"
                    @page-changed="handlePageChange" /> -->
            <PaginationComponent :currentPage="currentPage" :pageSize="pageSize" :totalCount=50
                @page-changed="handlePageChange" />
        </div>
        <div v-else-if="searched" class="no-results">No results found.</div>
    </div>
</template>

<script>
import SearchComponent from '../components/SearchComponent.vue';
import PaginationComponent from '../components/PaginationComponent.vue';

export default {
    data() {
        return {
            searchQuery: '',
            searchResults: [],
            searchTime: null,
            searched: false,
            currentPage: 1,
            pageSize: 10,
            isAdvancedSearchActive: false, // 默认情况下高级搜索不激活
        };
    },
    components: {
        SearchComponent,
        PaginationComponent,
    },
    computed: {
        searchURL() {
            return this.isAdvancedSearchActive ? 'http://127.0.0.1:5000/search' : 'http://127.0.0.1:5000/ranked_search';
        },
    },
    watch: {
        '$route.query': {
            immediate: true,
            handler(query) {
                this.isAdvancedSearchActive = query.advanced === '1';
                this.searchQuery = query.q;
                this.searchStepTwo();
            },
        },
    },
    // computed: {
    //     currentItems() {
    //         const start = (this.currentPage - 1) * this.pageSize;
    //         const end = start + this.pageSize;
    //         return this.items.slice(start, end);
    //     }
    // },
    methods: {
        async searchStepTwo() {
            // this.searchQuery = this.$route.query.q;
            const requestOptions = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: this.searchQuery,
                    page_number: this.currentPage,
                    page_size: this.pageSize
                }),
            };
            try {
                const response = await fetch(this.searchURL, requestOptions);
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
            this.$router.push({ name: 'HomePage' });
        },
        handlePageChange(newPage) {
            this.currentPage = newPage;
            this.searchStepTwo();
        },
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
    justify-content: center;
    align-items: center;
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
    padding-bottom: 10px;
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