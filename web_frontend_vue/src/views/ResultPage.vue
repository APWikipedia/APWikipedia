<template>
    <div class="search-results-container" ref="searchResultsContainer">
        <div class="search-container-h3" ref="searchContainerH3">
            <h3 @click="goToHomePage" class="search-h3">APWikipedia</h3>
            <SearchComponent @search-initiated="handleSearchInitiated" />
        </div>
        <!-- <hr class="custom-hr" /> -->
        <div v-if="searchResults.length > 0" class="results-container">
            <div v-if="searchTime !== null && searchLength !== null" class="search-time">{{ searchLength}} results ({{ searchTime }} ms) </div>
            <div v-for="result in searchResults" :key="result.url" class="search-result">
                <h3><a :href="result.url" target="_blank" class="result-link">{{ result.title }}</a></h3>
                <p class="result-summary">{{ result.summary }}</p>
                <small>Tags: <span v-for="tag in result.tags" :key="tag"
                        :style="{ 'background-color': getTagColor(tag), color: '#fff' }" class="result-tag">{{ tag
                        }}</span></small>
            </div>
            <PaginationComponent :currentPage="currentPage" :pageSize="pageSize" :totalCount="searchLength"
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
            searchLength: 0,
            searched: false,
            currentPage: 1,
            pageSize: 10,
            isAdvancedSearchActive: false,
            tagColorCache: {},
            baseHue: 0,
            hueIncrement: 25,
            colorIndex: 0,
        };
    },
    components: {
        SearchComponent,
        PaginationComponent,
    },
    computed: {
        searchURL() {
            return this.isAdvancedSearchActive ? 'http://34.142.98.9:5000/search' : 'http://34.142.98.9:5000/ranked_search';
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
    mounted() {
        this.adjustPaddingTop();
        window.addEventListener('resize', this.adjustPaddingTop);
    },
    beforeUnmount() {
        window.removeEventListener('resize', this.adjustPaddingTop);
    },
    methods: {
        async searchStepTwo() {
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
                this.searchLength = data['total length'] || 0;
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
        getTagColor(tag) {
            if (!this.tagColorCache[tag]) {
                const colors = [
                    { hue: (0 + 137 * this.colorIndex) % 360, saturation: 70, lightness: 60 },
                    { hue: (55 + 137 * this.colorIndex) % 360, saturation: 55, lightness: 50 },
                    { hue: (120 + 137 * this.colorIndex) % 360, saturation: 45, lightness: 70 },
                ];
                const color = colors[this.colorIndex % colors.length];
                const hsl = `hsl(${color.hue}, ${color.saturation}%, ${color.lightness}%)`;
                this.tagColorCache[tag] = hsl;
                this.colorIndex++;
            }
            return this.tagColorCache[tag];
        },
        handleSearchInitiated(page) {
            this.currentPage = page;
            this.searchStepTwo();
        },
        adjustPaddingTop() {
            const searchContainer = this.$refs.searchContainerH3;
            if (searchContainer) {
                const height = searchContainer.offsetHeight;
                const searchResultsContainer = this.$refs.searchResultsContainer;
                if (searchResultsContainer) {
                    searchResultsContainer.style.paddingTop = `${height}px`;
                }
            }
        }
    },
};
</script>

<style>
.result-tag {
    padding: 5px 10px;
    margin-right: 5px;
    border: 1px solid #DADCE0;
    border-radius: 5px;
    color: black;
    display: inline-block;
    margin-bottom: 5px;
    font-weight: bold;
}

.custom-hr {
    border: 0;
    height: 1px;
    width: 100%;
    background-color: #DADCE0;
    margin-top: 10px;
    margin-bottom: 10px;
}

.search-results-container {
    position: absolute;
    top: 20px;
    left: 15px;
}

.search-container-h3 {
    display: flex;
    justify-content: start;
    align-items: center;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    padding-left: 15px;
    padding-top: 20px;
    z-index: 1000;
    background-color: white;
    border-bottom: 1px solid #ccc;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
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
    font-size: 23px;
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
