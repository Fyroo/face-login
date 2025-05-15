<template>
  <div class="dashboard-container">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else class="dashboard-content">
      <div class="header">
        <h2>Welcome, {{ user?.username || "User" }}</h2>
        <button @click="handleLogout" class="logout-btn">Logout</button>
      </div>
      <div class="user-info">
        <p>Login method: {{ loginMethod }}</p>
        <p>Last login: {{ lastLogin }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { authStore } from "@/stores/auth";
import apiService from "@/services/api";

const router = useRouter();
const loading = ref(true);
const user = ref(null);
const loginMethod = ref("");
const lastLogin = ref(new Date().toLocaleString());

onMounted(async () => {
  try {
    user.value = authStore.getUser();
    loginMethod.value = user.value?.loginMethod || "Traditional";
    loading.value = false;
  } catch (error) {
    console.error("Error loading user data:", error);
    loading.value = false;
  }
});

const handleLogout = async () => {
  try {
    await apiService.logout();
    authStore.clearUser();
    router.push("/login");
  } catch (error) {
    console.error("Error during logout:", error);
  }
};
</script>

<style scoped>
.dashboard-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.loading {
  text-align: center;
  padding: 20px;
  font-size: 1.2em;
  color: #666;
}

.dashboard-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h2 {
  margin: 0;
  color: #2c3e50;
}

.logout-btn {
  padding: 8px 16px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.logout-btn:hover {
  background-color: #c82333;
}

.user-info {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
}

.user-info p {
  margin: 8px 0;
  color: #666;
}
</style>
