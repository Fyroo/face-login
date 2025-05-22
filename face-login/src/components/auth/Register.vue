<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1 class="login-title">Register</h1>
        <p class="login-subtitle">Create your account</p>
      </div>

      <div v-if="errorMessage" class="error-message">
        <svg class="error-icon" viewBox="0 0 24 24" fill="currentColor">
          <path
            d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"
          />
        </svg>
        {{ errorMessage }}
      </div>

      <div class="login-methods">
        <button
          :class="['method-tab', { active: registerMethod === 'credentials' }]"
          @click="switchMethod('credentials')"
        >
          <svg class="method-icon" viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 1V3H9V1L3 7V9H21ZM12 8C13.66 8 15 9.34 15 11V12H21V20C21 21.1 20.1 22 19 22H5C3.9 22 3 21.1 3 20V12H9V11C9 9.34 10.34 8 12 8Z"
            />
          </svg>
          Email & Password
        </button>
        <button
          :class="['method-tab', { active: registerMethod === 'face' }]"
          @click="switchMethod('face')"
        >
          <svg class="method-icon" viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M9,11H7V13H9V11M13,11H11V13H13V11M17,11H15V13H17V11M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"
            />
          </svg>
          Face Registration
        </button>
      </div>

      <!-- Credentials Registration Form -->
      <form
        v-if="registerMethod === 'credentials'"
        @submit.prevent="handleRegister"
        class="login-form"
      >
        <div class="input-group">
          <label for="username" class="input-label">Username</label>
          <input
            type="text"
            id="username"
            v-model="username"
            required
            class="input-field"
            placeholder="Enter your username"
          />
        </div>
        <div class="input-group">
          <label for="password" class="input-label">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            required
            class="input-field"
            placeholder="Enter your password"
          />
        </div>
        <button type="submit" class="primary-button" :disabled="isLoading">
          <span v-if="isLoading" class="loading-spinner"></span>
          {{ isLoading ? "Registering..." : "Register" }}
        </button>
      </form>

      <!-- Face Registration -->
      <div v-else class="face-login">
        <div class="face-input-selector">
          <button
            :class="[
              'input-method-btn',
              { active: faceInputMethod === 'webcam' },
            ]"
            @click="switchFaceInput('webcam')"
          >
            <svg class="method-icon" viewBox="0 0 24 24" fill="currentColor">
              <path
                d="M17,10.5V7A1,1 0 0,0 16,6H4A1,1 0 0,0 3,7V17A1,1 0 0,0 4,18H16A1,1 0 0,0 17,17V13.5L21,17.5V6.5L17,10.5Z"
              />
            </svg>
            Use Camera
          </button>
          <button
            :class="[
              'input-method-btn',
              { active: faceInputMethod === 'upload' },
            ]"
            @click="switchFaceInput('upload')"
          >
            <svg class="method-icon" viewBox="0 0 24 24" fill="currentColor">
              <path
                d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"
              />
            </svg>
            Upload Photo
          </button>
        </div>

        <form @submit.prevent="handleRegister" class="login-form">
          <div v-if="faceInputMethod === 'webcam'" class="webcam-section">
            <div v-if="webcamError" class="error-message">
              {{ webcamError }}
            </div>
            <div class="camera-container">
              <video
                v-show="!capturedImage"
                ref="video"
                class="video-feed"
                autoplay
                muted
              ></video>
              <div v-if="!capturedImage" class="camera-overlay">
                <div class="face-guide"></div>
              </div>
            </div>
            <button
              v-if="!capturedImage"
              type="button"
              @click="captureImage"
              class="capture-button"
            >
              <svg class="capture-icon" viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M12,15A2,2 0 0,1 14,17A2,2 0 0,1 12,19A2,2 0 0,1 10,17A2,2 0 0,1 12,15M12,9A8,8 0 0,1 20,17A8,8 0 0,1 12,25A8,8 0 0,1 4,17A8,8 0 0,1 12,9Z"
                />
              </svg>
              Capture Photo
            </button>
          </div>

          <div v-else class="upload-section">
            <input
              type="file"
              ref="fileInput"
              @change="handleFileUpload"
              accept="image/*"
              class="file-input"
            />
            <div
              class="upload-area"
              v-if="!capturedImage"
              @click="triggerFileInput"
            >
              <svg class="upload-icon" viewBox="0 0 24 24" fill="currentColor">
                <path
                  d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"
                />
              </svg>
              <h3 class="upload-title">Choose a photo</h3>
              <p class="upload-description">
                Select a clear photo of your face
              </p>
              <span class="upload-formats">JPG, PNG up to 10MB</span>
            </div>
          </div>

          <div v-if="capturedImage" class="captured-preview">
            <div class="preview-container">
              <img
                :src="capturedImage"
                alt="Face preview"
                class="preview-image"
              />
              <div class="preview-overlay">
                <button
                  type="button"
                  @click="retakeImage"
                  class="secondary-button"
                >
                  {{
                    faceInputMethod === "webcam"
                      ? "Retake Photo"
                      : "Choose Another"
                  }}
                </button>
              </div>
            </div>
            <div class="input-group">
              <label for="username" class="input-label">Username</label>
              <input
                type="text"
                id="username"
                v-model="username"
                required
                class="input-field"
                placeholder="Enter your username"
              />
            </div>
            <div class="input-group">
              <label for="password" class="input-label">Password</label>
              <input
                type="password"
                id="password"
                v-model="password"
                required
                class="input-field"
                placeholder="Enter your password"
              />
            </div>
            <button
              type="submit"
              class="primary-button"
              :disabled="!username || !password || !capturedImage || isLoading"
            >
              <span v-if="isLoading" class="loading-spinner"></span>
              {{ isLoading ? "Registering..." : "Register" }}
            </button>
          </div>
        </form>
      </div>

      <div class="switch-auth-link">
        <span>Already have an account?</span>
        <router-link to="/login" class="switch-link">Sign in</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import apiService from "@/services/api";
