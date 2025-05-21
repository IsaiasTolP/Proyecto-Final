import { mount } from '@vue/test-utils'
import { describe, it, expect, beforeEach, afterEach} from 'vitest'
import CloseProjectDialog from '../../src/components/CloseProjectDialog.vue'

describe('CloseProjectDialog', () => {
  let wrapper: ReturnType<typeof mount>

  beforeEach(() => {
    wrapper = mount(CloseProjectDialog, {
      props: {
        visible: true,
      },
      attachTo: document.body,
    })
  })

  it('emite "confirm" al hacer clic en el botón de cerrar', async () => {
    await wrapper.vm.$nextTick()
    const buttons = document.querySelectorAll('button')
    const closeButton = Array.from(buttons).find(b => b.textContent?.includes('Cerrar proyecto'))
    expect(closeButton).toBeTruthy()
    await closeButton!.dispatchEvent(new Event('click'))
    await wrapper.vm.$nextTick()
    expect(wrapper.emitted()).toHaveProperty('confirm')
  })

  it('emite "cancel" al hacer clic en el botón de cancelar', async () => {
		await wrapper.vm.$nextTick()
		const buttons = document.querySelectorAll('button')
    const cancelButton = Array.from(buttons).find(b => b.textContent?.includes('Cancelar'))
		expect(cancelButton).toBeTruthy()
    await cancelButton!.dispatchEvent(new Event('click'))
    await wrapper.vm.$nextTick()
    expect(wrapper.emitted()).toHaveProperty('cancel')
  })
	
	afterEach(() => {
    wrapper.unmount()
  })
})
