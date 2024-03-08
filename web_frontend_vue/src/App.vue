<template>
  <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
  <h1 id="h1" class="search-h1">APWikipedia</h1>
  <!-- 使用 SearchComponent 组件 -->
  <search-component></search-component>
</template>


<script>
import SearchComponent from './components/SearchComponent.vue';

export default {
  name: 'App',
  components: {
    SearchComponent
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
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
