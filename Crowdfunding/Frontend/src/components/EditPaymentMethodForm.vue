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

      <div class="d-flex justify-content-end">
        <button type="submit" class="btn btn-success">Guardar Cambios</button>
      </div>
    </form>
</template>

<script setup lang="ts">
  import { ref, watch, defineProps, defineEmits } from 'vue';

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
  
  // Rellenar campos iniciales al montar o cambiar prop
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
