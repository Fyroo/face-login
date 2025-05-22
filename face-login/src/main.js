import "./assets/main.css";
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

// PrimeVue imports
import PrimeVue from "primevue/config";
import Card from "primevue/card";
import Button from "primevue/button";
import InputText from "primevue/inputtext";
import Password from "primevue/password";
import Message from "primevue/message";
import SelectButton from "primevue/selectbutton";
import Avatar from "primevue/avatar";
import ProgressSpinner from "primevue/progressspinner";
import Timeline from "primevue/timeline";
import Tag from "primevue/tag";

// PrimeVue styles
import "primevue/resources/themes/lara-light-indigo/theme.css";
import "primevue/resources/primevue.min.css";
import "primeicons/primeicons.css";
import "primeflex/primeflex.css";

const app = createApp(App);

// Register PrimeVue components
app.use(PrimeVue);
app.component("Card", Card);
app.component("Button", Button);
app.component("InputText", InputText);
app.component("Password", Password);
app.component("Message", Message);
app.component("SelectButton", SelectButton);
app.component("Avatar", Avatar);
app.component("ProgressSpinner", ProgressSpinner);
app.component("Timeline", Timeline);
app.component("Tag", Tag);

app.use(router);
app.mount("#app");
