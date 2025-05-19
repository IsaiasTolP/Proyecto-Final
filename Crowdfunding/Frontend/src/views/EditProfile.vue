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
        <input id="location" v-model="form.location" type="text" class="form-control" maxlength="100" />
      </div>

      <!-- Campos adicionales para Fundadores -->
      <div v-if="form.is_founder">
        <div class="mb-3">
          <label for="website" class="form-label">Sitio Web</label>
          <input id="website" v-model="form.website" type="url" class="form-control" maxlength="200"/>
        </div>

        <div class="mb-3">
          <label for="contactEmail" class="form-label">Email de Contacto</label>
          <input id="contactEmail" v-model="form.contact_email" type="email" class="form-control" maxlength="100"/>
        </div>

        <div class="mb-3">
          <h5 class="form-label">Redes Sociales</h5>
          <div
            v-for="(url, key) in form.social_media"
            :key="String(key)"
            class="d-flex align-items-center mb-2"
          >
            <input
              v-model="form.social_media[key]"
              :placeholder="String(key)"
              type="url"
              class="form-control me-2"
              required
            />
            <button
              type="button"
              class="btn btn-outline-danger"
              @click="removeSocial(String(key))"
            >
              ×
            </button>
          </div>

          <!-- Nuevo par clave/valor -->
          <div class="d-flex align-items-center mb-3">
            <select
              v-model="newSocial.name"
              class="form-select me-2"
            >
              <option disabled value="">Selecciona una red</option>
              <option
                v-for="network in allowedSocialKeys.filter(k => !(k in form.social_media))"
                :key="network"
                :value="network"
              >
                {{ network.charAt(0).toUpperCase() + network.slice(1) }}
              </option>
            </select>

            <input
              v-model="newSocial.url"
              placeholder="https://..."
              type="url"
              class="form-control me-2"
            />
            <button
              type="button"
              class="btn btn-outline-primary"
              @click="addSocial"
              :disabled="!newSocial.name || !newSocial.url"
            >
              + Añadir
            </button>
          </div>
        </div>
      </div>

      <!-- Error -->
      <div v-if="messageStore.message" :class="['alert', 'alert-danger']">{{ messageStore.message }}</div>

      <button type="submit" class="btn btn-success">Guardar Cambios</button>
      <router-link :to="`/profile/${auth.user?.id}`" class="mx-3 btn btn-outline-success">Cancelar</router-link>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/services/api';
import axios, { AxiosError } from 'axios';
import { useMessageStore } from '@/stores/message';
import { useAuthStore } from '@/stores/auth';
import type { FounderProfileData, ProfileData } from '@/interfaces/Account';

const auth = useAuthStore();
const router = useRouter();
const messageStore = useMessageStore();
const uploadError = ref(false);
messageStore.clearMessage();

const error = 'error';
const success = 'success';

const allowedSocialKeys = ['twitter', 'instagram', 'linkedin'];

const form = ref<FounderProfileData>({
  id: 0,
  user: null,
  bio: '',
  pfp: undefined,
  location: '',
  is_founder: false,
  website: '',
  contact_email: '',
  social_media: {
    twitter: '',
    instagram: '',
    linkedin: ''
  }
});

const newSocial = ref({ name: '', url: '' });

const url = auth.user?.is_founder
  ? '/accounts/founders/me/'
  : '/accounts/profiles/me/';

onMounted(async () => {
  try {
    const { data } = await api.get<FounderProfileData | ProfileData>(url);
    Object.assign(form.value, data);
    console.log(form.value.social_media);
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
      uploadError.value = true;
      messageStore.setMessage('Formato de imagen no válido. Solo se permiten JPEG, JPG y PNG.', error);
      return;
    } else {
      uploadError.value = false;
      messageStore.clearMessage();
      form.value.pfp = file;
    }
  }
}

function addSocial() {
  const key = newSocial.value.name.toLowerCase().trim() as keyof typeof form.value.social_media;

  if (!allowedSocialKeys.includes(key)) {
    messageStore.setMessage(`Solo se permiten las redes sociales: ${allowedSocialKeys.join(', ')}`, error);
    return;
  }

  form.value.social_media[key] = newSocial.value.url;

  // Limpiar inputs
  newSocial.value.name = '';
  newSocial.value.url = '';
}

function removeSocial(key: string) {
  if (allowedSocialKeys.includes(key as keyof typeof form.value.social_media)) {
    delete form.value.social_media[key as keyof typeof form.value.social_media];
  }
}

async function submitProfile() {
  try {
    const payload = new FormData();
    payload.append('bio', form.value.bio);
    payload.append('location', form.value.location);

    if (form.value.pfp && form.value.pfp instanceof File) {
      payload.append('pfp', form.value.pfp);
    }

    if (form.value.is_founder) {
      payload.append('website', form.value.website || '');
      payload.append('contact_email', form.value.contact_email || '');
      payload.append('social_media', JSON.stringify(form.value.social_media || {}));
    }

    if (uploadError.value) {
      messageStore.setMessage('Corrige los errores antes de enviar el formulario', error);
      return;
    }

    await api.put(url, payload, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    messageStore.setMessage('Perfil actualizado con éxito.', success);
    router.push({ name: 'Account', params: { id: auth.user?.id } });
  } catch (err: any) {
    messageStore.setMessage('Error al guardar los cambios.', error);

    if (axios.isAxiosError(err)) {
      const axiosError = err as AxiosError;
      const status = axiosError.response?.status;
      if (status === 400) {
        messageStore.setMessage('Datos inválidos. Por favor verifica los campos.', error);
      } else if (status === 500) {
        messageStore.setMessage('Error interno del servidor. Intenta más tarde.', error);
      } else {
        messageStore.setMessage('Error de conexión. Intenta más tarde.', error);
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
