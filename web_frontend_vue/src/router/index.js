import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import ResultPage from '../views/ResultPage.vue';

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage
  },
  {
    path: '/result',
    name: 'ResultPage',
    component: ResultPage,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router
