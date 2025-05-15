import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api";

const apiService = {
  async register(username, password, faceImage) {
    try {
      const response = await axios.post(`${API_URL}/register/`, {
        username,
        password,
        face_image: faceImage,
      });
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || "Registration failed",
      };
    }
  },

  async loginWithCredentials(username, password) {
    try {
      const response = await axios.post(`${API_URL}/login/`, {
        username,
        password,
      });
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || "Login failed",
      };
    }
  },

  async loginWithFace(faceImage) {
    try {
      const response = await axios.post(`${API_URL}/login/face/`, {
        face_image: faceImage,
      });
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || "Face login failed",
      };
    }
  },
  async logout() {
    try {
      const response = await axios.post(`${API_URL}/logout/`);
      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || "Logout failed",
      };
    }
  },
};

export default apiService;
