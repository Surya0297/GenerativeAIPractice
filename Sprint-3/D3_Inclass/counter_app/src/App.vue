<template>
  <div class="counter-container">
    <h1>Counter Application</h1>
    <p class="count-display">Count: {{ count }}</p>
    <button class="button" @click="increment">Increment</button>
    <button class="button" @click="decrement">Decrement</button>
  </div>
</template>



<script>
export default {
  data() {
    return {
      count: 0
    };
  },
  methods: {
    increment() {
      this.count++;
    },
    decrement() {
      if (this.count > 0) {
        this.count--;
      }
    }
  }
};
</script>

<style>
  .counter-container {
    text-align: center;
    background-color:#b8e1ff;
    height:100vh;
    
  }


  .count-display {
    font-size: 24px;
    margin-bottom: 20px;
  }

  .button {
    padding: 10px 20px;
    font-size: 16px;
    background-color: #82aba1;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-right: 10px;
  }

  .button:hover {
    background-color: #bcb6ff;
  }
</style>
