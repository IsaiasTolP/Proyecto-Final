import { mount, flushPromises } from '@vue/test-utils'
import Auth from '../../src/components/Auth.vue'
import { it, expect, vi} from 'vitest'
import { createTestingPinia } from '@pinia/testing'
import { useAuthStore } from '../../src/stores/auth'
import { createRouter, createMemoryHistory } from 'vue-router'

const router = createRouter({
  history: createMemoryHistory(),
  routes: [{ path: '/', name: 'Home', component: { template: 'home' } }],
})

it('renderiza formulario de login por defecto', () => {
  const wrapper = mount(Auth, {
    global: {
      plugins: [createTestingPinia(), router]
    }
  })

  expect(wrapper.text()).toContain('Iniciar Sesión')
  expect(wrapper.find('#email').exists()).toBe(false)
})

it('muestra campos de registro al alternar', async () => {
  const wrapper = mount(Auth, {
    global: {
      plugins: [createTestingPinia({ stubActions: false }), router]
    }
  })

  const toggleButton = wrapper.findAll('button.auth-toggle-link').find(btn =>
    btn.text().includes('¿No tienes cuenta?')
  )

  await toggleButton?.trigger('click')
  await flushPromises()

  expect(wrapper.text()).toContain('Registrarse')
  expect(wrapper.find('#email').exists()).toBe(true)
  expect(wrapper.find('#confirmPassword').exists()).toBe(true)
})


it('muestra error si faltan campos en login', async () => {
  const wrapper = mount(Auth, {
    global: {
      plugins: [createTestingPinia({ stubActions: false }), router]
    }
  })

  await wrapper.find('form').trigger('submit.prevent')
  await flushPromises()

  expect(wrapper.text()).toContain('Por favor completa todos los campos.')
})

it('muestra error si las contraseñas no coinciden en registro', async () => {
  const wrapper = mount(Auth, {
    global: {
      plugins: [createTestingPinia({
        stubActions: false
      })]
    }
  });

  const toggleButton = wrapper.findAll('button.auth-toggle-link').find(btn =>
    btn.text().includes('¿No tienes cuenta?')
  );
  await toggleButton?.trigger('click');
  await flushPromises();

  await wrapper.find('#username').setValue('usuario');
  await wrapper.find('#email').setValue('usuario@correo.com');
  await wrapper.find('#password').setValue('password123');
  await wrapper.find('#confirmPassword').setValue('diferente123');

  await wrapper.find('form').trigger('submit.prevent');

  expect(wrapper.text()).toContain('Las contraseñas no coinciden.');
});


it('llama a auth.register con datos correctos', async () => {
  const authMock = vi.fn()
  const wrapper = mount(Auth, {
    global: {
      plugins: [createTestingPinia({
        stubActions: false,
        createSpy: vi.fn,
        initialState: {
          auth: {}
        }
      })]
    }
  })

  const toggleButton = wrapper.findAll('button.auth-toggle-link').find(btn =>
    btn.text().includes('¿No tienes cuenta?')
  )
  await toggleButton?.trigger('click')
  await flushPromises()

  await wrapper.find('#username').setValue('testuser')
  await wrapper.find('#email').setValue('test@example.com')
  await wrapper.find('#password').setValue('12345678')
  await wrapper.find('#confirmPassword').setValue('12345678')

  await wrapper.find('form').trigger('submit.prevent')

  const authStore = useAuthStore()
  expect(authStore.register).toHaveBeenCalledWith(
    'testuser',
    'test@example.com',
    '12345678',
    false
  )
})

it('muestra el modal de recuperación al hacer clic', async () => {
  const wrapper = mount(Auth, {
    global: {
      plugins: [createTestingPinia()],
    }
  });

  const resetButton = wrapper.findAll('button.auth-toggle-link').find(btn =>
    btn.text().includes('¿Olvidaste tu contraseña?')
  );
  await resetButton?.trigger('click');
  await flushPromises();

  expect(wrapper.findComponent({ name: 'ResetPasswordDialog' }).exists()).toBe(true);
});






