<template>
    <form @submit.prevent="submit">
      <div class="mb-3">
        <label for="holder_name" class="form-label">Nombre del Titular</label>
        <input
          id="holder_name"
          v-model="localForm.holder_name"
          type="text"
          class="form-control"
          required
        />
      </div>

      <div class="mb-3">
        <label for="card_number" class="form-label">Número de Tarjeta</label>
        <input
          id="card_number"
          v-model="localForm.card_number"
          type="text"
          class="form-control"
          maxlength="16"
          placeholder="Opcional"
        />
      </div>

      <div class="mb-3">
        <label for="cvv" class="form-label">CVV</label>
        <input
          id="cvv"
          v-model="localForm.cvv"
          type="text"
          class="form-control"
          maxlength="4"
          placeholder="Opcional"
        />
      </div>

      <div class="mb-3">
        <label for="expiration_date" class="form-label">Fecha de Expiración</label>
        <input
          id="expiration_date"
          v-model="localForm.expiration_date"
          type="date"
          class="form-control"
          required
        />
      </div>

      <div class="d-flex justify-content-center">
        <button type="submit" class="btn btn-success">Guardar Cambios</button>
      </div>
    </form>
</template>

<script setup lang="ts">
  import { ref, watch } from 'vue';

  const props = defineProps<{
    paymentMethod: {
      id: number;
      holder_name: string;
      expiration_date: string;
    };
  }>();
  
  const emit = defineEmits(['update']);
  
  const localForm = ref({
    holder_name: '',
    card_number: '',
    cvv: '',
    expiration_date: '',
  });
  
  watch(
    () => props.paymentMethod,
    (method) => {
      localForm.value.holder_name = method.holder_name;
      localForm.value.expiration_date = method.expiration_date;
    },
    { immediate: true }
  );
  
  function submit() {
    emit('update', { ...localForm.value });
  }
</script>

<style scoped>
form {
  max-width: 400px;
  margin: 0 auto;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.mb-3 {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #1e3a8a; /* azul oscuro */
  user-select: none;
}

.form-control {
  width: 100%;
  padding: 0.55rem 1rem;
  font-size: 1rem;
  border-radius: 8px;
  border: 1.5px solid #94a3b8; /* azul grisáceo */
  transition: border-color 0.25s ease, box-shadow 0.25s ease;
  font-family: inherit;
}

.form-control::placeholder {
  color: #64748b; /* gris azulado */
  font-style: italic;
}

.form-control:focus {
  border-color: #2563eb; /* azul vivo */
  box-shadow: 0 0 6px rgba(37, 99, 235, 0.5);
  outline: none;
}

.d-flex {
  display: flex !important;
}

.justify-content-end {
  justify-content: flex-end !important;
  margin-top: 1.2rem;
}

.btn-success {
  background-color: #22c55e; /* verde suave */
  border: none;
  padding: 0.6rem 1.5rem;
  font-weight: 600;
  font-size: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  user-select: none;
}

.btn-success:hover {
  background-color: #16a34a; /* verde más oscuro */
}
</style>
