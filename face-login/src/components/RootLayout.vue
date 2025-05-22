<template>
  <div class="root-layout">
    <slot />
  </div>
</template>

<script setup>
// No logic needed for root layout
</script>

<style scoped>
:root {
  --primary-color: #1976d2;
  --primary-hover: #1565c0;
  --primary-light: #e3f2fd;
  --secondary-color: #757575;
  --background: #fafafa;
  --surface: #ffffff;
  --surface-card: #fff;
  --surface-border: #e0e0e0;
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

.root-layout {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

@media (prefers-color-scheme: dark) {
  :root {
    --background: #121212;
    --surface: #1e1e1e;
    --surface-border: #333333;
    --text-primary: #ffffff;
    --text-secondary: #b3b3b3;
  }
  .root-layout {
    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  }
}
</style>
