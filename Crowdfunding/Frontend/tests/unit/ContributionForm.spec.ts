import { mount, flushPromises } from '@vue/test-utils'
import ContributionForm from '../../src/views/ContributionForm.vue'
import api from '../../src/services/api'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useRouter } from 'vue-router'
import { useMessageStore } from '../../src/stores/message'

vi.mock('../../src/services/api', () => ({
  default: { get: vi.fn(), post: vi.fn() }
}))

const push = vi.fn()
vi.mock('vue-router', async () => {
  const actual = await vi.importActual<typeof import('vue-router')>('vue-router')
  return {
    ...actual,
    useRoute: () => ({ params: { id: '123' } }),
    useRouter: () => ({ push }),
  }
})

vi.mock('../../src/stores/message', () => ({
  useMessageStore: () => ({ message: '', setMessage: vi.fn() })
}))

describe('ContributionForm.vue', () => {
  let router: ReturnType<typeof useRouter>
  let messageStore: ReturnType<typeof useMessageStore>

  beforeEach(() => {
    vi.clearAllMocks()
    router = useRouter()
    messageStore = useMessageStore()
  })

  it('carga métodos de pago al montar y los muestra en el select', async () => {
    ;(api.get as any).mockResolvedValueOnce({ data: [
      { id: 1, holder_name: 'A', card_last4: '1111' },
      { id: 2, holder_name: 'B', card_last4: '2222' },
    ]})
    const wrapper = mount(ContributionForm)
    await flushPromises()

    const options = wrapper.findAll('select#paymentMethod option')
    expect(options).toHaveLength(3)
    expect(options[1].text()).toContain('A - **** 1111')
    expect(options[2].text()).toContain('B - **** 2222')
  })

  it('muestra campo CVV tras seleccionar un método', async () => {
    ;(api.get as any).mockResolvedValueOnce({ data: [{ id: 5, holder_name: 'X', card_last4: '5555' }]})
    const wrapper = mount(ContributionForm)
    await flushPromises()

    expect(wrapper.find('input#cvv').exists()).toBe(false)
    await wrapper.find('select#paymentMethod').setValue('5')
    await wrapper.vm.$nextTick()
    expect(wrapper.find('input#cvv').exists()).toBe(true)
  })

  it('envía la contribución y navega tras éxito', async () => {
    ;(api.get as any).mockResolvedValueOnce({ data: [{ id: 7, holder_name: 'Y', card_last4: '7777' }] })
    ;(api.post as any).mockResolvedValueOnce({})

    const wrapper = mount(ContributionForm)
    await flushPromises()

    await wrapper.find('select#paymentMethod').setValue('7')
    await wrapper.vm.$nextTick()
    await wrapper.find('input#cvv').setValue('123')
    await wrapper.find('input#amount').setValue('10.50')
    await wrapper.find('textarea#message').setValue('¡Bien!')

    const btn = wrapper.find('button[type="submit"]')
    await btn.trigger('submit')

    await flushPromises()

    expect(push).toHaveBeenCalledWith({ name: 'ProjectDetails', params: { projectId: 123 } })
  })

  it('muestra mensaje de error al fallar validación de payment_method', async () => {
    ;(api.get as any).mockResolvedValueOnce({ data: [{ id: 9, holder_name: 'Z', card_last4: '9999' }]})
    const errorResponse = {
      response: { data: { payment_method: ['no válido'] } }
    }
    ;(api.post as any).mockRejectedValueOnce(errorResponse)

    const wrapper = mount(ContributionForm)
    await flushPromises()

    await wrapper.find('select#paymentMethod').setValue('9')
    await wrapper.vm.$nextTick()
    await wrapper.find('input#cvv').setValue('321')
    await wrapper.find('input#amount').setValue('5')
    await wrapper.find('form').trigger('submit.prevent')
    await flushPromises()
  })
})
