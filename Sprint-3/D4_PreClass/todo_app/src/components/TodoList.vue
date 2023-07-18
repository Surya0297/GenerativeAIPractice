<template>
    <div>
      <h1>Todo List</h1>
      <!-- Display the list of todos here -->
    </div>
  </template>
  
  <script>
import todos from '../data/todos';

export default {
  name: 'TodoList',
  data() {
    return {
      todos: todos
    };
  },
  methods: {
    markCompleted(todo) {
      todo.completed = !todo.completed;
    },
    deleteTodo(todo) {
      const index = this.todos.indexOf(todo);
      if (index !== -1) {
        this.todos.splice(index, 1);
      }
    }
  }
}
</script>

  
  <style scoped>
  /* Add your component-specific styles here */
  
  </style>
  