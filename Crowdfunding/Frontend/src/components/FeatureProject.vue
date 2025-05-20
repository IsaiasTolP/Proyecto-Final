<template>
  <div class="modal fade show d-block" tabindex="-1" @click.self="close">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content p-4">
        <div class="modal-header border-0 pb-0">
          <h5 class="modal-title">Patrocinar Proyecto</h5>
          <button type="button" class="btn-close" @click="close"></button>
        </div>

        <div class="modal-body pt-2">
          <p class="text-muted mb-3">Haz que tu proyecto sea destacado por solo <strong>100 €</strong>.</p>

          <form @submit.prevent="submitFeature">
            <!-- Método de Pago -->
            <div class="mb-3">
              <label for="paymentMethod" class="form-label fw-medium">Método de Pago</label>
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

                <input
                  v-if="form.payment_method"
                  v-model="form.cvv"
                  type="password"
                  maxlength="4"
                  minlength="3"
                  class="form-control"
                  placeholder="CVV"
                  required
                />
                <router-link
                  class="btn-outline-secondary-custom"
                  :to="{ name: 'AddPaymentMethod', query: { back: 'true' } }"
                >
                  Añadir
                </router-link>
              </div>
            </div>

            <button type="submit" class="btn-outline-secondary-custom w-100" :disabled="loading">
              {{ loading ? 'Procesando...' : 'Patrocinar por 100 €' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const props = defineProps<{ projectId: number }>()
const emit = defineEmits(['close', 'featured'])

const paymentMethods = ref<any[]>([])
const loading = ref(false)

const form = ref({
  payment_method: '',
  cvv: '',
})

onMounted(() => {
  fetchPaymentMethods()
})

async function fetchPaymentMethods() {
  try {
    const { data } = await api.get('/payment-methods/payment-methods/')
    paymentMethods.value = data
  } catch (error) {
    console.error('Error cargando métodos de pago:', error)
  }
}

async function submitFeature() {
  loading.value = true
  try {
    await api.post('/projects/sponsorships/', {
      project: props.projectId,
      payment_method: form.value.payment_method,
			cvv: form.value.cvv,
    })

    await api.patch(`/projects/list/${props.projectId}/`, { featured: true })

    emit('featured', props.projectId)
    close()
  } catch (error) {
    console.error('Error al patrocinar:', error)
  } finally {
    loading.value = false
  }
}

function close() {
  emit('close')
}
</script>

<style scoped>
.modal {
  background-color: rgba(0, 0, 0, 0.4);
  z-index: 1050;
}

.modal-content {
  border-radius: 0.75rem;
  background-color: #ffffff;
}

.btn-outline-secondary-custom {
  background: linear-gradient(90deg, #7c3aed, #a78bfa);
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
  padding: 0.5rem 1rem;
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
</style>
