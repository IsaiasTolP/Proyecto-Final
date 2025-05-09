import type { User } from "./Account";

interface ProjectImage { id: number; image: string; }
interface ProjectCategory { id: number; category: string; }
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

export type { Project, ProjectImage, ProjectCategory, SimpleProject};