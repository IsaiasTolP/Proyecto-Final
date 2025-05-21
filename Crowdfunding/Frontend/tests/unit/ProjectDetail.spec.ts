import { mount, flushPromises } from '@vue/test-utils'
import ProjectDetail from '../../src/views/ProjectDetail.vue'
import api from '../../src/services/api'
import { describe, it, expect, vi, beforeEach } from 'vitest'

vi.mock('vue-router', async () => {
  const actual = await vi.importActual<typeof import('vue-router')>('vue-router')
  return {
    ...actual,
    useRoute: () => ({ params: { id: '42' } }),
  }
})

const authUser = { id: 100, username: 'juan', is_founder: false }
vi.mock('@/stores/auth', () => ({
  useAuthStore: () => ({
    user: authUser,
    isAuthenticated: true,
  })
}))

vi.mock('@/services/api', () => ({
  default: {
    get: vi.fn(),
    patch: vi.fn(),
  }
}))

describe('ProjectDetail.vue', () => {
  const sampleProject = {
    id: 42,
    name: 'P Test',
    category: 7,
    owner: 100,
    goal: 500,
    start_date: '2025-01-01T00:00:00Z',
    is_active: true,
    percent_completed: 25,
    total_donated: 125,
    description: 'Contenido **MD** largo'.repeat(10),
    project_images: [
      { image: 'img1.jpg' },
      { image: 'img2.jpg' },
    ]
  }
  const sampleCategory = { id: 7, category: 'Tech' }
  const sampleOwner = { id: 100, username: 'juan' }
  const sampleContributions = [
    { id: 1, contributor: { username: 'ana' }, message: 'OK', date: '2025-02-02T00:00:00Z', amount: 50 },
  ]

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('muestra loader y luego datos básicos', async () => {
    ;(api.get as any)
      .mockResolvedValueOnce({ data: sampleProject })
      .mockResolvedValueOnce({ data: sampleCategory })
      .mockResolvedValueOnce({ data: sampleOwner })
      .mockResolvedValueOnce({ data: sampleContributions })

    const wrapper = mount(ProjectDetail, {
      global: {
        stubs: ['GoBackBtn', 'router-link', 'transition']
      }
    })

    expect(wrapper.text()).toContain('Cargando proyecto...')
    await flushPromises()
    expect(wrapper.text()).not.toContain('Cargando proyecto...')
    expect(wrapper.find('h1').text()).toBe('P Test')
    expect(wrapper.text()).toContain('Categoría: Tech')
    expect(wrapper.text()).toContain('Propietario: juan')
    expect(wrapper.text()).toContain('Meta: 500 €')
    expect(wrapper.text()).toContain('Activo')
    expect(wrapper.find('.progress-bar').attributes('style')).toContain('25%')
  })

  it('carousel muestra imagenes e indicadores y funciona Prev/Next', async () => {
    ;(api.get as any)
      .mockResolvedValueOnce({ data: sampleProject })
      .mockResolvedValueOnce({ data: sampleCategory })
      .mockResolvedValueOnce({ data: sampleOwner })
      .mockResolvedValueOnce({ data: [] })

    const wrapper = mount(ProjectDetail, {
      global: { stubs: ['GoBackBtn', 'router-link', 'transition'] }
    })
    await flushPromises()

    const img = wrapper.find('img')
    expect(img.attributes('src')).toBe('img1.jpg')

    await wrapper.find('button[aria-label="Imagen siguiente"]').trigger('click')
    expect(wrapper.find('img').attributes('src')).toBe('img2.jpg')

    await wrapper.find('button[aria-label="Imagen anterior"]').trigger('click')
    expect(wrapper.find('img').attributes('src')).toBe('img1.jpg')

    const dots = wrapper.findAll('.indicator')
    expect(dots.length).toBe(2)
    expect(dots[0].classes()).toContain('active')
  })

  it('muestra contribuciones y mensaje vacío', async () => {
    ;(api.get as any)
      .mockResolvedValueOnce({ data: sampleProject })
      .mockResolvedValueOnce({ data: sampleCategory })
      .mockResolvedValueOnce({ data: sampleOwner })
      .mockResolvedValueOnce({ data: [] })

    const wrapper = mount(ProjectDetail, {
      global: { stubs: ['GoBackBtn', 'router-link', 'transition'] }
    })
    await flushPromises()

    expect(wrapper.text()).toContain('Aún no hay contribuciones.')
  })

  it('cierra proyecto y recarga al hacer click en Close', async () => {
    ;(api.get as any)
      .mockResolvedValueOnce({ data: sampleProject })
      .mockResolvedValueOnce({ data: sampleCategory })
      .mockResolvedValueOnce({ data: sampleOwner })
      .mockResolvedValueOnce({ data: sampleContributions })
    const wrapper = mount(ProjectDetail, {
      global: { stubs: ['GoBackBtn', 'router-link', 'transition'] }
    })
    await flushPromises()

    await wrapper.find('button.btn-danger').trigger('click')
    await wrapper.vm.closeProject()
    expect(api.patch).toHaveBeenCalledWith('/projects/list/42/', { is_active: false })
  })
})