import { mount } from '@vue/test-utils'
import EditPaymentMethodForm from '../../src/components/EditPaymentMethodForm.vue'
import { describe, it, expect, vi } from 'vitest'

describe('EditPaymentMethodForm.vue', () => {
  const paymentMethodProp = {
    id: 42,
    holder_name: 'María López',
    expiration_date: '2026-07-15',
  }

  it('inicializa los campos holder_name y expiration_date desde la prop', () => {
    const wrapper = mount(EditPaymentMethodForm, {
      props: { paymentMethod: paymentMethodProp }
    })

    const holderInput = wrapper.find('#holder_name')
    const expInput    = wrapper.find('#expiration_date')

    expect((holderInput.element as HTMLInputElement).value).toBe('María López')
    expect((expInput.element    as HTMLInputElement).value).toBe('2026-07-15')
  })

  it('no inicializa campos opcionales (card_number, cvv) y los deja vacíos', () => {
    const wrapper = mount(EditPaymentMethodForm, {
      props: { paymentMethod: paymentMethodProp }
    })

    const cardInput = wrapper.find('#card_number')
    const cvvInput  = wrapper.find('#cvv')

    expect((cardInput.element as HTMLInputElement).value).toBe('')
    expect((cvvInput.element  as HTMLInputElement).value).toBe('')
  })

  it('emite "update" con los datos completos al enviar el formulario', async () => {
    const wrapper = mount(EditPaymentMethodForm, {
      props: { paymentMethod: paymentMethodProp }
    })

    await wrapper.find('#holder_name').setValue('Ana García')
    await wrapper.find('#card_number').setValue('1111222233334444')
    await wrapper.find('#cvv').setValue('987')
    await wrapper.find('#expiration_date').setValue('2027-08-20')

    await wrapper.find('form').trigger('submit.prevent')

    const emitted = wrapper.emitted('update')
    expect(emitted).toHaveLength(1)

    const payload = emitted![0][0]
    expect(payload).toEqual({
      holder_name:     'Ana García',
      card_number:     '1111222233334444',
      cvv:             '987',
      expiration_date:'2027-08-20',
    })
  })

  it('mantiene el id de paymentMethod sin incluirlo en el payload emitido', async () => {
    const wrapper = mount(EditPaymentMethodForm, {
      props: { paymentMethod: paymentMethodProp }
    })

    await wrapper.find('#holder_name').setValue('Laura Pérez')
    await wrapper.find('#expiration_date').setValue('2025-05-01')
    await wrapper.find('form').trigger('submit.prevent')

    const payload = wrapper.emitted('update')![0][0]
    expect(payload).not.toHaveProperty('id')
    expect(payload.holder_name).toBe('Laura Pérez')
    expect(payload.expiration_date).toBe('2025-05-01')
  })
})
