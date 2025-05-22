<template>
  <div class="dashboard-page">
    <div class="dashboard-card">
      <div class="dashboard-header">
        <div
          style="
            display: flex;
            align-items: center;
            justify-content: space-between;
          "
        >
          <div
            style="display: flex; align-items: center; gap: var(--spacing-md)"
          >
            <Avatar icon="pi pi-user" size="large" />
            <div>
              <h1 class="dashboard-title">
                Welcome, {{ user?.username || "User" }}
              </h1>
              <p class="dashboard-subtitle">Here is your dashboard overview</p>
            </div>
          </div>
          <button class="logout-btn" @click="handleLogout">
            <i class="pi pi-sign-out" style="margin-right: 8px"></i> Logout
          </button>
        </div>
      </div>

      <div
        v-if="loading"
        style="
          display: flex;
          justify-content: center;
          align-items: center;
          min-height: 200px;
        "
      >
        <ProgressSpinner />
      </div>

      <div v-else>
        <div class="info-section">
          <h2
            style="
              margin-bottom: var(--spacing-lg);
              font-size: 1.25rem;
              color: var(--primary-color);
            "
          >
            User Information
          </h2>
          <div class="info-grid">
            <div class="info-item">
              <i class="pi pi-shield" style="color: var(--primary-color)"></i>
              <span class="info-label">Login Method:</span>
              <Tag
                :severity="
                  loginMethod === 'face recognition' ? 'info' : 'success'
                "
                class="tag"
              >
                {{ loginMethod }}
              </Tag>
            </div>
            <div class="info-item">
              <i class="pi pi-calendar" style="color: var(--primary-color)"></i>
              <span class="info-label">Last Login:</span>
              <span style="margin-left: var(--spacing-sm)">{{
                lastLogin
              }}</span>
            </div>
          </div>
        </div>

        <div class="recent-section">
          <h2
            style="
              margin-bottom: var(--spacing-lg);
              font-size: 1.25rem;
              color: var(--primary-color);
            "
          >
            Recent Activity
          </h2>
          <Timeline :value="recentActivity" class="timeline">
            <template #content="slotProps">
              <div
                style="
                  display: flex;
                  align-items: center;
                  gap: var(--spacing-sm);
                "
              >
                <i
                  :class="slotProps.item.icon"
                  style="color: var(--primary-color)"
                ></i>
                <span>{{ slotProps.item.text }}</span>
                <small class="text-color-secondary" style="margin-left: auto">{{
                  slotProps.item.date
                }}</small>
              </div>
            </template>
          </Timeline>
        </div>
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

const recentActivity = ref([
  {
    text: "Successfully logged in",
    date: new Date().toLocaleString(),
    icon: "pi pi-sign-in",
  },
  {
    text: "Profile updated",
    date: new Date(Date.now() - 24 * 60 * 60 * 1000).toLocaleString(),
    icon: "pi pi-user-edit",
  },
  {
    text: "Face recognition data updated",
    date: new Date(Date.now() - 48 * 60 * 60 * 1000).toLocaleString(),
    icon: "pi pi-camera",
  },
]);

onMounted(async () => {
  try {
    user.value = authStore.getUser();
    loginMethod.value = (
      user.value?.loginMethod || "credentials"
    ).toLowerCase();
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
/* Design System Variables */
:root {
  --primary-color: #1976d2;
  --primary-hover: #1565c0;
  --primary-light: #e3f2fd;
  --secondary-color: #757575;
  --error-color: #d32f2f;
  --error-light: #ffebee;
  --success-color: #388e3c;
  --background: #fafafa;
  --surface: #ffffff;
  --surface-card: #fff;
  --surface-ground: #f4f6fb;
  --surface-border: #e0e0e0;
  --text-primary: #212121;
  --text-secondary: #757575;
  --text-color-secondary: #b3b3b3;
  --shadow-1: 0 1px 3px rgba(0, 0, 0, 0.12);
  --shadow-2: 0 2px 8px rgba(0, 0, 0, 0.15);
  --shadow-3: 0 4px 16px rgba(0, 0, 0, 0.15);
  --radius-small: 4px;
  --radius-medium: 8px;
  --radius-large: 12px;
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-xxl: 40px;
}

.dashboard-page {
  width: 100vw;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-lg);
  box-sizing: border-box; /* Add this */
}

.dashboard-card {
  background: var(--surface);
  border-radius: var(--radius-large);
  box-shadow: var(--shadow-3);
  padding: var(--spacing-xxl);
  width: 100%;
  max-width: 1200px;
  min-height: 90vh;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s ease;
}

.dashboard-card:hover {
  transform: translateY(-2px);
}

.dashboard-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.dashboard-title {
  font-size: 2rem;
  font-weight: 400;
  color: var(--text-primary);
  margin: 0 0 var(--spacing-sm) 0;
  letter-spacing: -0.5px;
}

.dashboard-subtitle {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin: 0;
  font-weight: 400;
}

.info-section {
  margin-bottom: var(--spacing-xl);
  background: var(--background);
  border-radius: var(--radius-medium);
  box-shadow: var(--shadow-1);
  padding: var(--spacing-xl);
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-lg);
}

.info-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 1rem;
  color: var(--text-primary);
}

.info-label {
  font-weight: 500;
  color: var(--text-secondary);
}

.tag {
  margin-left: var(--spacing-sm);
}

.recent-section {
  background: var(--background);
  border-radius: var(--radius-medium);
  box-shadow: var(--shadow-1);
  padding: var(--spacing-xl);
}

.timeline {
  margin-top: var(--spacing-lg);
}

.logout-btn {
  background: transparent;
  color: var(--primary-color);
  border: 2px solid var(--primary-color);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-small);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: var(--primary-light);
}

@media (max-width: 900px) {
  .dashboard-card {
    max-width: 98vw;
    padding: var(--spacing-lg);
  }
  .info-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .dashboard-page {
    padding: var(--spacing-md);
  }
  .dashboard-card {
    padding: var(--spacing-lg);
  }
  .dashboard-title {
    font-size: 1.75rem;
  }
}

@media (prefers-color-scheme: dark) {
  :root {
    --background: #121212;
    --surface: #1e1e1e;
    --border-color: #333333;
    --text-primary: #ffffff;
    --text-secondary: #b3b3b3;
  }
  .dashboard-page {
    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  }
}
</style>
