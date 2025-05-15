<template>
  <div class="login-container">
    <h2>Login</h2>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <div class="login-methods">
      <button
        :class="['method-btn', { active: loginMethod === 'credentials' }]"
        @click="switchMethod('credentials')"
      >
        Username & Password
      </button>
      <button
        :class="['method-btn', { active: loginMethod === 'face' }]"
        @click="switchMethod('face')"
      >
        Face Recognition
      </button>
    </div>

    <!-- Credentials Login Form -->
    <form
      v-if="loginMethod === 'credentials'"
      @submit.prevent="handleCredentialsLogin"
      class="login-form"
    >
      <div class="form-group">
        <label for="username">Username</label>
        <input
          type="text"
          id="username"
          v-model="username"
          required
          class="form-control"
        />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input
          type="password"
          id="password"
          v-model="password"
          required
          class="form-control"
        />
      </div>
      <button type="submit" class="submit-btn">Login</button>
    </form>
    <!--
Face Recognition Login -->
    <div v-else class="face-login">
      <div class="input-method-selector">
        <button
          :class="['method-btn', { active: faceInputMethod === 'webcam' }]"
          @click="switchFaceInput('webcam')"
        >
          Use Webcam
        </button>
        <button
          :class="['method-btn', { active: faceInputMethod === 'upload' }]"
          @click="switchFaceInput('upload')"
        >
          Upload Image
        </button>
      </div>

      <div v-if="faceInputMethod === 'webcam'" class="webcam-container">
        <div v-if="webcamError" class="error-message">{{ webcamError }}</div>
        <video
          v-show="!capturedImage"
          ref="video"
          width="400"
          height="300"
          autoplay
        ></video>
        <button
          v-if="!capturedImage"
          type="button"
          @click="captureImage"
          class="capture-btn"
        >
          Capture Image
        </button>
      </div>

      <div v-else class="upload-container">
        <input
          type="file"
          ref="fileInput"
          @change="handleFileUpload"
          accept="image/*"
          class="file-input"
        />
        <div class="upload-preview" v-if="!capturedImage">
          <button @click="triggerFileInput" class="upload-btn">
            Choose Image
          </button>
          <p class="upload-hint">Supported formats: JPG, PNG</p>
        </div>
      </div>

      <div v-if="capturedImage" class="captured-image">
        <img :src="capturedImage" alt="Face image" width="400" />
        <div class="button-group">
          <button type="button" @click="retakeImage" class="retake-btn">
            {{ faceInputMethod === "webcam" ? "Retake" : "Choose Another" }}
          </button>
          <button type="button" @click="handleFaceLogin" class="submit-btn">
            Login with Face
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import apiService from "@/services/api";
import { authStore } from "@/stores/auth";

const router = useRouter();
const loginMethod = ref("credentials");
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
  if (loginMethod.value === "face") {
    await initializeWebcam();
  }
});

onUnmounted(() => {
  stopWebcam();
});

const switchMethod = async (method) => {
  loginMethod.value = method;
  if (method === "face") {
    await initializeWebcam();
  } else {
    stopWebcam();
  }
};

const switchFaceInput = (method) => {
  faceInputMethod.value = method;
  if (method === "webcam") {
    initializeWebcam();
  } else {
    stopWebcam();
  }
};

const initializeWebcam = async () => {
  try {
    stream.value = await navigator.mediaDevices.getUserMedia({ video: true });
    if (video.value) {
      video.value.srcObject = stream.value;
    }
  } catch (err) {
    console.error("Error accessing webcam:", err);
    errorMessage.value =
      "Could not access webcam. Please make sure you have granted camera permissions.";
  }
};

const startWebcam = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.value.srcObject = stream;
    webcamError.value = null;
  } catch (error) {
    console.error("Error accessing webcam:", error);
    webcamError.value =
      "Camera access denied. Please enable camera permissions and try again.";
    isFaceLoginMode.value = false;
  }
};

const stopWebcam = () => {
  if (video.value && video.value.srcObject) {
    const tracks = video.value.srcObject.getTracks();
    tracks.forEach((track) => track.stop());
    video.value.srcObject = null;
  }
};

const captureImage = () => {
  const canvas = document.createElement("canvas");
  canvas.width = video.value.videoWidth;
  canvas.height = video.value.videoHeight;
  canvas.getContext("2d").drawImage(video.value, 0, 0);
  capturedImage.value = canvas.toDataURL("image/jpeg");
};

const retakeImage = () => {
  capturedImage.value = null;
};

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
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

const handleCredentialsLogin = async () => {
  try {
    isLoading.value = true;
    errorMessage.value = "";

    const result = await apiService.loginWithCredentials(
      username.value,
      password.value
    );

    if (result.success) {
      authStore.setUser({
        username: username.value,
        loginMethod: "credentials",
      });
      router.push("/dashboard");
    } else {
      errorMessage.value = result.error;
    }
  } catch (error) {
    errorMessage.value = "Login failed. Please try again.";
    console.error("Login error:", error);
  } finally {
    isLoading.value = false;
  }
};

const handleFaceLogin = async () => {
  try {
    isLoading.value = true;
    errorMessage.value = "";

    const result = await apiService.loginWithFace(capturedImage.value);

    if (result.success) {
      authStore.setUser({
        username: result.data.username,
        loginMethod: "face recognition",
      });
      router.push("/dashboard");
    } else {
      errorMessage.value = result.error;
    }
  } catch (error) {
    errorMessage.value = "Face login failed. Please try again.";
    console.error("Face login error:", error);
  } finally {
    isLoading.value = false;
  }
};
</script>
<style scoped>
.login-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
}
.login-methods {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}
.method-btn {
  padding: 10px 20px;
  border: 1px solid #4caf50;
  background-color: white;
  color: #4caf50;
  cursor: pointer;
  border-radius: 4px;
}
.method-btn.active {
  background-color: #4caf50;
  color: white;
}
.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.form-control {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.webcam-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}
.upload-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}
.upload-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}
.upload-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #4caf50;
  color: white;
}
.upload-hint {
  font-size: 0.9em;
  color: #666;
}
.captured-image {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}
.button-group {
  display: flex;
  gap: 10px;
}
.capture-btn,
.retake-btn,
.submit-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.capture-btn,
.submit-btn {
  background-color: #4caf50;
  color: white;
}
.retake-btn {
  background-color: #f44336;
  color: white;
}
</style>
