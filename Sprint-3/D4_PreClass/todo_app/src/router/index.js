import { createRouter, createWebHistory } from 'vue-router';
import TodoList from '../components/TodoList.vue';
import CreateTodo from '../components/CreateTodo.vue';

const routes = [
  {
    path: '/todos',
    component: TodoList,
  },
  {
    path: '/create',
    component: CreateTodo,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
