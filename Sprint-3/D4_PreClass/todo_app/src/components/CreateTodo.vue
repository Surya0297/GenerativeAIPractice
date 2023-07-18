<template>
  <div class="create-todo">
    <h2>Create Todo</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="title">Title:</label>
        <input type="text" id="title" v-model="newTodo.title" required>
      </div>
      <div class="form-group">
        <label for="description">Description:</label>
        <textarea id="description" v-model="newTodo.description" required></textarea>
      </div>
      <button type="submit">Create</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newTodo: {
        title: '',
        description: '',
      },
    };
  },
  methods: {
    handleSubmit() {
      // Check if todos is defined before accessing its length
      if (this.$router.currentRoute.value.meta.todos) {
        const todos = this.$router.currentRoute.value.meta.todos;
        todos.push(this.newTodo);

        // Reset newTodo properties after adding it to todos
        this.newTodo.title = '';
        this.newTodo.description = '';
      }
    },
  },
};
</script>

<style scoped>
.create-todo {
  max-width: 400px;
  margin: 0 auto;
}

h2 {
  text-align: center;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  background-color: #007bff;
  color: #fff;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
