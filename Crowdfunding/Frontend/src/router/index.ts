import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const routes = [
    { path: "/", name: "Home", component: () => import("@/views/Home.vue") },
    { path: "/auth", name: "Auth", component: () => import("@/components/Auth.vue"), meta: { requiresUnauth: true } },
    { path: "/projects/:id", name: "ProjectDetails", component: () => import("@/views/ProjectDetail.vue"), props: true },
    { path: "/profile/:id", name: "Account", component: () => import("@/views/Account.vue"), meta: { requiresAuth: true} },
    { path: "/profile/edit", name: "EditProfile", component: () => import("@/views/EditProfile.vue"), meta: { requiresAuth: true} },
    { path: "/payment-methods", name: "PaymentMethods", component: () => import("@/views/PaymentMethods.vue"), meta: { requiresAuth: true} },
    { path: "/payment-methods/add", name: "AddPaymentMethod", component: () => import("@/components/AddPaymentMethod.vue"), meta: { requiresAuth: true} },
    { path: "/project/create", name: "CreateProject", component: () => import("@/views/CreateProject.vue"), meta: {requiresAuth: true}}
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, _from, next) => {
    const auth = useAuthStore();

    if (to.meta.requiresUnauth && auth.isAuthenticated) {
        return next({ name: "Home" });
    }
    if (to.meta.requiresAuth && !auth.isAuthenticated) {
        return next({ name: "Auth" });
    }
    next();
});

export default router;