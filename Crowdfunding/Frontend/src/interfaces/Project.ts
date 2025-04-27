interface ProjectImage { id: number; image: string; }
interface ProjectCategory { id: number; category: string; }
interface ProjectOwner { id: number; username: string; }
interface Project {
    id: number;
    name: string;
    description: string;
    goal: string;
    start_date: string;
    is_active: boolean;
    category: ProjectCategory;
    owner: ProjectOwner;
    project_images: ProjectImage[];
    total_donated: string;
    percent_completed: number;
}

export type { Project, ProjectImage, ProjectCategory, ProjectOwner };