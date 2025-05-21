import { shallowMount, flushPromises, mount } from '@vue/test-utils'
import Account from '../../src/views/Account.vue'
import api from '../../src/services/api'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createRouter, createMemoryHistory, useRouter } from 'vue-router'

vi.mock('vue-router', async () => {
  const actual = await vi.importActual<typeof import('vue-router')>('vue-router')
  return {
    ...actual,
    useRoute: () => ({ params: { id: '99' } }),
    useRouter: () => ({ push: vi.fn() }),
  }
})

vi.mock('@/stores/auth', () => {
  const user = { id: 99, username: 'pepito', is_founder: true }
  return {
    useAuthStore: () => ({ user })
  }
})

vi.mock('@/services/api', () => ({
  default: {
    get: vi.fn()
  }
}))

describe('Account.vue', () => {
  let router: ReturnType<typeof createRouter>
  const sampleProfile = {
    user: { id: 99, username: 'pepito' },
    pfp: 'https://img.jpg',
    bio: 'Hola mundo',
    location: 'Madrid',
    website: 'https://web',
    contact_email: 'pepito@mail.com',
    is_founder: true,
    social_media: {
      instagram: 'insta.com/u',
      twitter: 'tw.com/u',
      linkedin: 'li.com/u'
    }
  }
  const sampleStats = {
    created_projects: 5,
    supported_projects: 3,
    given_funds: 120
  }

  beforeEach(() => {
    vi.clearAllMocks()
    router = createRouter({
      history: createMemoryHistory(),
      routes: [
        { path: '/user/edit', name: 'EditUser', component: { template: '<div/>' } },
        { path: '/profile/edit', name: 'EditProfile', component: { template: '<div/>' } },
        { path: '/payment-methods', name: 'Payments', component: { template: '<div/>' } },
        { path: '/profile/:id/contributions', name: 'Contributions', component: { template: '<div/>' } },
        { path: '/projects/me', name: 'MyProjects', component: { template: '<div/>' } },
      ]
    })
  })

  function mountComponent() {
    ;(api.get as any)
      .mockResolvedValueOnce({ data: sampleProfile })
      .mockResolvedValueOnce({ data: sampleStats })

    return shallowMount(Account, {
      global: { plugins: [router], stubs: { GoBackBtn: true } }
    })
  }

  it('muestra loader inicialmente y luego el perfil', async () => {
    const wrapper = mountComponent()
    expect(wrapper.text()).toContain('Cargando perfil...')
    await flushPromises()
    expect(wrapper.text()).not.toContain('Cargando perfil...')
    expect(wrapper.find('h1').text()).toContain('Mi Perfil')
  })

  it('renderiza campos del perfil y badge de fundador', async () => {
    const wrapper = mountComponent()
    await flushPromises()
    const img = wrapper.find('img')
    expect(img.attributes('src')).toBe('https://img.jpg')
    expect(img.attributes('alt')).toContain('pepito')
    expect(wrapper.text()).toContain('Hola mundo')
    expect(wrapper.text()).toContain('Madrid')
    expect(wrapper.find('.verified-badge').text()).toContain('Fundador')
    expect(wrapper.text()).toContain('Proyectos Creados')
    expect(wrapper.text()).toContain('5')
    expect(wrapper.text()).toContain('Fondos Aportados')
  })
})
