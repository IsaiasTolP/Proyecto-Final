import type { ProfileData, User } from "./Account";
import type { SimpleProject } from "./Project";

interface Contribution {
    id: number;
    contributor: User;
    amount: number;
    date: string;
    message: string;
    project: number;
    payment_method: number;
    profile?: ProfileData;
    simpleProject?: SimpleProject;
}

export type { Contribution };