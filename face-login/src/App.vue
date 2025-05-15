<script setup>
import { useRoute } from "vue-router";

const route = useRoute();
</script>

<template>
  <div class="app-container">
    <header>
      <h1>Face Recognition Authentication</h1>
      <div class="nav-buttons">
        <router-link to="/login" custom v-slot="{ navigate, isActive }">
          <button :class="['nav-btn', { active: isActive }]" @click="navigate">
            Login
          </button>
        </router-link>

        <router-link to="/register" custom v-slot="{ navigate, isActive }">
          <button :class="['nav-btn', { active: isActive }]" @click="navigate">
            Register
          </button>
        </router-link>
      </div>
    </header>

    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<style scoped>
.app-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

header {
  text-align: center;
  margin-bottom: 30px;
}

h1 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.nav-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 30px;
}

.nav-btn {
  padding: 10px 30px;
  border: 2px solid #4caf50;
  background-color: white;
  color: #4caf50;
  cursor: pointer;
  border-radius: 4px;
  font-size: 1.1em;
  transition: all 0.3s ease;
}

.nav-btn.active {
  background-color: #4caf50;
  color: white;
}

.nav-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(76, 175, 80, 0.2);
}

main {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 30px;
}
</style>
