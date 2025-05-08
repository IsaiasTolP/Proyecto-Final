import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import api from "@/services/api";
import type { Project } from '@/interfaces/Project';

const routes = [
    { path: "/", name: "Home", component: () => import("@/views/Home.vue") },
    { path: "/auth", name: "Auth", component: () => import("@/components/Auth.vue"), meta: { requiresUnauth: true } },
    { path: "/projects/:id", name: "ProjectDetails", component: () => import("@/views/ProjectDetail.vue"), props: true },
    { path: "/profile/:id", name: "Account", component: () => import("@/views/Account.vue"), meta: { requiresAuth: true} },
    { path: "/profile/edit", name: "EditProfile", component: () => import("@/views/EditProfile.vue"), meta: { requiresAuth: true} },
    { path: "/payment-methods", name: "PaymentMethods", component: () => import("@/views/PaymentMethods.vue"), meta: { requiresAuth: true} },
    { path: "/payment-methods/add", name: "AddPaymentMethod", component: () => import("@/components/AddPaymentMethod.vue"), meta: { requiresAuth: true} },
    { path: "/project/create", name: "CreateProject", component: () => import("@/views/CreateProject.vue"), meta: {requiresAuth: true}},
    { path: "/projects/:id/contribute", name: "Contribute", component: () => import("@/views/ContributionForm.vue"), meta: {requiresAuth: true, disallowOwner: true}},
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, _from, next) => {
    const auth = useAuthStore();

    if (to.meta.requiresUnauth && auth.isAuthenticated) {
        return next({ name: "Home" });
    }
    if (to.meta.requiresAuth && !auth.isAuthenticated) {
        return next({ name: "Auth" });
    }
    if (to.meta.disallowOwner && auth) {
        const projectId = to.params.id;
        try {
            const { data: project } = await api.get<Project>(`/projects/list/${projectId}/`);
            if (project.owner === auth.user?.id) {
                return router.back();
            }
        } catch (e) {
            console.error("Error al acceder al formulario", e);
            return next({ name: "Home" })
        }
        
    }
    next();
});

export default router;