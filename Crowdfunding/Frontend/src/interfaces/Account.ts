interface User {
    id: number;
    username: string;
    email: string;
    is_founder: boolean;
}

interface ProfileData {
    id: number;
    user: User | null;
    bio: string;
    pfp: string | File | undefined;
    location: string;
    is_founder: boolean;
}

interface SocialMedia {
    twitter: string;
    instagram: string;
    linkedin: string;
}

interface FounderProfileData extends ProfileData {
    website: string;
    contact_email: string;
    social_media: SocialMedia;
}

interface ProfileStats {
    created_projects: number;
    supported_projects: number;
    given_funds: number;
}

export type { User, ProfileData, FounderProfileData, ProfileStats };