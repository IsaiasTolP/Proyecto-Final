<template>
    <div class="container py-5">
      <h2 class="mb-4 text-success">Añadir Método de Pago</h2>
  
      <form @submit.prevent="submitPaymentMethod">
        <!-- Nombre del titular -->
        <div class="mb-3">
          <label for="holderName" class="form-label">Nombre del Titular</label>
          <input
            id="holderName"
            v-model="form.holder_name"
            type="text"
            class="form-control"
            required
          />
        </div>
  
        <!-- Número de tarjeta -->
        <div class="mb-3">
          <label for="cardNumber" class="form-label">Número de Tarjeta</label>
          <input
            id="cardNumber"
            v-model="form.card_number"
            type="text"
            class="form-control"
            maxlength="16"
            pattern="\d{16}"
            required
          />
        </div>
  
        <!-- CVV -->
        <div class="mb-3">
          <label for="cvv" class="form-label">CVV</label>
          <input
            id="cvv"
            v-model="form.cvv"
            type="text"
            class="form-control"
            maxlength="4"
            pattern="\d{3,4}"
            required
          />
        </div>
  
        <!-- Fecha de expiración -->
        <div class="mb-3">
          <label for="expirationDate" class="form-label">Fecha de Expiración</label>
          <input
            id="expirationDate"
            v-model="form.expiration_date"
            type="date"
            class="form-control"
            required
          />
        </div>
  
        <div v-if="messageStore.message" class="alert alert-danger">{{ messageStore.message }}</div>
  
        <button type="submit" class="btn btn-success">Guardar Método</button>
      </form>
    </div>
</template>

<script setup lang="ts">
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import api from '@/services/api';
	import { useMessageStore } from '@/stores/message';
  
  const router = useRouter();
	const messageStore = useMessageStore();
  
  const form = ref({
    holder_name: '',
    card_number: '',
    cvv: '',
    expiration_date: '',
  });
  
  const error = ref('');
  
  async function submitPaymentMethod() {
    try {
      await api.post('/payment-methods/payment-methods/', form.value);
      router.push({ name: 'PaymentMethods' });
    } catch (err: any) {
      error.value = err?.response?.data?.detail || 'Error al guardar el método de pago.';
			messageStore.setMessage(error.value, 'error');
    }
  }
</script>
