<template>
  <div class="payment-form container py-5 my-5">
    <GoBackBtn />
    <h2 class="mb-4 title">Añadir Método de Pago</h2>

    <form @submit.prevent="submitPaymentMethod" class="form">
      <!-- Nombre del titular -->
      <div class="form-group">
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
      <div class="form-group">
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
      <div class="form-group">
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
      <div class="form-group">
        <label for="expirationDate" class="form-label">Fecha de Expiración</label>
        <input
          id="expirationDate"
          v-model="form.expiration_date"
          type="date"
          class="form-control"
          required
        />
      </div>

      <div v-if="messageStore.message" class="alert alert-danger mt-3">{{ messageStore.message }}</div>

      <button type="submit" class="btn btn-submit">Guardar Método</button>
    </form>
  </div>
</template>

<script setup lang="ts">
  import { ref } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import api from '@/services/api';
  import { useMessageStore } from '@/stores/message';
  import GoBackBtn from './GoBackBtn.vue';

  const router = useRouter();
  const route = useRoute();
  const messageStore = useMessageStore();

  const form = ref({
    holder_name: '',
    card_number: '',
    cvv: '',
    expiration_date: '',
  });

  async function submitPaymentMethod() {
    try {
      await api.post('/payment-methods/payment-methods/', form.value);
      if (route.query.back === 'true') {
        router.back();
      } else {
        router.push({ name: 'PaymentMethods' });
      }
    } catch (err: any) {
      messageStore.setMessage(
        err?.response?.data?.detail || 'Error al guardar el método de pago.',
        'error'
      );
    }
  }
</script>

<style scoped>
.payment-form {
  max-width: 600px;
  margin: 0 auto;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.1);
  padding: 2rem 2.5rem;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.title {
  font-weight: 700;
  font-size: 2rem;
  text-align: center;
  margin-bottom: 2rem;
  color: #7c3aed;
}

.form-group {
  margin-bottom: 1.8rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
  user-select: none;
}

.form-control {
  width: 100%;
  padding: 0.65rem 1rem;
  font-size: 1rem;
  border-radius: 8px;
  border: 1.8px solid #cbd5e0;
  transition: border-color 0.25s ease, box-shadow 0.25s ease;
  font-family: inherit;
}

.form-control:focus {
  border-color: #7c3aed;
  box-shadow: 0 0 5px rgba(124, 58, 237, 0.5);
  outline: none;
}

.alert {
  font-weight: 600;
  font-size: 0.95rem;
}

.btn-submit {
  display: block;
  width: 100%;
  background-color: #7c3aed;
  color: white;
  font-weight: 700;
  font-size: 1.15rem;
  padding: 0.9rem 1.2rem;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  user-select: none;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  margin-top: 1.5rem;
}

.btn-submit:hover {
  background-color: #6b21a8;
  box-shadow: 0 6px 12px rgba(107, 33, 168, 0.45);
  outline: none;
}

.btn-submit:focus {
  outline: 2px solid #d8b4fe;
  outline-offset: 2px;
}
</style>
