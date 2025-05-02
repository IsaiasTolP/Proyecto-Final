<template>
  <div class="container py-5">
    <h2 class="mb-4 text-success">Mis Métodos de Pago</h2>

    <button class="btn btn-success mb-4" @click="goToAddMethod">
      Añadir Método de Pago
    </button>

    <div v-if="paymentMethods.length === 0" class="text-muted">
      No tienes métodos de pago guardados.
    </div>

    <div v-for="method in paymentMethods" :key="method.id" class="card mb-3 p-3 shadow-sm">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h5 class="mb-1">{{ method.holder_name }}</h5>
          <p class="mb-1">**** **** **** {{ method.card_last4 || '****' }}</p>
          <small class="text-muted">Vence: {{ formatDate(method.expiration_date) }}</small>
        </div>
        <div>
          <button class="btn btn-outline-primary me-2" @click="openEditDialog(method)">
            Editar
          </button>
          <button class="btn btn-outline-danger" @click="confirmDelete(method.id)">
            Eliminar
          </button>
        </div>
      </div>
    </div>

    <!-- Diálogo de Confirmación para Eliminar -->
    <div v-if="deleteId !== null" class="modal-backdrop">
      <div class="modal-dialog shadow">
        <div class="modal-content p-4">
          <h5>¿Estás seguro de que quieres eliminar este método de pago?</h5>
          <div class="d-flex justify-content-end mt-4">
            <button class="btn btn-secondary me-2" @click="deleteId = null">Cancelar</button>
            <button class="btn btn-danger" @click="deleteMethod">Eliminar</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Diálogo de Edición -->
    <div v-if="editMethod" class="modal-backdrop d-flex justify-content-center align-items-center">
      <div class="modal-dialog shadow">
        <div class="modal-content p-4">
          <h5 class="mb-3">Editar Método de Pago</h5>
          <EditPaymentMethodForm
            :paymentMethod="editMethod"
            @update="handleUpdateMethod"
          />
          <div class="d-flex justify-content-end mt-3">
            <button class="btn btn-secondary" @click="editMethod = null">Cancelar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import EditPaymentMethodForm from '@/components/EditPaymentMethodForm.vue';

const router = useRouter();
const paymentMethods = ref<any[]>([]);
const deleteId = ref<number | null>(null);
const editMethod = ref<any | null>(null);

onMounted(async () => {
  await loadPaymentMethods();
});

async function loadPaymentMethods() {
  try {
    const { data } = await api.get('/payment-methods/payment-methods/');
    paymentMethods.value = data;
  } catch (err) {
    console.error('Error al cargar métodos de pago', err);
  }
}

function goToAddMethod() {
  router.push({ name: 'AddPaymentMethod' });
}

function confirmDelete(id: number) {
  deleteId.value = id;
}

async function deleteMethod() {
  if (deleteId.value !== null) {
    try {
      await api.delete(`/payment-methods/payment-methods/${deleteId.value}/`);
      paymentMethods.value = paymentMethods.value.filter(pm => pm.id !== deleteId.value);
      deleteId.value = null;
    } catch (err) {
      console.error('Error al eliminar método de pago', err);
    }
  }
}

function openEditDialog(method: any) {
  editMethod.value = { ...method };
}

async function handleUpdateMethod(updatedData: any) {
  try {
    await api.put(`/payment-methods/payment-methods/${editMethod.value.id}/`, updatedData);
    await loadPaymentMethods();
    editMethod.value = null;
  } catch (err) {
    console.error('Error al actualizar método de pago', err);
  }
}

function formatDate(dateStr: string) {
  const options: Intl.DateTimeFormatOptions = { month: '2-digit', year: '2-digit' };
  return new Date(dateStr).toLocaleDateString(undefined, options);
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}
.modal-dialog {
  background: white;
  border-radius: 8px;
  max-width: 500px;
  width: 100%;
}
</style>