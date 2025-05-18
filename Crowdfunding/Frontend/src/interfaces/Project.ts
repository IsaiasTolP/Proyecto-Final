import type { User } from "./Account";

interface ProjectImage { id: number; image: string; }
interface ProjectCategory { id: number; category: string; icon: string; num_projects: number; color: string; }
interface Project {
    id: number;
    name: string;
    description: string;
    goal: string;
    start_date: string;
    is_active: boolean;
    category: number;
    owner: number;
    project_images: ProjectImage[];
    total_donated: string;
    percent_completed: number;
}
interface SimpleProject {
    id: number;
    name: string;
    description: string;
    owner: User;
}

interface ProjectStats {
    total_projects: number;
    total_donated: number;
    active_projects: number;
    completed_projects: number;
    users: number;
}

export type { Project, ProjectImage, ProjectCategory, SimpleProject, ProjectStats};