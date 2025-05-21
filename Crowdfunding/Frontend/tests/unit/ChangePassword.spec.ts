import { mount, flushPromises } from '@vue/test-utils'
import ChangePassword from '../../src/components/ChangePassword.vue'
import { vi, describe, it, expect, beforeEach } from 'vitest'
import { createRouter, createMemoryHistory } from 'vue-router'
import api from '../../src/services/api'

const push = vi.fn()
vi.mock('vue-router', async () => {
  const actual = await vi.importActual('vue-router')
  return {
    ...actual,
    useRoute: () => ({
      query: { uid: '123', token: 'abc' }
    }),
    useRouter: () => ({
      push: vi.fn(),
    }),
  }
})

vi.mock('../../src/services/api', () => {
  return {
    default: {
      post: vi.fn(),
    },
  }
})

describe('ChangePassword.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    push.mockClear()
  })

  it('renderiza correctamente', () => {
    const wrapper = mount(ChangePassword)
    expect(wrapper.text()).toContain('Recuperar Contraseña')
  })

  it('muestra error si campos están vacíos', async () => {
    const wrapper = mount(ChangePassword)
    await wrapper.find('form').trigger('submit.prevent')
    expect(wrapper.text()).toContain('Por favor completa ambos campos.')
  })

  it('muestra error si contraseñas no coinciden', async () => {
    const wrapper = mount(ChangePassword)
    await wrapper.find('#newPassword').setValue('password123')
    await wrapper.find('#confirmNewPassword').setValue('password456')
    await wrapper.find('form').trigger('submit.prevent')
    expect(wrapper.text()).toContain('Las contraseñas no coinciden.')
  })

  it('muestra error si api.post falla', async () => {
    (api.post as any).mockRejectedValueOnce(new Error('fail'))
    const wrapper = mount(ChangePassword)
    await wrapper.find('#newPassword').setValue('password123')
    await wrapper.find('#confirmNewPassword').setValue('password123')
    await wrapper.find('form').trigger('submit.prevent')
    await flushPromises()
    expect(wrapper.text()).toContain('Hubo un error al restablecer la contraseña.')
  })
})
