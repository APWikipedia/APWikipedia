<!-- Pagination.vue -->
<template>
    <nav aria-label="Page navigation">
        <ul class="pagination">
            <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">Previous</a>
            </li>
            <li class="page-item" v-for="page in totalPages" :key="page" :class="{ active: currentPage === page }">
                <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
            </li>
            <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <a class="page-link" href="#" @click.prevent="changePage(currentPage + 1)">Next</a>
            </li>
        </ul>
    </nav>
</template>

<script>
export default {
    props: {
        currentPage: Number,
        pageSize: Number,
        totalCount: Number
    },
    computed: {
        totalPages() {
            return Math.ceil(this.totalCount / this.pageSize);
        }
    },
    methods: {
        changePage(page) {
            if (page > 0 && page <= this.totalPages) {
                this.$emit('page-changed', page);
            }
            window.scrollTo(0, 0);
        }
    }
}
</script>

<style>
.pagination {
    list-style-type: none;
    display: flex;
    flex-direction: row;
    gap: 10px;
}

.page-link {
    color: #1e88e5;
}
</style>