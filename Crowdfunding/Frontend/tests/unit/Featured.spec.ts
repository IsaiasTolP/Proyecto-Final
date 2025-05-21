import { shallowMount, flushPromises } from '@vue/test-utils'
import Featured from '../../src/components/Featured.vue'
import api from '../../src/services/api'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createRouter, createMemoryHistory } from 'vue-router'

vi.mock('../../src/services/api', () => ({
  default: {
    get: vi.fn()
  }
}))

describe('Featured.vue', () => {
  let router: ReturnType<typeof createRouter>

  const sampleProjects = (n: number) =>
    Array.from({ length: n }, (_, i) => ({ id: i + 1, name: `P${i + 1}` }))

  beforeEach(() => {
    router = createRouter({
      history: createMemoryHistory(),
      routes: [{ path: '/projects/:id', name: 'ProjectDetail', component: { template: '<div/>' } }]
    })
    vi.clearAllMocks()
  })

  function mountComponent(projectsCount: number) {
    ;(api.get as any).mockResolvedValue({ data: sampleProjects(projectsCount) })

    return shallowMount(Featured, {
      global: {
        plugins: [router],
        stubs: {
          Swiper: { template: '<div><slot/></div>' },
          SwiperSlide: { template: '<div><slot/></div>' },
          FeaturedProjectCard: {
            props: ['project'],
            template: '<div class="card">{{ project.name }}</div>',
          },
          'router-link': { template: '<a><slot/></a>' },
        }
      },
      props: {
        projectCategories: []
      }
    })
  }

  it('no renderiza nada cuando la lista de proyectos está vacía', async () => {
    ;(api.get as any).mockResolvedValue({ data: [] })
    const wrapper = mountComponent(0)
    await flushPromises()
    expect(wrapper.find('body').exists()).toBe(false)
  })

  it('renderiza grid cuando hay 3 o menos proyectos', async () => {
    const wrapper = mountComponent(3)
    await flushPromises()

    expect(wrapper.find('div.row').exists()).toBe(true)
    const cards = wrapper.findAll('.card')
    expect(cards.length).toBe(3)
    expect(wrapper.find('.projects-slider-wrapper').exists()).toBe(false)
  })

  it('renderiza slider cuando hay más de 3 proyectos', async () => {
    const wrapper = mountComponent(5)
    await flushPromises()

    expect(wrapper.find('.projects-slider-wrapper').exists()).toBe(true)
    expect(wrapper.find('button.custom-swiper-button-prev').exists()).toBe(true)
    expect(wrapper.find('button.custom-swiper-button-next').exists()).toBe(true)
    expect(wrapper.findAll('.card').length).toBe(5)
  })

  it('llama a api.get en mounted con la ruta correcta', async () => {
    mountComponent(2)
    expect(api.get).toHaveBeenCalledWith('/projects/list/featured/')
  })

  it('navega al click en un proyecto usando goTo', async () => {
    const wrapper = mountComponent(1)
    await flushPromises()

    const pushSpy = vi.spyOn(router, 'push')
    await wrapper.find('.card').trigger('click')
    expect(pushSpy).toHaveBeenCalledWith('/projects/1')
  })
})
