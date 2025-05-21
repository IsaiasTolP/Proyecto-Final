import type { ProjectStats, Project, SimpleProject, ProjectImage, ProjectCategory } from "@/interfaces/Project";
import api from "./api";

async function getProjects() {
    const { data } = await api.get<Project>("/projects/list/")
    return data;
}

async function getFeatured() {
    const { data } = await api.get<Project[]>('/projects/list/featured/');
    return data
}

async function getLatest() {
    const { data } = await api.get<Project[]>('/projects/list/latest/');
    return data
}

async function getProject(id: number) {
    const { data } = await api.get<Project>(`/projects/list/${id}/`)
    return data;
}

async function getSimpleProject(id: number) {
    const { data } = await api.get<SimpleProject>(`/projects/simple-project-list/${id}/`)
    return data
}

async function getProjectByQuery(query: string) {
    const { data } = await api.get<Project[]>(`/projects/list/?search=${encodeURIComponent(query)}`);
    return data
}

async function getCategories() {
    const { data } = await api.get<ProjectCategory[]>("/projects/categories/")
    return data;
}

async function getCategory(id: number) {
    const { data } = await api.get<ProjectCategory>(`/projects/categories/${id}/`);
    return data
}

async function getProjectsImages() {
    const { data } = await api.get<ProjectImage[]>("/projects/project-images/")
    return data;
}

async function getProjectsImagesByProject(id: number) {
    const { data } = await api.get<ProjectImage[]>(`/projects/project-images/?project=${id}`)
    return data;
}

async function getProjectStats() {
    const { data } = await api.get<ProjectStats>("/projects/stats/")
    return data;
}

export { getProjects, getFeatured, getLatest, getProject, getProjectByQuery, getSimpleProject, getCategories, getCategory, getProjectsImages, getProjectsImagesByProject, getProjectStats };