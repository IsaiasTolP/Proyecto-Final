import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const routes = [
    { path: "/", name: "Home", component: () => import("@/views/Home.vue") },
    { path: "/auth", name: "Auth", component: () => import("@/components/Auth.vue"), meta: { requiresUnauth: true }},
    { path: "/projects/:id", name: "ProjectDetails", component: () => import("@/views/ProjectDetail.vue"), props: true },
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
    next();
});

export default router;