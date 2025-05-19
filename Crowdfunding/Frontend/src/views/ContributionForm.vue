<template>
  <main class="container py-5" style="max-width: 640px;">
    <h2 class="text-center fw-semibold mb-4 fs-5 text-dark">Contribuir al Proyecto</h2>

    <section class="contribution-card">
      <form @submit.prevent="submitContribution">
        <!-- Método de Pago -->
        <div class="mb-3">
          <label for="paymentMethod" class="form-label fw-medium text-dark">Método de Pago</label>
          <div class="d-flex align-items-center gap-2">
            <select
              v-model="form.payment_method"
              class="form-select custom-select"
              id="paymentMethod"
              required
            >
              <option disabled value="">Selecciona un método</option>
              <option v-for="method in paymentMethods" :key="method.id" :value="method.id">
                {{ method.holder_name }} - **** {{ method.card_last4 }}
              </option>
            </select>
            <router-link
              class="btn-outline-secondary-custom text-nowrap"
              :to="{ name: 'AddPaymentMethod', query: { back: 'true' } }"
            >
              Añadir
            </router-link>
          </div>
        </div>

        <!-- Cantidad -->
        <div class="mb-3">
          <label for="amount" class="form-label fw-medium text-dark">Cantidad (€)</label>
          <input
            v-model.number="form.amount"
            type="number"
            step="0.01"
            min="0.5"
            class="form-control"
            id="amount"
            required
          />
        </div>

        <!-- Mensaje -->
        <div class="mb-3">
          <label for="message" class="form-label fw-medium text-dark">
            Mensaje <span class="text-muted">(opcional, máx. 140 caracteres)</span>
          </label>
          <textarea
            v-model="form.message"
            class="form-control"
            id="message"
            maxlength="140"
            rows="3"
          ></textarea>
        </div>

        <!-- Mensajes de error -->
        <div v-if="messageStore.message" class="alert alert-danger" role="alert">
          {{ messageStore.message }}
        </div>

        <!-- Botón de envío -->
        <button type="submit" class="btn-outline-secondary-custom w-100 mt-2" :disabled="loading">
          {{ loading ? 'Enviando...' : 'Contribuir' }}
        </button>
      </form>
    </section>
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';
import { useMessageStore } from '@/stores/message';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const messageStore = useMessageStore();

const projectId = Number(route.params.id);
const form = ref({
  amount: null,
  payment_method: '',
  message: '',
  project: projectId,
});

const paymentMethods = ref<any[]>([]);
const loading = ref(false);

onMounted(async () => {
  await fetchPaymentMethods();
});

async function fetchPaymentMethods() {
  try {
    const { data } = await api.get('/payment-methods/payment-methods/');
    paymentMethods.value = data;
  } catch (error: any) {
    console.error('Error al cargar métodos de pago:', error);
  }
}

async function submitContribution() {
  try {
    loading.value = true;
    await api.post('/contributions/list/', form.value);
    router.push({ name: 'ProjectDetails', params: { projectId } });
  } catch (error: any) {
    if (axios.isAxiosError(error) && error.response) {
      const errors = error.response.data;
      if (errors.payment_method) {
        messageStore.setMessage(`Error al enviar la contribución. ${errors.payment_method[0]}`, 'error');
      }
    }
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.contribution-card {
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  box-shadow: 0 1px 2px rgb(0 0 0 / 0.05);
  padding: 1.5rem;
  background-color: #ffffff;
}

.custom-select {
  background-color: #f9fafb;
  border-radius: 0.375rem;
  padding: 0.5rem;
}

.btn-outline-secondary-custom {
  background: linear-gradient(90deg, #7c3aed 0%, #a78bfa 100%);
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
  padding: 0.5rem 1.25rem;
  border-radius: 0.5rem;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  box-shadow: 0 4px 8px rgba(124, 58, 237, 0.3);
  transition: box-shadow 0.3s ease, transform 0.2s ease;
  text-decoration: none;
}

.btn-outline-secondary-custom:hover,
.btn-outline-secondary-custom:focus {
  box-shadow: 0 6px 12px rgba(124, 58, 237, 0.5);
  transform: translateY(-2px);
  color: white;
  text-decoration: none;
}

label.form-label {
  font-size: 0.9rem;
}

textarea.form-control,
input.form-control {
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
}
</style>
