<template>
  <div class="container py-5">
    <GoBackBtn />
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
          <div class="d-flex justify-content-center mt-3">
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
import GoBackBtn from '@/components/GoBackBtn.vue';

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
.card {
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  background-color: #ffffff;
  transition: box-shadow 0.2s ease;
}

.card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.card h5 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
}

.card p {
  font-size: 1rem;
  margin-bottom: 0.25rem;
  color: #374151;
}

.card small {
  font-size: 0.875rem;
  color: #6b7280;
}

.btn {
  font-weight: 500;
}

.btn-outline-primary {
  border-color: #6366f1;
  color: #6366f1;
}

.btn-outline-primary:hover {
  background-color: #6366f1;
  color: white;
}

.btn-outline-danger {
  border-color: #ef4444;
  color: #ef4444;
}

.btn-outline-danger:hover {
  background-color: #ef4444;
  color: white;
}

.btn-success {
  background-color: #16a34a;
  border-color: #16a34a;
}

.btn-success:hover {
  background-color: #15803d;
  border-color: #15803d;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}

.modal-dialog {
  background: #fff;
  border-radius: 0.75rem;
  max-width: 480px;
  width: 100%;
  padding: 1.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.modal-content h5 {
  font-weight: 600;
  font-size: 1.125rem;
  color: #1f2937;
}

.modal-content .btn-secondary {
  background-color: #e5e7eb;
  border: none;
  color: #374151;
}

.modal-content .btn-secondary:hover {
  background-color: #d1d5db;
}

</style>