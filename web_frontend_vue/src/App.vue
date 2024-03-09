<template>
  <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
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
</style>
