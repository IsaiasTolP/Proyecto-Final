import type { ProjectStats, Project } from "@/interfaces/Project";
import api from "./api";

async function getProjects() {
    const { data } = await api.get<Project>("/projects/list/")
    return data;
}

async function getProject(id: number) {
    const { data } = await api.get<Project>(`/projects/list/${id}/`)
    return data;
}

async function getCategories() {
    const { data } = await api.get("/projects/categories/")
    return data;
}

async function getProjectsImages() {
    const { data } = await api.get("/projects/project-images/")
    return data;
}

async function getProjectStats() {
    const { data } = await api.get<ProjectStats>("/projects/stats/")
    return data;
}

export { getProjects, getProject, getCategories, getProjectsImages, getProjectStats };