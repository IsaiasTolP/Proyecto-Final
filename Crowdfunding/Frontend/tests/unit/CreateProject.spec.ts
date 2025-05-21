import { mount, flushPromises } from '@vue/test-utils'
import CreateProject from '../../src/views/CreateProject.vue'
import api from '../../src/services/api'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useMessageStore } from '../../src/stores/message'

const push = vi.fn()

vi.mock('vue-router', async () => {
  const actual = await vi.importActual<typeof import('vue-router')>('vue-router')
  return {
    ...actual,
    useRouter: () => ({ push }),
  }
})

vi.mock('@/stores/message', () => ({
  useMessageStore: () => ({ message: '', setMessage: vi.fn() })
}))

vi.mock('../../src/services/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn()
  }
}))

describe('CreateProject.vue', () => {
  let messageStore: ReturnType<typeof useMessageStore>

  beforeEach(() => {
    vi.clearAllMocks()
    messageStore = useMessageStore()
  })

  it('carga categorías al montar y las muestra en el select', async () => {
    (api.get as any).mockResolvedValueOnce({ data: [
      { id: 1, category: 'Arte' },
      { id: 2, category: 'Música' }
    ]})

    const wrapper = mount(CreateProject)
    await flushPromises()

    const options = wrapper.findAll('select#category option')
    expect(options).toHaveLength(3)
    expect(options[1].text()).toBe('Arte')
    expect(options[2].text()).toBe('Música')
  })

  it('muestra mensaje de error si falla la carga de categorías', async () => {
    (api.get as any).mockRejectedValueOnce(new Error('fail'))

    const wrapper = mount(CreateProject)
    await flushPromises()

    expect(wrapper.text()).toContain('No se pudieron cargar las categorías.')
  })

  it('muestra error si createProject falla', async () => {
  ;(api.get as any).mockResolvedValueOnce({ data: [] });

  ;(api.post as any).mockRejectedValueOnce(new Error('fail-create'));

  const wrapper = mount(CreateProject);
  await flushPromises();

  await wrapper.find('#name').setValue('X');
  await wrapper.find('#description').setValue('D');
  await wrapper.find('#goal').setValue('50');
  await wrapper.find('select#category').setValue('');

  await wrapper.find('form').trigger('submit.prevent');
  await flushPromises();

  expect(wrapper.text()).toContain(
    'Error al crear el proyecto. Comprueba el formulario'
  );
});
})
