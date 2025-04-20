import { createApp } from 'vue';
import App from './App.vue';
import router from '@/router/index.ts';
import '@/assets/css/bootstrap.min.css';
import '@/assets/js/bootstrap.bundle.min.js';

const app = createApp(App);
app.use(router);
app.mount('#app');