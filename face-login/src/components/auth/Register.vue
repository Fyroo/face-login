<template>
  <div class="register-container">
    <h2>Register</h2>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <form @submit.prevent="handleRegister" class="register-form">
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
      <div class="form-group">
        <label>Face Image</label>
        <div class="input-method-selector">
          <button
            type="button"
            :class="['method-btn', { active: faceInputMethod === 'webcam' }]"
            @click="switchFaceInput('webcam')"
          >
            Use Webcam
          </button>
          <button
            type="button"
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
            <button type="button" @click="triggerFileInput" class="upload-btn">
              Choose Image
            </button>
            <p class="upload-hint">Supported formats: JPG, PNG</p>
          </div>
        </div>

        <div v-if="capturedImage" class="captured-image">
          <img :src="capturedImage" alt="Face image" width="400" />
          <button type="button" @click="retakeImage" class="retake-btn">
            {{ faceInputMethod === "webcam" ? "Retake" : "Choose Another" }}
          </button>
        </div>
      </div>

      <button
        type="submit"
        class="submit-btn"
        :disabled="!isFormValid || isLoading"
      >
        {{ isLoading ? "Registering..." : "Register" }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from "vue";
import apiService from "@/services/api";
import { useRouter } from "vue-router";

const router = useRouter();
const username = ref("");
const password = ref("");
const video = ref(null);
const capturedImage = ref(null);
const stream = ref(null);
const errorMessage = ref("");
const isLoading = ref(false);
const faceInputMethod = ref("webcam");
const fileInput = ref(null);
const webcamError = ref(null);

const isFormValid = computed(() => {
  return username.value && password.value && capturedImage.value;
});

onMounted(async () => {
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
});

onUnmounted(() => {
  if (stream.value) {
    stream.value.getTracks().forEach((track) => track.stop());
  }
});

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

const switchFaceInput = (method) => {
  faceInputMethod.value = method;
  if (method === "webcam") {
    initializeWebcam();
  } else {
    stopWebcam();
  }
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

const initializeWebcam = async () => {
  try {
    stream.value = await navigator.mediaDevices.getUserMedia({ video: true });
    if (video.value) {
      video.value.srcObject = stream.value;
    }
    webcamError.value = null;
  } catch (err) {
    console.error("Error accessing webcam:", err);
    webcamError.value =
      "Could not access webcam. Please make sure you have granted camera permissions.";
    faceInputMethod.value = "upload";
  }
};

const stopWebcam = () => {
  if (stream.value) {
    stream.value.getTracks().forEach((track) => track.stop());
  }
};

const handleRegister = async () => {
  try {
    isLoading.value = true;
    errorMessage.value = "";

    const result = await apiService.register(
      username.value,
      password.value,
      capturedImage.value
    );

    if (result.success) {
      // Navigate to login page
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
.register-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
}

.register-form {
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

.captured-image {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.capture-btn,
.retake-btn,
.submit-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #4caf50;
  color: white;
  transition: background-color 0.3s;
}

.capture-btn:hover,
.submit-btn:hover {
  background-color: #45a049;
}

.retake-btn {
  background-color: #f44336;
}

.retake-btn:hover {
  background-color: #e53935;
}

.submit-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.input-method-selector {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
  justify-content: center;
}

.method-btn {
  padding: 8px 16px;
  border: 1px solid #4caf50;
  background-color: white;
  color: #4caf50;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s;
}

.method-btn.active {
  background-color: #4caf50;
  color: white;
}

.upload-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
  margin: 10px 0;
}

.file-input {
  display: none;
}

.upload-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 20px;
  border: 2px dashed #ddd;
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
}

.upload-btn {
  padding: 10px 20px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.upload-btn:hover {
  background-color: #45a049;
}

.upload-hint {
  color: #666;
  font-size: 0.9em;
}
</style>
