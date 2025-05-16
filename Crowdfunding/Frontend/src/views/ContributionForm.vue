<template>
    <div class="container py-4">
      <h2 class="mb-4 text-success">Contribuir al Proyecto</h2>
  
      <form @submit.prevent="submitContribution">
        <div class="mb-3 d-flex align-items-center">
          <div class="flex-grow-1 me-2">
            <label for="paymentMethod" class="form-label d-block">Método de Pago</label>
            <div class="d-flex align-items-center">
              <select
                v-model="form.payment_method"
                class="form-select me-2"
                id="paymentMethod"
                required
              >
                <option disabled value="">Selecciona un método</option>
                <option v-for="method in paymentMethods" :key="method.id" :value="method.id">
                {{ method.holder_name }} - **** {{ method.card_last4 }}
                </option>
              </select>
                <router-link class="btn btn-outline-success" :to="{ name: 'AddPaymentMethod', query: { back: 'true' }}">Añadir</router-link>
            </div>
          </div>
        </div>
  
        <div class="mb-3">
          <label for="amount" class="form-label">Cantidad (€)</label>
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
  
        <div class="mb-3">
          <label for="message" class="form-label">Mensaje (opcional, máx. 140 caracteres)</label>
          <textarea
            v-model="form.message"
            class="form-control"
            id="message"
            maxlength="140"
            rows="3"
          ></textarea>
        </div>
  
        <div v-if="messageStore.message">
          <div class="alert alert-danger" role="alert">
            {{ messageStore.message }}
          </div>
        </div>
        <button type="submit" class="btn btn-success" :disabled="loading">
          {{ loading ? 'Enviando...' : 'Contribuir' }}
        </button>
      </form>
    </div>
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
      await api.post('/contributions/', form.value);
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
