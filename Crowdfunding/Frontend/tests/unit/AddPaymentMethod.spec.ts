import { mount, flushPromises } from '@vue/test-utils';
import AddPaymentMethod from '../../src/components/AddPaymentMethod.vue';
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createTestingPinia } from '@pinia/testing'
import { useMessageStore } from '../../src/stores/message'
import { createRouter, createMemoryHistory } from 'vue-router'

vi.mock('@/services/api', () => ({
  default: {
    post: vi.fn()
  }
}))

import api from '../../src/services/api'

describe('PaymentForm.vue', () => {
  let router: ReturnType<typeof createRouter>

  beforeEach(() => {
    router = createRouter({
      history: createMemoryHistory(),
      routes: [{ path: '/', name: 'PaymentMethods', component: { template: '<div />' } }]
    })
  })

  it('renderiza los campos del formulario', () => {
    const wrapper = mount(AddPaymentMethod, {
      global: {
        plugins: [createTestingPinia(), router]
      }
    })

    expect(wrapper.find('input#holderName').exists()).toBe(true)
    expect(wrapper.find('input#cardNumber').exists()).toBe(true)
    expect(wrapper.find('input#cvv').exists()).toBe(true)
    expect(wrapper.find('input#expirationDate').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
  })

  it('envía el formulario correctamente', async () => {
    const mockPush = vi.spyOn(router, 'push')
    const wrapper = mount(AddPaymentMethod, {
      global: {
        plugins: [createTestingPinia(), router],
        mocks: {
          $route: { query: {} }
        }
      }
    })

    await wrapper.find('#holderName').setValue('Juan Pérez')
    await wrapper.find('#cardNumber').setValue('1234567812345678')
    await wrapper.find('#cvv').setValue('123')
    await wrapper.find('#expirationDate').setValue('2025-12-31')

    await wrapper.find('form').trigger('submit.prevent')

    expect(api.post).toHaveBeenCalledWith(
      '/payment-methods/payment-methods/',
      expect.objectContaining({
        holder_name: 'Juan Pérez',
        card_number: '1234567812345678',
        cvv: '123',
        expiration_date: '2025-12-31'
      })
    )

    await flushPromises()
    expect(mockPush).toHaveBeenCalledWith({ name: 'PaymentMethods' })
  })

  it('muestra mensaje de error si falla el envío', async () => {
    

    vi.mocked(api).post = vi.fn().mockRejectedValue({
      response: {
        data: { detail: 'Error del servidor' }
      }
    })

    const wrapper = mount(AddPaymentMethod, {
      global: {
        plugins: [createTestingPinia({ stubActions: false }), router],
        mocks: {
          $route: { query: {} }
        }
      }
    })

    const messageStore = useMessageStore()
    const mockSetMessage = vi.spyOn(messageStore, 'setMessage')

    await wrapper.find('#holderName').setValue('Juan Pérez')
    await wrapper.find('#cardNumber').setValue('1234567812345678')
    await wrapper.find('#cvv').setValue('123')
    await wrapper.find('#expirationDate').setValue('2025-12-31')

    await wrapper.find('form').trigger('submit.prevent')
    await flushPromises()

    expect(mockSetMessage).toHaveBeenCalledWith('Error del servidor', 'error')
  })
})
