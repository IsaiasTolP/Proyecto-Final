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
    [key: string]: string;
}

interface FounderProfileData extends ProfileData {
    website: string;
    contact_email: string;
    social_media: SocialMedia;
}

export type { User, ProfileData, FounderProfileData };