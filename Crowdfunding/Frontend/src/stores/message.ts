import { defineStore } from "pinia";
import { ref } from "vue";

export const useMessageStore = defineStore("message", () => {
    const message = ref<string>();
    const type = ref<string>();

    function setMessage(msg: string, t: string) {
        message.value = msg;
        type.value = t;
        setInterval(() => {
        clearMessage();
        }, 5000);
    }

    function clearMessage() {
        message.value = '';
        type.value = '';
    }

    return { message, type, setMessage, clearMessage };
} 
);