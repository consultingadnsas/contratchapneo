declare module '#app' {
  interface NuxtApp {
    $api: typeof $fetch
  }
}

declare module 'vue' {
  interface ComponentCustomProperties {
    $api: typeof $fetch
  }
}

// ⚡️ LA SOLUTION EST ICI : On rend les interfaces accessibles partout
declare global {
  interface Country {
      id: number;
      name: string;
      code: string;
      is_ohada_member: boolean;
  }

  interface LegalDomain {
      id: number;
      name: string;
      slug: string;
      description?: string;
  }

  interface LegalProfessional {
      id: string;
      first_name: string;
      last_name: string;
      title: string;
      title_display: string;
      professional_order: string;
      registration_number: string;
      email: string;
      phone_number: string;
      website?: string;
      profile_picture?: string | null;
      bio: string;
      years_of_experience: number;
      country: Country;
      city: string;
      domains: LegalDomain[];
      is_active: boolean;
      is_verified: boolean;
  }
  interface Order {
    id: string;
    status: string;
    status_label: string;
    total_amount: number;
    buyer_email?: string;
    client_email?: string; // Plan B (Compta)
    created_at?: string;
    date_transaction?: string; // Plan B (Compta)
    order_items: any[];
  }
}

export {}