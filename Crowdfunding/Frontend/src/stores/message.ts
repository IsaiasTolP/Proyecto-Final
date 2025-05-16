import router from "@/router";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useMessageStore = defineStore("message", () => {
    const message = ref<string>();
    const type = ref<string>();

    function setMessage(msg: string, t: string, persist: boolean = false) {
        message.value = msg;
        type.value = t;
        if (!persist) {
            router.beforeEach((to, from, next) => {
                clearMessage();
                next();
            })
        }
    }

    function clearMessage() {
        message.value = '';
        type.value = '';
    }

    return { message, type, setMessage, clearMessage };
} 
);