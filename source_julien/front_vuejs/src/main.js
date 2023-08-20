import { createApp } from 'vue'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css'
// import { BootstrapVue } from 'bootstrap-vue-3'

// Make BootstrapVue available throughout your project
const app = createApp(App);
// app.use(BootstrapVue);
app.mount('#app');