import { useRouter } from "vue-router";

const router = useRouter();
const registerMethod = ref("credentials");
const faceInputMethod = ref("webcam");
const username = ref("");
const password = ref("");
const video = ref(null);
const capturedImage = ref(null);
const stream = ref(null);
const errorMessage = ref("");
const isLoading = ref(false);
const webcamError = ref(null);
const fileInput = ref(null);

onMounted(async () => {
  if (registerMethod.value === "face") {
    await initializeWebcam();
  }
});

onUnmounted(() => {
  stopWebcam();
});

const switchMethod = async (method) => {
  registerMethod.value = method;
  errorMessage.value = "";
  capturedImage.value = null;
  if (method === "face") {
    await initializeWebcam();
  } else {
    stopWebcam();
  }
};

const switchFaceInput = (method) => {
  faceInputMethod.value = method;
  capturedImage.value = null;
  if (method === "webcam") {
    initializeWebcam();
  } else {
    stopWebcam();
  }
};

const initializeWebcam = async () => {
  try {
    webcamError.value = null;
    stream.value = await navigator.mediaDevices.getUserMedia({
      video: {
        width: { ideal: 640 },
        height: { ideal: 480 },
        facingMode: "user",
      },
    });
    if (video.value) {
      video.value.srcObject = stream.value;
    }
  } catch (err) {
    console.error("Error accessing webcam:", err);
    webcamError.value =
      "Camera access denied. Please enable camera permissions and try again.";
  }
};

const stopWebcam = () => {
  if (stream.value) {
    stream.value.getTracks().forEach((track) => track.stop());
    stream.value = null;
  }
  if (video.value) {
    video.value.srcObject = null;
  }
};

const captureImage = () => {
  const canvas = document.createElement("canvas");
  canvas.width = video.value.videoWidth;
  canvas.height = video.value.videoHeight;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(video.value, 0, 0);
  capturedImage.value = canvas.toDataURL("image/jpeg", 0.8);
};

const retakeImage = () => {
  capturedImage.value = null;
  if (faceInputMethod.value === "webcam") {
    initializeWebcam();
  }
};

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    if (file.size > 10 * 1024 * 1024) {
      errorMessage.value = "File size must be less than 10MB";
      return;
    }
    const reader = new FileReader();
    reader.onload = (e) => {
      capturedImage.value = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleRegister = async () => {
  try {
    isLoading.value = true;
    errorMessage.value = "";
    let result;
    if (registerMethod.value === "credentials") {
      result = await apiService.register(username.value, password.value, null);
    } else {
      result = await apiService.register(
        username.value,
        password.value,
        capturedImage.value
      );
    }
    if (result.success) {
      router.push("/login");
    } else {
      errorMessage.value = result.error;
    }
  } catch (error) {
    errorMessage.value = "Registration failed. Please try again.";
    console.error("Registration error:", error);
  } finally {
    isLoading.value = false;
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
  --border-color: #e0e0e0;
  --text-primary: #212121;
  --text-secondary: #757575;
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

.login-container {
  display: flex;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  margin: 0;
  box-sizing: border-box;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1;
}

.login-card {
  background: var(--surface);
  border-radius: var(--radius-large);
  box-shadow: var(--shadow-3);
  padding: var(--spacing-xxl);
  width: 100%;
  max-width: 480px;
  min-height: 600px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  transition: transform 0.2s ease;
  margin: 0 auto;
}

@media (min-width: 900px) {
  .login-card {
    max-width: 600px;
    min-height: 700px;
  }
}

@media (max-width: 640px) {
  .login-container {
    padding: var(--spacing-md);
  }
  .login-card {
    padding: var(--spacing-lg);
    min-height: 400px;
  }
}

.login-card:hover {
  transform: translateY(-2px);
}

.login-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.login-title {
  font-size: 2rem;
  font-weight: 400;
  color: var(--text-primary);
  margin: 0 0 var(--spacing-sm) 0;
  letter-spacing: -0.5px;
}

.login-subtitle {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin: 0;
  font-weight: 400;
}

.error-message {
  background: var(--error-light);
  color: var(--error-color);
  padding: var(--spacing-md);
  border-radius: var(--radius-medium);
  margin-bottom: var(--spacing-lg);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 0.875rem;
  border: 1px solid rgba(211, 47, 47, 0.2);
}

.error-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.login-methods {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-xl);
  background: var(--background);
  padding: var(--spacing-xs);
  border-radius: var(--radius-medium);
}

.method-tab {
  padding: var(--spacing-md) var(--spacing-sm);
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: var(--radius-small);
  font-size: 0.875rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  transition: all 0.2s ease;
  min-height: 48px;
}

.method-tab:hover {
  background: rgba(25, 118, 210, 0.04);
  color: var(--primary-color);
}

.method-tab.active {
  background: var(--surface);
  color: var(--primary-color);
  box-shadow: var(--shadow-1);
}

.method-icon {
  width: 18px;
  height: 18px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: var (--spacing-sm);
}

.input-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-primary);
  margin: 0;
}

