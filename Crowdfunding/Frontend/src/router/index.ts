import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import api from "@/services/api";
import type { Project } from '@/interfaces/Project';
import type { ProfileData } from "@/interfaces/Account";

const routes = [
    { path: "/", name: "Home", component: () => import("@/views/Home.vue") },
    { path: "/auth", name: "Auth", component: () => import("@/components/Auth.vue"), meta: { requiresUnauth: true } },
    { path: "/projects", name: "Projects", component: () => import("@/views/Projects.vue") },
    { path: "/projects/:id", name: "ProjectDetails", component: () => import("@/views/ProjectDetail.vue"), props: true },
    { path: "/profile/:id", name: "Account", component: () => import("@/views/Account.vue"), meta: { requiresAuth: true} },
    { path: "/profile/edit", name: "EditProfile", component: () => import("@/views/EditProfile.vue"), meta: { requiresAuth: true} },
    { path: "/payment-methods", name: "PaymentMethods", component: () => import("@/views/PaymentMethods.vue"), meta: { requiresAuth: true} },
    { path: "/payment-methods/add", name: "AddPaymentMethod", component: () => import("@/components/AddPaymentMethod.vue"), meta: { requiresAuth: true} },
    { path: "/project/create", name: "CreateProject", component: () => import("@/views/CreateProject.vue"), meta: {requiresAuth: true, founderRequired: true} },
    { path: "/projects/:id/contribute", name: "Contribute", component: () => import("@/views/ContributionForm.vue"), meta: {requiresAuth: true, disallowOwner: true}},
    { path: "/profile/:id/contributions", name: "MyContributionsHistory", component: () => import("@/views/MyContributionsHistory.vue"), meta: { requiresAuth: true, onlyProfileOwner: true}},
    { path: "/projects/:id/contributions", name: "ProjectContributionsHistory", component: () => import("@/views/ProjectContributionsHistory.vue"), meta: { requiresAuth: true, onlyProjectOwner: true}},
    { path: "/user/edit", name: "EditUser", component: () => import("@/views/EditUser.vue"), meta: { requiresAuth: true} },
    { path: "/projects/me", name: "MyProjects", component: () => import("@/views/MyProjects.vue"), meta: { requiresAuth: true, founderRequired: true} },
    { path: "/projects/edit/:id", name: "EditProject", component: () => import("@/views/EditProject.vue"), meta: { requiresAuth: true, founderRequired: true, onlyProjectOwner: true} },
    { path: "/projects/search", name: "ProjectSearch", component: () => import("@/views/ProjectSearch.vue"), meta: { requiresAuth: true} },
    { path: "/story", name: "Story", component: () => import("@/views/Story.vue") },
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

    if (to.meta.founderRequired) {
        try {
            const { data: profile } = await api.get<ProfileData>(`/accounts/profiles/me/`);
            if (!profile.is_founder) {
                return next({ name: "Home" });
            }
        } catch (e) {
            return router.back()
        }
        ;
    }

    if (to.meta.disallowOwner) {
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

    if (to.meta.onlyProfileOwner) {
        const userId = to.params.id
        try {
            const { data: profile } = await api.get<ProfileData>(`/accounts/profiles/user/${userId}/`);
            if (profile.user?.id !== auth.user?.id) {
                return router.back()
            }
        } catch (e: any) {
            console.error(e)
        }
    }

    if (to.meta.onlyProjectOwner) {
        const projectId = to.params.id
        try {
            const { data: project } = await api.get<Project>(`/projects/list/${projectId}/`);
            if (project.owner !== auth.user?.id) {
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