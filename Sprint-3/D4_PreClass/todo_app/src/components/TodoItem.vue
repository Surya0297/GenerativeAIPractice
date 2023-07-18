<template>
    <div>
      <h3>{{ todo.title }}</h3>
      <p>{{ todo.description }}</p>
      <button @click="toggleCompleted">{{ todo.completed ? 'Mark Incomplete' : 'Mark Complete' }}</button>
      <button @click="deleteTodo">Delete</button>
    </div>
  </template>
  
  
  <script>
  export default {
    name: 'TodoItem',
    props: ['todo'],
    methods: {
      toggleCompleted() {
        this.$emit('toggle-completed', this.todo);
      },
      deleteTodo() {
        this.$emit('delete-todo', this.todo);
      }
    }
  }
  </script>
  
  
  <style scoped>
button {
  background-color: #e53935;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>

  