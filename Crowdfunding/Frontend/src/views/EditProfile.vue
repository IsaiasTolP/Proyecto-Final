<template>
  
  <div class="profile-edit-container">
    <GoBackBtn />
    <h2 class="title text-success mb-4">Editar Perfil</h2>

    <form @submit.prevent="submitProfile" enctype="multipart/form-data" class="profile-form">

      <!-- Imagen -->
      <div class="form-group">
        <label for="pfp" class="form-label">Foto de Perfil</label>
        <input
          type="file"
          id="pfp"
          class="form-control"
          @change="handleFileUpload"
          accept="image/jpeg,image/jpg,image/png"
        />
      </div>

      <!-- Bio -->
      <div class="form-group">
        <label for="bio" class="form-label">Biografía</label>
        <textarea
          id="bio"
          v-model="form.bio"
          class="form-control"
          rows="3"
          maxlength="250"
          placeholder="Cuéntanos sobre ti..."
        ></textarea>
      </div>

      <!-- Localización -->
      <div class="form-group">
        <label for="location" class="form-label">Ubicación</label>
        <input
          id="location"
          v-model="form.location"
          type="text"
          class="form-control"
          maxlength="100"
          placeholder="Ej. Madrid, España"
        />
      </div>

      <!-- Campos Fundador -->
      <div v-if="form.is_founder" class="founder-fields">
        <div class="form-group">
          <label for="website" class="form-label">Sitio Web</label>
          <input
            id="website"
            v-model="form.website"
            type="url"
            class="form-control"
            maxlength="200"
            placeholder="https://tuweb.com"
          />
        </div>

        <div class="form-group">
          <label for="contactEmail" class="form-label">Email de Contacto</label>
          <input
            id="contactEmail"
            v-model="form.contact_email"
            type="email"
            class="form-control"
            maxlength="100"
            placeholder="contacto@tuemail.com"
          />
        </div>

        <div class="form-group social-media-section">
          <h5 class="form-label mb-3">Redes Sociales</h5>

          <div
            v-for="(_url, key) in form.social_media"
            :key="key"
            class="social-input d-flex align-items-center mb-2"
          >
            <span class="social-icon">{{ getSocialIcon(key) }}</span>
            <input
              v-model="form.social_media[key]"
              :placeholder="key.charAt(0).toUpperCase() + key.slice(1)"
              type="url"
              class="form-control me-2"
              required
            />
            <button
              type="button"
              class="btn btn-outline-danger btn-sm"
              @click="removeSocial(key)"
              aria-label="Eliminar red social"
            >
              ×
            </button>
          </div>

          <!-- Añadir nueva red -->
          <div class="d-flex align-items-center mt-3">
            <select v-model="newSocial.name" class="form-select me-2" aria-label="Selecciona una red social">
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
              aria-label="URL de red social"
            />
            <button
              type="button"
              class="btn btn-outline-primary btn-sm"
              @click="addSocial"
              :disabled="!newSocial.name || !newSocial.url"
            >
              + Añadir
            </button>
          </div>
        </div>
      </div>

      <!-- Mensaje de error -->
      <div v-if="messageStore.message" class="alert alert-danger mt-3" role="alert">
        {{ messageStore.message }}
      </div>

      <div class="form-actions mt-4 d-flex">
        <button type="submit" class="btn btn-success me-3">Guardar Cambios</button>
        <router-link :to="`/profile/${auth.user?.id}`" class="btn btn-outline-success">Cancelar</router-link>
      </div>
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
import GoBackBtn from '@/components/GoBackBtn.vue';

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

function getSocialIcon(network: string) {
  const icons: Record<string, string> = {
    twitter: '🐦',
    instagram: '📸',
    linkedin: '🔗',
  };
  return icons[network.toLowerCase()] || '🌐';
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
.profile-edit-container {
  max-width: 600px;
  margin: 2rem auto;
  background: #fff;
  border-radius: 14px;
  padding: 2rem 2.5rem;
  box-shadow: 0 8px 24px rgb(0 0 0 / 0.1);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.title {
  font-weight: 700;
  color: #2f855a;
  text-align: center;
}

.profile-form .form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  font-weight: 600;
  color: #4a5568;
  margin-bottom: 0.5rem;
  display: block;
}

.form-control {
  border: 1.8px solid #cbd5e0;
  border-radius: 8px;
  padding: 0.6rem 1rem;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-control:focus {
  border-color: #2f855a;
  outline: none;
  box-shadow: 0 0 6px #68d391aa;
}

textarea.form-control {
  resize: vertical;
}

.founder-fields h5 {
  color: #2d3748;
  font-weight: 700;
  margin-bottom: 0.75rem;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 0.3rem;
}

.social-media-section .social-input {
  gap: 0.5rem;
}

.social-icon {
  font-size: 1.3rem;
  width: 28px;
  text-align: center;
  user-select: none;
}

.btn-outline-primary,
.btn-outline-danger,
.btn-success {
  border-radius: 8px;
  font-weight: 600;
  padding: 0.4rem 1.1rem;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.btn-outline-primary:hover {
  background-color: #2f855a;
  color: white;
  border-color: #2f855a;
}

.btn-outline-danger:hover {
  background-color: #e53e3e;
  color: white;
  border-color: #e53e3e;
}

.btn-success {
  background-color: #2f855a;
  border: none;
  color: white;
}

.btn-success:hover {
  background-color: #276749;
}

.form-actions {
  justify-content: flex-start;
}

.alert {
  border-radius: 10px;
  font-size: 0.95rem;
  padding: 1rem 1.25rem;
}

</style>
