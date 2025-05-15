<template>
	<teleport to="body">
		<div v-if="props.visible" class="modal fade show d-block" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Cerrar Proyecto</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" @click="cancel" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p>¿Estás seguro de que deseas cerrar este proyecto? Esta acción no se puede deshacer.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="cancel">Cancelar</button>
            <button type="button" class="btn btn-danger" @click="confirm">Cerrar proyecto</button>
          </div>
        </div>
      </div>
		</div>
	</teleport>

    
		
</template>

<script setup lang="ts">

const props = defineProps<{
  visible: boolean;
}>();

const emits = defineEmits(['confirm', 'cancel']);

function confirm() {
  emits('confirm');
}

function cancel() {
  emits('cancel');
}
</script>