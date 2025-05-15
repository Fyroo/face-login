// Simple auth state management
const authState = {
  user: JSON.parse(localStorage.getItem("user") || "null"),
  isAuthenticated: false,
};

export const authStore = {
  getUser() {
    return authState.user;
  },

  isAuthenticated() {
    return !!authState.user;
  },

  setUser(userData) {
    authState.user = userData;
    authState.isAuthenticated = true;
    localStorage.setItem("user", JSON.stringify(userData));
  },

  clearUser() {
    authState.user = null;
    authState.isAuthenticated = false;
    localStorage.removeItem("user");
  },
};
