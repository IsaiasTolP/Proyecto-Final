<template>
    <div class="container py-5">
      <h2 class="mb-4 text-success">Editar Perfil</h2>
  
      <form @submit.prevent="submitProfile" enctype="multipart/form-data">
        <!-- Imagen -->
        <div class="mb-3">
          <label for="pfp" class="form-label">Foto de Perfil</label>
          <input type="file" class="form-control" id="pfp" @change="handleFileUpload" />
        </div>
  
        <!-- Bio -->
        <div class="mb-3">
          <label for="bio" class="form-label">Biografía</label>
          <textarea id="bio" v-model="form.bio" class="form-control" rows="3" maxlength="250" />
        </div>
  
        <!-- Localización -->
        <div class="mb-3">
          <label for="location" class="form-label">Ubicación</label>
          <input id="location" v-model="form.location" type="text" class="form-control" />
        </div>
  
        <!-- Campos adicionales para Fundadores -->
        <div v-if="form.is_founder">
          <div class="mb-3">
            <label for="website" class="form-label">Sitio Web</label>
            <input id="website" v-model="form.website" type="url" class="form-control" />
          </div>
  
          <div class="mb-3">
            <label for="contactEmail" class="form-label">Email de Contacto</label>
            <input id="contactEmail" v-model="form.contact_email" type="email" class="form-control" />
          </div>
  
          <div class="mb-3">
            <label class="form-label">Redes Sociales</label>
            <div v-for="(url, key) in form.social_media" :key="key" class="mb-2">
              <input
                :placeholder="String(key)"
                v-model="form.social_media[key]"
                type="url"
                class="form-control"
              />
            </div>
          </div>
        </div>
  
        <!-- Error -->
        <div v-if="messageStore.message" :class="['alert', 'alert-danger']">{{ messageStore.message }}</div>
  
        <button type="submit" class="btn btn-success">Guardar Cambios</button>
      </form>
    </div>
</template>

<script setup lang="ts">
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import api from '@/services/api';
	import axios, { AxiosError } from 'axios';
	import { useMessageStore } from '@/stores/message';
  
  const router = useRouter();
  const form = ref<any>({
    bio: '',
    pfp: null,
    location: '',
    is_founder: false,
    website: '',
    contact_email: '',
    social_media: {}
  });
  const messageStore = useMessageStore();
	messageStore.clearMessage();

  const error = 'error';
	const success = 'success';
  
  onMounted(async () => {
    try {
      const { data } = await api.get('/accounts/profiles/me/');
      Object.assign(form.value, data);
    } catch (err) {
			messageStore.setMessage('Error al cargar los datos del perfil.', error);
    }
  });
  
  function handleFileUpload(event: Event) {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    const file = target.files[0];
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!allowedTypes.includes(file.type)) {
			messageStore.setMessage('Formato de imagen no válido. Solo se permiten JPEG, JPG y PNG.', error);
      return;
    }
    form.value.pfp = file;
  }
}

  
  async function submitProfile() {
    try {
      const payload = new FormData();
      payload.append('bio', form.value.bio);
      payload.append('location', form.value.location);
      if (form.value.pfp && form.value.pfp instanceof File) {
				payload.append('pfp', form.value.pfp)
			}
			
      if (form.value.is_founder) {
        payload.append('website', form.value.website || '');
        payload.append('contact_email', form.value.contact_email || '');
        payload.append('social_media', JSON.stringify(form.value.social_media || {}));
      }
  
      const url = form.value.is_founder
        ? '/accounts/founders/me/'
        : '/accounts/profiles/me/';
  
      await api.put(url, payload, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

			messageStore.setMessage('Perfil actualizado con éxito.', success);
			router.push({ name: 'Account', params: { id: form.value.user.id } });
    } catch (err: any) {
			messageStore.setMessage('Error al guardar los cambios.', error);

			if (axios.isAxiosError(err)) {
				const axiosError = err as AxiosError;
				const status = axiosError.response?.status;
				if (status === 400 ) {
					messageStore.setMessage('Datos inválidos. Por favor verifica los campos.', error);
				} else if (status === 500 ) {
					messageStore.setMessage('Error interno del servidor. Intenta más tarde.', error);
				} else {
					messageStore.setMessage('Error de conexión. Intenta más tarde.', error)
				}

    } else {
			messageStore.setMessage('Error no controlado.', error);
			}
		}
  }
</script>

<style scoped>
  input[type='file'] {
    padding: 5px;
  }
</style>