.input-field {
  padding: var(--spacing-md);
  border: 2px solid var(--border-color);
  border-radius: var(--radius-small);
  font-size: 1rem;
  transition: border-color 0.2s ease;
  background: var(--surface);
  color: var(--text-primary);
}

.input-field:focus {
  outline: none;
  border-color: var(--primary-color);
}

.input-field::placeholder {
  color: var(--text-secondary);
}

.primary-button {
  background: var(--primary-color);
  color: white;
  border: none;
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--radius-small);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.primary-button:hover:not(:disabled) {
  background: var(--primary-hover);
  box-shadow: var(--shadow-2);
}

.primary-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.secondary-button {
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

.secondary-button:hover {
  background: var(--primary-light);
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.face-login {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.face-input-selector {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-sm);
  background: var(--background);
  padding: var(--spacing-xs);
  border-radius: var(--radius-medium);
}

.input-method-btn {
  padding: var(--spacing-sm);
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  border-radius: var (--radius-small);
  font-size: 0.875rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);
  transition: all 0.2s ease;
  min-height: 40px;
}

.input-method-btn:hover {
  background: rgba(25, 118, 210, 0.04);
  color: var(--primary-color);
}

.input-method-btn.active {
  background: var(--surface);
  color: var(--primary-color);
  box-shadow: var(--shadow-1);
}

.webcam-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-lg);
}

.camera-container {
  position: relative;
  border-radius: var(--radius-medium);
  overflow: hidden;
  box-shadow: var(--shadow-2);
  background: #000;
}

.video-feed {
  width: 100%;
  max-width: 400px;
  height: auto;
  display: block;
}

.camera-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.face-guide {
  width: 200px;
  height: 250px;
  border: 3px solid rgba(255, 255, 255, 0.8);
  border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
  background: transparent;
}

.capture-button {
  background: var(--primary-color);
  color: white;
  border: none;
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: 50px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  box-shadow: var(--shadow-2);
}

.capture-button:hover {
  background: var(--primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-3);
}

.capture-icon {
  width: 20px;
  height: 20px;
}

.upload-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.file-input {
  display: none;
}

.upload-area {
  border: 2px dashed var(--border-color);
  border-radius: var(--radius-medium);
  padding: var(--spacing-xxl);
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  background: var(--background);
  width: 100%;
}

.upload-area:hover {
  border-color: var(--primary-color);
  background: var(--primary-light);
}

.upload-icon {
  width: 48px;
  height: 48px;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-md);
}

.upload-title {
  font-size: 1.125rem;
  font-weight: 500;
  color: var(--text-primary);
  margin: 0 0 var(--spacing-sm) 0;
}

.upload-description {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin: 0 0 var(--spacing-sm) 0;
}

.upload-formats {
  font-size: 0.75rem;
  color: var(--text-secondary);
  opacity: 0.8;
}

.captured-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-lg);
}

.preview-container {
  position: relative;
  border-radius: var(--radius-medium);
  overflow: hidden;
  box-shadow: var(--shadow-2);
}

.preview-image {
  width: 100%;
  max-width: 300px;
  height: auto;
  display: block;
}

.preview-overlay {
  position: absolute;
  top: var(--spacing-sm);
  right: var(--spacing-sm);
}

.switch-auth-link {
  margin-top: var(--spacing-xl);
  text-align: center;
  font-size: 0.95rem;
  color: var(--text-secondary);
}

.switch-link {
  color: var(--primary-color);
  margin-left: 6px;
  text-decoration: underline;
  cursor: pointer;
  font-weight: 500;
}

.switch-link:hover {
  color: var(--primary-hover);
}

@media (max-width: 640px) {
  .login-container {
    padding: var(--spacing-md);
  }
  .login-card {
    padding: var(--spacing-lg);
  }
  .login-title {
    font-size: 1.75rem;
  }
  .login-methods {
    grid-template-columns: 1fr;
  }
  .face-input-selector {
    grid-template-columns: 1fr;
  }
  .method-tab,
  .input-method-btn {
    min-height: 44px;
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
  .login-container {
    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  }
}
</style>
