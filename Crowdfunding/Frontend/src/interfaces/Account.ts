interface User {
    id: number;
    username: string;
}

interface ProfileData {
    id: number;
    user: User;
    bio: string;
    pfp: string;
    location: string;
    is_founder: boolean;
}

export type { User, ProfileData };