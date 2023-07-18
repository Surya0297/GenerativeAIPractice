<template>
  <div id="app">
    <router-view :todos="todos" @toggle-completed="markCompleted" @delete-todo="deleteTodo"></router-view>

  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      todos: []
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


<style>
#app {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 10px;
}

button {
  margin-right: 10px;
}
</style>

