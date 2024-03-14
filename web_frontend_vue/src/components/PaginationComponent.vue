<template>
    <nav aria-label="Page navigation">
        <ul class="pagination">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">Previous</a>
            </li>
            <li class="page-item" v-for="page in pagesToShow" :key="page" :class="{ active: currentPage === page }">
                <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">Next</a>
            </li>
            <li class="page-jump">
                <input type="number" v-model="jumpPage" @keyup.enter="jumpToPage" placeholder="Jump to page" min="1"
                    :max="totalPages" />
                <button @click="jumpToPage">Go</button>
            </li>
        </ul>
    </nav>

</template>

<script>
export default {
    data() {
        return {
            jumpPage: null,
        };
    },
    props: {
        currentPage: Number,
        pageSize: Number,
        totalCount: Number,
    },
    computed: {
        totalPages() {
            return Math.ceil(this.totalCount / this.pageSize);
        },
        pagesToShow() {
            let startPage = Math.max(this.currentPage - 4, 1);
            let endPage = Math.min(startPage + 9, this.totalPages);
            if (endPage - startPage < 9) {
                startPage = Math.max(1, endPage - 9);
            }
            return Array.from({ length: endPage - startPage + 1 }, (_, i) => startPage + i);
        },
    },
    methods: {
        changePage(page) {
            if (page > 0 && page <= this.totalPages) {
                this.$emit('page-changed', page);
                window.scrollTo(0, 0);
            }
        },
        jumpToPage() {
            const page = Math.min(Math.max(parseInt(this.jumpPage), 1), this.totalPages);
            if (!isNaN(page)) {
                this.changePage(page);
                this.jumpPage = null; 
            }
        },
    },
}
</script>

<style>
.pagination {
    list-style-type: none;
    display: flex;
    flex-direction: row;
    gap: 10px;
    padding: 0;
    margin: 20px 0;
}

.page-item {
    border: 1px solid #ddd;
    border-radius: 5px;
    overflow: hidden;
}

.page-link {
    display: block;
    padding: 8px 16px;
    color: #2c3e50;
    text-decoration: none;
    background-color: #f8f9fa;
    transition: all 0.3s ease;
}

.page-link:hover,
.page-link:focus {
    background-color: #e9ecef;
    color: #2c3e50;
}

.active .page-link {
    color: #ffffff;
    background-color: #2c3e50;
    border-color: #2c3e50;
}

.disabled .page-link {
    color: #6c757d;
    pointer-events: none;
    background-color: #f8f9fa;
}

.page-jump {
    display: flex;
    gap: 5px;
    align-items: center;
}

.page-jump input {
    padding: 8px;
    /* font-size: 12px; */
    /* line-height: 20px; */
    width: 120px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

.page-jump button {
    padding: 8px 16px;
    /* font-size: 12px; */
    background-color: #2c3e50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.page-jump button:hover {
    background-color: #2c3e50;
}
</style>