<template>
    <div class="search-container-h1">
        <h1 class="search-h1">APWikipedia</h1>
        <SearchComponent />
    </div>
</template>

<script>
import SearchComponent from '../components/SearchComponent.vue';

export default {
    components: {
        SearchComponent,
    },
};
</script>

<style>
.search-container-h1 {
    position: absolute;
    top: 30%;
    left: 50%;
    transform: translate(-50%, -50%);
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
</style>